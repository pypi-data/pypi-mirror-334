import argparse
import dataclasses
import importlib.util
import inspect
import os
import os.path
import subprocess
import sys
import tempfile
import time
from typing import Any

from orc_client.client import OrcClient

from orc_sdk.workflow import WorkflowRuntimeObject
from orc_sdk.step import FuncStep, RetValWrapper, RawStep
from orc_sdk.utils import catchtime, catchtime_deco


def load_module(file_name, module_name):
    spec = importlib.util.spec_from_file_location(module_name, file_name)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def compile_wf_config(wfro: WorkflowRuntimeObject) -> dict[str, Any]:
    wf_config = {
        "triggers": [],
        "steps": [],
    }

    steps = wfro.get_steps()
    for step_id, sci_info in steps.items():
        if isinstance(sci_info.sci, FuncStep):
            func_signature = inspect.signature(sci_info.sci.func)

            passed_args = {}
            for i, arg in enumerate(sci_info.sci.func_args):
                arg_name = list(func_signature.parameters.keys())[i]  # FIXME??
                passed_args[arg_name] = arg

            for name, value in sci_info.sci.func_kwargs.items():
                passed_args[name] = value

            step_args = []
            for i, name in enumerate(func_signature.parameters):
                if name in passed_args:
                    if isinstance(passed_args[name], RetValWrapper):
                        src_type = "step_output"
                        src_ref = f"{passed_args[name].sci.step_id}.{passed_args[name].name}"
                    else:
                        src_type = "constant"
                        src_ref = passed_args[name]
                else:
                    src_type = "constant"
                    src_ref = func_signature.parameters[name].default

                step_args.append({
                    "name": name,
                    "src_type": src_type,
                    "src_ref": src_ref,
                })

            task_type = "docker"

            task_params = {
                "docker_image": "TODO",
                "command": sci_info.sci.func.__name__,
            }

            if sci_info.sci.memory_limit_bytes is not None:
                task_params["memory_limit"] = sci_info.sci.memory_limit_bytes

            outputs = [{
                "name": name,
            } for name in sci_info.sci.retval_names]


        elif isinstance(sci_info.sci, RawStep):
            task_type = sci_info.sci.task_type
            task_params = sci_info.sci.task_params

            step_args = []
            for arg in sci_info.sci.args:
                step_args.append({
                    "name": arg.name,
                    "src_type": arg.src_type,
                    "src_ref": arg.src_ref,
                })

            outputs = []
            for output_name in sci_info.sci.outputs:
                outputs.append({
                    "name": output_name,
                })

            for key, value in task_params.items():
                if isinstance(value, RetValWrapper):
                    task_params[key] = f"{{{{ args.{value.name} }}}}"  # TODO: randomize value.name?
                    step_args.append({
                        "name": value.name,
                        "src_type": "step_output",
                        "src_ref": f"{value.sci.step_id}.{value.name}",
                    })

        else:
            raise NotImplementedError

        secrets = []
        for secret in sci_info.sci.secrets:
            secrets.append({
                "key": secret.key,
                "value_ref": secret.value_ref,
                "value_src_type": secret.value_src_type,
            })

        wf_config["steps"].append({
            "step_id": step_id,
            "task_type": task_type,
            "task_params": task_params,
            "args": step_args,
            "secrets": secrets,
            "outputs": outputs,
            "depends_on": list(sci_info.depends_on),
            "cache": {
                "enable": sci_info.sci.cache.enable,
            },
        })

    wf_config["triggers"] = wfro.triggers

    return wf_config


def get_wfro_from_file(filename: str) -> WorkflowRuntimeObject:
    module = load_module(filename, "user_code")
    for key, obj in module.__dict__.items():
        if getattr(obj, "is_workflow", False):
            wfro = obj()  # TODO: args?
            return wfro
    else:
        raise Exception("No workflow found")


def get_file_module_root(filename: str) -> str:
    dirname = os.path.dirname(os.path.abspath(filename))
    if not os.path.exists(os.path.join(dirname, "__init__.py")):
        return filename
    return get_file_module_root(dirname)


BASE_IMAGE = "cr.eu-north1.nebius.cloud/e00faee7vas5hpsh3s/orchestracto/sdk-simple-runtime:33"

