import json
import pathlib
import unittest.mock
import uuid

import mlflow.projects as projects

import mantik.utils as mantik_utils
import mantik.utils.credentials as _credentials
import mantik_compute_backend.backend as backend
import mantik_compute_backend.ssh_remote_compute_system.job as ssh_job

FILE_PATH = pathlib.Path(__file__).parent

ALL_ENV_VARS = [
    _credentials.SSH_PASSWORD_ENV_VAR,
    _credentials.SSH_PRIVATE_KEY_ENV_VAR,
    _credentials.SSH_USERNAME_ENV_VAR,
]


class TestSSHRemoteComputeSystemBackend:
    def test_run(
        self,
        monkeypatch,
        example_project_path,
        tmp_path,
        env_vars_set,
    ):
        fake_ssh_client = unittest.mock.Mock()
        fake_job_id = "123"
        fake_ssh_client.submit_job.return_value = ssh_job.Job(
            job_id=fake_job_id, job_dir=pathlib.Path("sample-path")
        )

        with open(
            example_project_path / "compute-backend-ssh-config.json"
        ) as infile:
            backend_config = json.load(infile)

        # Following env vars are set by MLflow before running a project.
        backend_config[
            projects.PROJECT_STORAGE_DIR
        ] = example_project_path.as_posix()

        # Point MLFLOW_TRACKING_URI to a temporary directory
        tracking_uri = tmp_path / "mlruns"
        fake_run_id = str(uuid.uuid4().hex)
        with unittest.mock.patch(
            "mantik_compute_backend.backend._create_ssh_client",
            return_value=fake_ssh_client,
        ):
            with env_vars_set(
                {
                    # Following env vars must be set for the config.
                    **{key: "test-val" for key in ALL_ENV_VARS},
                    mantik_utils.mlflow.TRACKING_URI_ENV_VAR: tracking_uri.as_uri(),  # noqa E501
                    mantik_utils.mlflow.ACTIVE_RUN_ID_ENV_VAR: fake_run_id,
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
                assert submitted_run.run_id == fake_run_id
                assert submitted_run.job_id == fake_job_id
