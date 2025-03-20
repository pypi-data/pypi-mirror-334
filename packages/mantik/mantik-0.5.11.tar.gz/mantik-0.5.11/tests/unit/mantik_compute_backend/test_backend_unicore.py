import functools
import json
import pathlib
import uuid

import mlflow.projects as projects
import pytest
import pyunicore.client

import mantik.config.core as core
import mantik.testing as testing
import mantik.utils as mantik_utils
import mantik.utils.credentials as _credentials
import mantik_compute_backend.backend as backend

FILE_PATH = pathlib.Path(__file__).parent

ALL_ENV_VARS = [
    _credentials.UNICORE_USERNAME_ENV_VAR,
    _credentials.UNICORE_PASSWORD_ENV_VAR,
    core.COMPUTE_BUDGET_ACCOUNT_ENV_VAR,
]


class TestUnicoreBackend:
    def test_run(
        self, monkeypatch, example_project_path, tmp_path, env_vars_set, caplog
    ):
        monkeypatch.setattr(
            pyunicore.client,
            "Transport",
            testing.pyunicore.FakeTransport,
        )
        fake_client_with_successful_login = functools.partial(
            testing.pyunicore.FakeClient,
            login_successful=True,
        )
        monkeypatch.setattr(
            pyunicore.client,
            "Client",
            fake_client_with_successful_login,
        )
        backend_config_path = (
            example_project_path / "compute-backend-config.json"
        )
        with open(backend_config_path) as infile:
            backend_config = json.load(infile)
        # Following env vars are set by MLflow before running a project.
        backend_config[
            projects.PROJECT_STORAGE_DIR
        ] = example_project_path.as_posix()

        # Point MLFLOW_TRACKING_URI to a temporary directory
        tracking_uri = tmp_path / "mlruns"

        with env_vars_set(
            {
                # Following env vars must be set for the config.
                **{key: "test-val" for key in ALL_ENV_VARS},
                mantik_utils.mlflow.TRACKING_URI_ENV_VAR: tracking_uri.as_uri(),
                mantik_utils.mlflow.ACTIVE_RUN_ID_ENV_VAR: str(
                    uuid.uuid4().hex
                ),
            }
        ):
            submitted_run = backend.Backend().run(
                project_uri=example_project_path.as_posix(),
                entry_point="main",
                params={"print": "test"},
                version=None,
                backend_config=backend_config,
                tracking_uri=None,
                experiment_id=None,
            )

            assert submitted_run._job._job.started
            assert pathlib.Path(example_project_path / "mantik.sh").exists()
            pathlib.Path(example_project_path / "mantik.sh").unlink()


def test_create_job_description_apptainer(
    example_project_path, example_project, example_unicore_config
):
    expected = {
        "Executable": 'source $(dirname "$(realpath "$0")")/mantik.sh',
        "Arguments": [],
        "Project": "test-project",
        "Resources": {"Queue": "batch"},
        "RunUserPrecommandOnLoginNode": True,
        "RunUserPostcommandOnLoginNode": True,
        "Stderr": "mantik.log",
        "Stdout": "mantik.log",
    }

    result = example_unicore_config.to_unicore_job_description(
        bash_script_name="mantik.sh"
    )

    # Environment contains additional MLFLOW env vars,
    # which depend on the execution environment
    expected_environment = {
        "SRUN_CPUS_PER_TASK": 100,
        "MANTIK_WORKING_DIRECTORY": "$UC_WORKING_DIRECTORY",
    }
    actual_environment = result.pop("Environment")
    assert all(
        actual_environment[key] == value
        for key, value in expected_environment.items()
    )

    assert result == expected


def test_create_job_description_python(
    example_project_path, example_project, example_unicore_config_for_python
):
    expected = {
        "Executable": 'source $(dirname "$(realpath "$0")")/mantik.sh',
        "Arguments": [],
        "Project": "test-project",
        "Resources": {"Queue": "batch"},
        "RunUserPrecommandOnLoginNode": True,
        "RunUserPostcommandOnLoginNode": True,
        "Stderr": "mantik.log",
        "Stdout": "mantik.log",
    }
    result = example_unicore_config_for_python.to_unicore_job_description(
        bash_script_name="mantik.sh"
    )

    # Environment contains additional MLFLOW env vars,
    # which depend on the execution environment
    expected_environment = {"MANTIK_WORKING_DIRECTORY": "$UC_WORKING_DIRECTORY"}
    actual_environment = result.pop("Environment")
    assert all(
        actual_environment[key] == value
        for key, value in expected_environment.items()
    )

    assert result == expected


@pytest.mark.parametrize(
    ("entry_point", "config", "expected"),
    [
        (
            "main",
            "example_unicore_config_for_python",
            (
                "echo 'Submitted bash script'\n"
                'cat "$(realpath "$0")"\n'
                "precommand compute node && source /venv/bin/activate "
                "&& python main.py "
                "whatever && postcommand compute node"
            ),
        ),
        (
            "main",
            "example_unicore_config",
            (
                "echo 'Submitted bash script'\n"
                'cat "$(realpath "$0")"\n'
                "srun apptainer run mantik-test.sif python main.py whatever"
            ),
        ),
        (
            "multi-line",
            "example_unicore_config",
            (
                "echo 'Submitted bash script'\n"
                'cat "$(realpath "$0")"\n'
                "srun apptainer run mantik-test.sif python main.py whatever  "
                "--o option1  --i option2"
            ),
        ),
    ],
)
def test_to_bash_script(
    request,
    example_project_path,
    example_project,
    entry_point,
    config,
    expected,
):
    config = request.getfixturevalue(config)

    entry_point = example_project.get_entry_point(entry_point)
    parameters = {"print": "whatever"}
    storage_dir = "test-dir"

    arguments = backend._create_arguments(
        entry_point=entry_point, parameters=parameters, storage_dir=storage_dir
    )

    result = config.to_bash_script(arguments)

    assert result == expected