DEFAULT_DOCKER_COMMAND = "docker"


@catchtime_deco
def login_in_registry(registry_url: str, token: str):
    proc = subprocess.Popen(
        ["docker", "login", registry_url, "--password-stdin", "-u", "user"],
        stdin=subprocess.PIPE, stdout=sys.stdout, stderr=sys.stderr
    )
    proc.communicate(token.encode())
    if proc.wait() != 0:
        print("Login failed", file=sys.stderr)
        sys.exit(1)


@dataclasses.dataclass
class DockerImageBuildRequest:
    dockerfile: str
    image_tag: str


def get_docker_image_build_request(
        workflow_path: str,
        image_name: str,
        wf_file_module: str,
        additional_requirements: list[str],
        registry_url: str,
        base_image: str = BASE_IMAGE,
) -> DockerImageBuildRequest:
    py_packages_installation = f"""
            RUN pip install -U {" ".join(additional_requirements)}
            """ if additional_requirements else ""

    dockerfile = f"""
        FROM {BASE_IMAGE} AS sdk_runtime
        FROM {base_image}
        USER root
        {py_packages_installation}
        RUN mkdir /orc
        COPY --from=sdk_runtime /usr/local/lib/python3.12/site-packages/orc_sdk /orc/lib/orc_sdk
        COPY --from=sdk_runtime /usr/local/bin/orc_run_step /usr/local/bin/orc_run_step
        RUN new_shebang='#!/usr/bin/env python3' && sed -i "1s|.*|$new_shebang|" /usr/local/bin/orc_run_step
        RUN chmod +x /usr/local/bin/orc_run_step
        COPY {os.path.basename(wf_file_module)} /orc/lib/{os.path.basename(wf_file_module)}
    """

    image_rel_path = workflow_path.removeprefix("//") + "/" + image_name
    docker_tag = f"{registry_url}/home/orchestracto/public_registry/{image_rel_path}:latest"

    return DockerImageBuildRequest(dockerfile=dockerfile, image_tag=docker_tag)


def get_docker_image_with_sha(docker_image: str) -> str:
    return subprocess.check_output([
        "docker", "inspect", "--format", "{{index .RepoDigests 0}}", docker_image
    ]).decode().strip()


@dataclasses.dataclass
class WorkflowInfo:
    workflow_path: str
    workflow_config: dict[str, Any]


