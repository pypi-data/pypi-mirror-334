import dataclasses
import enum
import logging
import os
import socket
import subprocess
import typing as t
import uuid

import IPython
import requests

import mantik.utils.mantik_api.client as client
import mantik.utils.other as other_utils

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class GPUInfo:
    name: str
    id: str
    driver: str
    total_memory: str

    @classmethod
    def from_dict(cls, _dict):
        return cls(
            name=_dict["name"],
            id=_dict["id"],
            driver=_dict["driver"],
            total_memory=_dict["totalMemory"],
        )

    def to_json(self):
        return {
            "name": self.name,
            "id": self.id,
            "driver": self.driver,
            "totalMemory": self.total_memory,
        }


@dataclasses.dataclass
class RunInfrastructure:
    os: str
    cpu_cores: int
    gpu_count: int
    gpu_info: t.List[GPUInfo]
    hostname: str
    memory_gb: str
    platform: str
    processor: str
    python_version: str
    python_executable: str

    def to_json(self):
        return {
            "os": self.os,
            "cpuCores": self.cpu_cores,
            "gpuCount": self.gpu_count,
            "gpuInfo": [_gpu.to_json() for _gpu in self.gpu_info],
            "hostname": self.hostname,
            "memoryGb": self.memory_gb,
            "platform": self.platform,
            "processor": self.processor,
            "pythonVersion": self.python_version,
            "pythonExecutable": self.python_executable,
        }

    @classmethod
    def from_system(cls):
        _gpu_info = other_utils.get_gpu_info()
        return cls(
            os=other_utils.get_os(),
            cpu_cores=other_utils.get_cpu_cores(),
            gpu_count=len(_gpu_info),
            gpu_info=[GPUInfo.from_dict(_gpu) for _gpu in _gpu_info],
            hostname=other_utils.get_hostname(),
            memory_gb=other_utils.get_memory_gb(),
            platform=other_utils.get_platform(),
            processor=other_utils.get_processor(),
            python_version=other_utils.get_python_version(),
            python_executable=other_utils.get_python_executable(),
        )


class ProviderType(enum.Enum):
    JUPYTER = "Jupyter"
    COLAB = "Colab"


@dataclasses.dataclass
class NoteBookSource:
    """
    A class representing the source of a notebook, including its location,
    version, and provider.

    This class encapsulates details about a notebook's origin, such as
    whether it is hosted
    on Google Colab or located locally. It provides functionality to
    represent the notebook
    information as JSON and to create instances based on the execution
    environment.

    Attributes:
        location (str): The location of the notebook. This can be a URL
        (e.g., for Google Colab)
            or a local file path.
        version (Optional[str]): The version of the notebook, typically
        derived from a Git commit,
            if available. This may not always be set (e.g., in environments
            like Google Colab).
        provider (ProviderType): The provider of the notebook, such as
        Google Colab or local execution.

    Methods:
        to_json() -> dict:
            Converts the notebook source details into a JSON-serializable
            dictionary.

        create_instance(provider: ProviderType) -> "NoteBookSource":
            Creates a new instance of NoteBookSource based on the specified
             provider. Handles
            environment-specific logic, such as detecting the Colab
            container hostname or using
            the local file path.

            For Google Colab:
                - Resolves the container hostname and IP address.
                - Sends a request to the Colab API to retrieve session
                details.
                - Constructs a URL pointing to the active notebook in Colab.

            For local execution:
                - Uses the current file path as the notebook location.
                - Retrieves the latest Git commit hash as the version.

            Raises:
                RuntimeError: If environment-specific detection fails (e.g.,
                 failure to retrieve
                Colab session details or hostname resolution issues).
    """

    location: str
    version: t.Optional[str]
    provider: ProviderType

    def to_json(self) -> dict:
        return {
            "location": self.location,
            "version": self.version,
            "provider": self.provider.value,
        }

    @classmethod
    def create_instance(cls, provider: ProviderType) -> "NoteBookSource":
        # currently, this only covers Colab vs not Colab
        if provider == ProviderType.COLAB:
            try:
                # there is a whole bunch of env vars that include the ip of the
                # container but resolving the hostname seemed like the most
                # reliable variant
                # to view them, open any colab notebook and run `!env | sort`

                colab_container_hostname = os.environ.get("HOSTNAME", None)
                if colab_container_hostname is None:
                    raise RuntimeError("Could not get Colab container hostname")
                try:
                    colab_container_ip = socket.gethostbyname(
                        colab_container_hostname
                    )
                except socket.gaierror as e:
                    raise RuntimeError(
                        "Could not resolve Colab Container Hostname "
                        f"({colab_container_hostname}) to IP"
                    ) from e

                request_url = f"http://{colab_container_ip}:9000/api/sessions"
                response = requests.get(request_url)
                response.raise_for_status()

                sessions = response.json()
                if not sessions:
                    raise RuntimeError(
                        "No sessions found"
                    )  # should never happen because we are in a session
                elif len(sessions) > 1:
                    raise RuntimeError(
                        "More than one session found,"
                        "cannot identify the correct one"
                    )

                fileId = sessions["notebook"]["path"]
                location = (
                    f"https://colab.research.google.com/notebook#{fileId}"
                )

            except Exception as e:
                raise RuntimeError("Colab URL Detection Failed") from e

        else:
            # Running not in google colab
            location = find_notebook_location()
            if location is None:
                raise ValueError("Could not determine notebook location")

            version = get_latest_git_commit()

        # version is not set because it is not clear how to get it in
        # google colab (revisionId)
        return cls(location=location, version=version, provider=provider)


