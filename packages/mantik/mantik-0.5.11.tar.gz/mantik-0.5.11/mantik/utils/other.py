import contextlib
import os
import platform
import socket
import sys
import typing as t

import GPUtil
import psutil


@contextlib.contextmanager
def temp_chdir(path: str):
    _old_cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(_old_cwd)


def construct_git_clone_uri(
    uri: str, git_access_token: str, platform: str
) -> str:
    # How github expects the URI to look like for cloning
    if platform == "GitLab":
        uri = uri.replace("https://", f"https://oauth:{git_access_token}@")
    else:  # GitHub
        uri = uri.replace("https://", f"https://{git_access_token}@")
    return uri


def get_os():
    return platform.system()


def get_cpu_cores():
    return psutil.cpu_count(logical=True)


def get_gpu_info() -> t.List[t.Dict]:
    """Retrieve GPU info.

    Currently only Nvidia GPUs are supported for bookkeeping
    """

    return [
        {
            "name": gpu.name,
            "id": str(gpu.id),
            "driver": gpu.driver,
            "totalMemory": str(gpu.memoryTotal),
        }
        for gpu in GPUtil.getGPUs()
    ]


def get_hostname():
    return socket.gethostname()


def get_memory_gb():
    return f"{psutil.virtual_memory().total / (1024**3):.2f} GB"


def get_platform():
    return platform.platform()


def get_processor():
    return platform.processor()


def get_python_version():
    return platform.python_version()


def get_python_executable():
    return sys.executable