@catchtime_deco
def build_wf_info_from_file(filename: str, debug_docker_build: bool = False) -> WorkflowInfo:
    with catchtime("get_wfro_from_file"):
        wfro = get_wfro_from_file(filename)
    with catchtime("compile_wf_config"):
        wf_config = compile_wf_config(wfro)

    wf_file_module = get_file_module_root(filename)

    if os.path.abspath(wf_file_module) != os.path.abspath(filename):
        wf_file_module_dir = os.path.dirname(wf_file_module)  # FIXME
        rel_file_path = os.path.abspath(filename).removeprefix(wf_file_module_dir + "/")
    else:
        rel_file_path = os.path.basename(filename)  # TODO FIXME
    path_in_container = f"/orc/lib/{rel_file_path}"

    default_docker_tag = None

    registry_url = os.environ.get("REGISTRY_URL")  # TODO: get from //sys/@ui_config?..
    if registry_url is None:
        registry_url = "registry." + os.environ["YT_PROXY"].removeprefix("https://").removeprefix("http://")
    login_in_registry(registry_url, os.environ["YT_TOKEN"])

    wfro_steps = wfro.get_steps()

    docker_build_requests: list[DockerImageBuildRequest] = []

    print("Preparing workflow config")
    for step in wf_config["steps"]:
        step_id = step["step_id"]
        sci = wfro_steps[step_id].sci
        if not isinstance(sci, FuncStep):
            continue

        if sci.additional_requirements or sci.base_image:
            dbr = get_docker_image_build_request(
                wfro.workflow_path, step_id,
                wf_file_module,
                wfro.additional_requirements + sci.additional_requirements,
                registry_url=registry_url,
                base_image=sci.base_image or BASE_IMAGE,
            )
            docker_build_requests.append(dbr)
            step["task_params"]["docker_image"] = dbr.image_tag
        else:
            if default_docker_tag is None:
                dbr = get_docker_image_build_request(
                    wfro.workflow_path, "default",
                    wf_file_module,
                    wfro.additional_requirements,
                    registry_url=registry_url,
                )
                default_docker_tag = dbr.image_tag
                docker_build_requests.append(dbr)
            step["task_params"]["docker_image"] = default_docker_tag

        step["task_params"]["env"] = {"PYTHONPATH": "/orc/lib", "YT_BASE_LAYER": step["task_params"]["docker_image"]}
        step["task_params"]["command"] = f"orc_run_step {path_in_container} {sci.func.__name__} >&2"
        step["task_params"]["func_code_hash"] = sci.func_code_hash

    docker_command = os.environ.get("DOCKER_COMMAND", DEFAULT_DOCKER_COMMAND)
    supports_push_in_build = docker_command.split("/")[-1] != "buildah"  # TODO: check `--version`

    if supports_push_in_build:
        print("Building and pushing docker images")
    else:
        print("Building docker images")

    with catchtime("build_and_push_docker_images"):
        build_processes: list[subprocess.Popen] = []

        stdout = sys.stdout if debug_docker_build else subprocess.PIPE
        stderr = sys.stderr if debug_docker_build else subprocess.PIPE

        for dbr in docker_build_requests:
            build_command = [
                docker_command, "build",
                "-t", dbr.image_tag,
                "-f", "-",
                "--platform", "linux/amd64",
                os.path.dirname(wf_file_module),
            ]

            if supports_push_in_build:
                build_command.append("--push")

            proc = subprocess.Popen(
                build_command,
                stdin=subprocess.PIPE, stdout=stdout, stderr=stderr,
                env={"BUILDKIT_PROGRESS": "plain", **os.environ},
            )
            try:
                proc.communicate(dbr.dockerfile.encode(), timeout=0.001)
            except subprocess.TimeoutExpired:
                pass
            build_processes.append(proc)

        while any(proc.poll() is None for proc in build_processes):
            if not debug_docker_build:
                sys.stdout.write(".")
                sys.stdout.flush()
            time.sleep(0.3)
        print()

        build_failed = False
        for idx, proc in enumerate(build_processes):
            out, err = proc.communicate()

            if proc.returncode != 0:
                build_failed = True
                if not debug_docker_build:
                    print("=== stdout ===")
                    print("\n".join(out.decode().splitlines()))
                    print("=== stderr ===")
                    print("\n".join(err.decode().splitlines()))

    if build_failed:
        print("BUILD FAILED")
        sys.exit(1)

    if not supports_push_in_build:  # TODO: find a way to do it in "main loop"
        print("Pushing docker images")
        for dbr in docker_build_requests:
            subprocess.run([docker_command, "push", dbr.image_tag], check=True)

    return WorkflowInfo(workflow_path=wfro.workflow_path, workflow_config=wf_config)


def process_python_file(filename: str, debug_docker_build: bool = False):
    print("Preparing workflow config...")
    with catchtime("prepare_workflow_config"):
        wf_info = build_wf_info_from_file(filename, debug_docker_build=debug_docker_build)
    print("Workflow config is ready, pushing it to orchestracto")

    if "ORC_URL" not in os.environ:
        yt_proxy = os.environ.get("YT_PROXY")
        if yt_proxy is None:
            raise ValueError("Either ORC_URL or YT_PROXY environment variable should be set")
        orc_url = "https://orc." + yt_proxy.removeprefix("https://").removeprefix("http://")
    else:
        orc_url = os.environ["ORC_URL"]

    orc_client = OrcClient(orc_url=orc_url, yt_token=os.environ["YT_TOKEN"])
    with catchtime("update_workflow_config_on_yt"):
        orc_client.update_workflow(wf_info.workflow_path, wf_info.workflow_config)
    print("Workflow is updated")


def configure_arg_parser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    subparsers = parser.add_subparsers(dest="command")

    get_config = subparsers.add_parser("get-config")
    get_config.add_argument("filename", type=str)

    process_parser = subparsers.add_parser("process")
    process_parser.add_argument("filename", type=str)
    process_parser.add_argument("--debug-docker-build", action="store_true")

    return parser


def process_args(args: argparse.Namespace):
    match args.command:
        case "process":
            process_python_file(args.filename, debug_docker_build=args.debug_docker_build)
