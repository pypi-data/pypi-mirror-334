"""Integration tests for UNICORE.

**WARNING:** The UNICORE container takes up to 15-30 seconds to process a job,
hence be careful with the number of test cases used.


"""
import pathlib
import uuid

import mlflow.entities as entities
import mlflow.projects as projects
import pytest

import mantik.config.core as core
import mantik.utils as utils
import mantik.utils.credentials as _credentials
import mantik_compute_backend.backend as backend

FILE_PATH = pathlib.Path(__file__).parent


@pytest.fixture()
def required_unicore_env_vars(unicore_credentials) -> dict:
    return {
        _credentials.UNICORE_USERNAME_ENV_VAR: unicore_credentials["user"],
        _credentials.UNICORE_PASSWORD_ENV_VAR: unicore_credentials["password"],
        core.COMPUTE_BUDGET_ACCOUNT_ENV_VAR: "test-project",
        utils.mlflow.ACTIVE_RUN_ID_ENV_VAR: str(uuid.uuid4().hex),
    }


RESOURCES = {
    "Queue": "batch",
    "Runtime": "1h",
    "Nodes": 1,
    "TotalCPUs": 1,
    "CPUsPerNode": 1,
    "MemoryPerNode": "1M",
}

EXPECTED_RESOURCE_MESSAGES = (
    "Queue=batch",
    "Runtime=3600",
    "Nodes=1",
    "TotalCPUs=1",
    "CPUsPerNode=1",
    "MemoryPerNode=1048576",
    "Project=test-project",
)


class TestUnicoreBackend:
    @pytest.mark.parametrize(
        (
            "entry_point",
            "params",
            "backend_config",
            "expected_job_status",
            "expected_log_messages",
        ),
        [
            # Test case: Apptainer with 1 env var
            #
            # * Test case will fail since no Apptainer image present in UNICORE
            #   container, thus the post command on login node won't be executed
            (
                "main",
                {"print": "test"},
                {
                    "Environment": {
                        "Variables": {"TEST_VAR": "test_value"},
                        "Apptainer": {
                            "Path": "/does/not/exist.sif",
                            "Type": "remote",
                        },
                        "PreRunCommandOnLoginNode": [
                            "echo precommand login node",
                            "echo again",
                        ],
                        "PostRunCommandOnLoginNode": [
                            "echo postcommand login node"
                        ],
                        "PreRunCommandOnComputeNode": [
                            "echo precommand compute node"
                        ],
                        "PostRunCommandOnComputeNode": [
                            "echo postcommand compute node"
                        ],
                    },
                    "Resources": RESOURCES,
                },
                entities.RunStatus.FAILED,
                [
                    *EXPECTED_RESOURCE_MESSAGES,
                    "MLFLOW_RUN_ID=",
                    "; export MLFLOW_RUN_ID",
                    'TEST_VAR="test_value"; export TEST_VAR',
                    'source $(dirname "$(realpath "$0")")/mantik.sh',
                ],
            ),
            # Test case: Python with 1 env var
            #
            # * Test case will fail since no venv present in UNICORE container,
            #   thus the post command on login node won't be executed
            (
                "main",
                {"print": "test"},
                {
                    "Environment": {
                        "Variables": {"TEST_VAR": "test_value"},
                        "Python": {
                            "Path": "/does/not/exist",
                        },
                        "PreRunCommandOnLoginNode": [
                            "echo precommand login node",
                            "echo again",
                        ],
                        "PostRunCommandOnLoginNode": [
                            "echo postcommand login node"
                        ],
                        "PreRunCommandOnComputeNode": [
                            "echo precommand compute node"
                        ],
                        "PostRunCommandOnComputeNode": [
                            "echo postcommand compute node"
                        ],
                    },
                    "Resources": RESOURCES,
                },
                entities.RunStatus.FAILED,
                [
                    *EXPECTED_RESOURCE_MESSAGES,
                    "MLFLOW_RUN_ID=",
                    "; export MLFLOW_RUN_ID",
                    'TEST_VAR="test_value"; export TEST_VAR',
                    "echo precommand login node",
                    "echo again",
                    'source $(dirname "$(realpath "$0")")/mantik.sh',
                ],
            ),
            # Test case: No execution environment and echo entry point
            #
            # * Should succeed
            # * Pre/postcommand will be executed on login node, hence no modules
            #   loaded here. Modules would make the pre command fail (no modules
            #   in UNICORE container), and the main application will not be
            #   executed, as well as the post command.
            (
                "echo",
                {"output": "test"},
                {
                    "Environment": {
                        "Variables": {"TEST_VAR": "test_value"},
                        "PreRunCommandOnLoginNode": [
                            "echo precommand login node",
                            "echo again",
                        ],
                        "PostRunCommandOnLoginNode": [
                            "echo postcommand login node"
                        ],
                    },
                    "Resources": RESOURCES,
                },
                entities.RunStatus.FINISHED,
                [
                    "Launched pre command <echo precommand login node && "
                    "echo again>\n",
                    "Executing command: echo precommand login node && "
                    "echo again",
                    "Execution on login node",
                    *EXPECTED_RESOURCE_MESSAGES,
                    'TEST_VAR="test_value"; export TEST_VAR',
                    "MLFLOW_RUN_ID=",
                    "; export MLFLOW_RUN_ID",
                    'source $(dirname "$(realpath "$0")")/mantik.sh',
                ],
            ),
        ],
    )
    def test_run(
        self,
        tmp_path,
        env_vars_set,
        unicore_api_url,
        required_unicore_env_vars,
        example_project_path,
        entry_point,
        params,
        backend_config,
        expected_job_status,
        expected_log_messages,
    ):
        backend_config = {
            **backend_config,
            "UnicoreApiUrl": unicore_api_url,
            # Following values are set by MLflow before running a project.
            projects.PROJECT_STORAGE_DIR: example_project_path.as_posix(),
        }

        expected_log_messages.extend(
            [
                # MLflow Tracking URI should be set by compute backend
                f'MLFLOW_TRACKING_URI="file://{tmp_path.as_posix()}/mlruns"; export MLFLOW_TRACKING_URI',  # noqa: E501
            ]
        )

        # Following env vars must be set for the config.
        tracking_uri = tmp_path / "mlruns"
        with env_vars_set(
            {
                **required_unicore_env_vars,
                # Point MLFLOW_TRACKING_URI to a temporary directory
                utils.mlflow.TRACKING_URI_ENV_VAR: tracking_uri.as_uri(),  # noqa: E501
            }
        ):
            result = backend.Backend().run(
                project_uri=example_project_path.as_posix(),
                entry_point=entry_point,
                params=params,
                version=None,
                backend_config=backend_config,
                tracking_uri=None,
                experiment_id=None,
            )
            # Wait for job to fail or succeed
            result.wait()
            # For the structure of the UNICORE job properties responce, see
            # `tests/resources/unicore-responses/job-property-response.json`.
            result_log_messages = "\n".join(result._job._job.properties["log"])
        for exp in expected_log_messages:
            assert exp in result_log_messages, f"Message {exp!r} not in logs"
        assert result.get_status() == expected_job_status