def find_notebook_location():
    # Known keys that might contain notebook path
    known_keys = [
        "session",
        "__session__",
        "vsc_ipynb_file",
        "__vsc_ipynb_file__",
        "notebook_path",
        "notebook_name",
        "ipynb_path",
        "file_path",
    ]

    logging.info("Starting notebook location search")

    try:
        notebook_info = IPython.get_ipython().kernel.shell.user_ns
    except Exception as e:
        print(
            f"Unexpected error accessing notebook information, ensure you "
            f"are running this function in a python notebook: {e}"
        )
        return None

    found_paths = set()

    # First check known keys
    for key in known_keys:
        if key in notebook_info:
            value = notebook_info[key]
            if isinstance(value, str) and value.endswith(".ipynb"):
                found_paths.add(value)

    # If no paths found with known keys, search all dictionary values
    if not found_paths:
        for key, value in notebook_info.items():
            if isinstance(value, str) and value.endswith(".ipynb"):
                found_paths.add(value)

    if len(found_paths) == 0:
        logging.warning("No notebook paths found")
        return None  # No valid paths found
    elif len(found_paths) == 1:
        return found_paths.pop()  # Return the single path found
    else:
        # If multiple paths found, try to choose the most likely (longest) one
        logging.info(
            f"Found {len(found_paths)} potential notebook paths: {found_paths}"
        )
        return max(found_paths, key=len)


def submit_run(project_id: uuid.UUID, submit_run_data: dict, token: str):
    endpoint = f"/projects/{project_id}/runs"
    response = client.send_request_to_mantik_api(
        method="POST", data=submit_run_data, url_endpoint=endpoint, token=token
    )
    logger.info("Run has been successfully submitted")
    return response


def save_run(project_id: uuid.UUID, run_data: dict, token: str):
    endpoint = f"/projects/{project_id}/runs"
    response = client.send_request_to_mantik_api(
        method="POST",
        data=run_data,
        url_endpoint=endpoint,
        token=token,
        query_params={"submit": False},
    )
    logger.info("Run has been successfully saved")
    return response


def update_run_status(
    project_id: uuid.UUID, run_id: uuid.UUID, status: str, token: str
):
    endpoint = f"/projects/{project_id}/runs/{run_id}/status"
    response = client.send_request_to_mantik_api(
        method="PUT", data=status, url_endpoint=endpoint, token=token
    )
    logger.info("Run status has been successfully updated")
    return response


def update_logs(
    project_id: uuid.UUID, run_id: uuid.UUID, logs: str, token: str
):
    endpoint = f"/projects/{project_id}/runs/{run_id}/logs"
    response = client.send_request_to_mantik_api(
        method="PUT", data=logs, url_endpoint=endpoint, token=token
    )
    logger.info("Run logs has been successfully updated")
    return response


def get_download_artifact_url(
    project_id: uuid.UUID, run_id: uuid.UUID, token: str
):
    endpoint = f"/projects/{project_id}/runs/{run_id}/artifacts"
    response = client.send_request_to_mantik_api(
        method="GET", data={}, url_endpoint=endpoint, token=token
    )
    logger.info("Artifacts' download url successfully fetched")
    return response.json()["url"]


def update_run_infrastructure(
    project_id: uuid.UUID,
    run_id: uuid.UUID,
    infrastructure: RunInfrastructure,
    token: str,
):
    endpoint = f"/projects/{project_id}/runs/{run_id}/infrastructure"
    response = client.send_request_to_mantik_api(
        method="PUT",
        data=infrastructure.to_json(),
        url_endpoint=endpoint,
        token=token,
    )
    logger.info("Run infrastructure has been successfully updated")
    return response


def check_notebook_type() -> t.Optional[ProviderType]:
    """
    Determines the type of notebook environment in which the code is
    running.

    Returns:
    -------
    Optional[ProviderType]
        - ProviderType.JUPYTER: Running in Jupyter notebook
        - ProviderType.COLAB: Running in Google Colab
        - None: Running in IPython terminal or standard Python interpreter

    Notes:
        - This function uses `ipython.get_ipython()` to detect the type of
          interactive shell currently running.
        - It relies on checking substrings in the shell's type to
        distinguish
          between Jupyter, Google Colab, and other environments.
        - `ProviderType` is assumed to be an enum or class that defines
          constants for different notebook types (e.g., Jupyter, Colab).
    """
    shell = str(IPython.get_ipython())
    try:
        if "ipykernel" in shell:
            logger.info("Run executed in a notebook")
            return ProviderType.JUPYTER
        if "google.colab" in shell:
            logger.info("Run executed in a notebook")
            return ProviderType.COLAB
        return None
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return None


def update_notebook_source(
    project_id: uuid.UUID,
    run_id: uuid.UUID,
    notebook_source: NoteBookSource,
    token: str,
):
    """
    Updates the notebook source for a specific run within a project.

    Args:
        project_id (uuid.UUID): The unique identifier of the project.
        run_id (uuid.UUID): The unique identifier of the run.
        notebook_source (NoteBookSource): An object containing the notebook
        source data to be updated.
        token (str): The authentication token used to authorize the API
        request.

    Returns:
        Response: Status code returned from Mantik API after update process.

    Raises:
        Any exceptions raised during the API request will propagate.

    Side Effects:
        - Logs a success message if the update is completed successfully.
    """
    endpoint = f"/projects/{project_id}/runs/{run_id}/notebook-source"
    response = client.send_request_to_mantik_api(
        method="PUT",
        data=notebook_source.to_json(),
        url_endpoint=endpoint,
        token=token,
    )
    logger.info("Run notebook source has been successfully updated")
    return response


def get_latest_git_commit() -> str:
    """
    Retrieves the latest Git commit hash from the current repository.

    Returns:
        str: The latest Git commit hash as a string if the command executes
        successfully.
             If the current directory is not a Git repository or there are
             no commits, returns "Not a git repository or no git commit
             found".
             If an unexpected exception occurs, returns an error message
             with the exception details.

    Exceptions:
        - Handles `subprocess.CalledProcessError` if the `git rev-parse`
        command fails.
        - Handles any other exceptions and returns a descriptive error
        message.
    """
    try:
        # Execute the command to get the latest git commit hash
        commit_hash = (
            subprocess.check_output(
                ["git", "rev-parse", "HEAD"], stderr=subprocess.STDOUT
            )
            .strip()
            .decode("utf-8")
        )
        return commit_hash
    except subprocess.CalledProcessError:
        return "Not a git repository or no git commit found"
    except Exception as e:
        return f"Error fetching git commit: {str(e)}"
