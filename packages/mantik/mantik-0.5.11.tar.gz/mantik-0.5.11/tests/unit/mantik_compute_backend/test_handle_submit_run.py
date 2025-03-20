import glob
import pathlib
import tempfile
import unittest.mock
import uuid

import mantik.testing as testing
import mantik.utils as utils
import mantik.utils.credentials as _credentials
import mantik_compute_backend.handle_submit_run as backend


@unittest.mock.patch("mlflow.projects.run")
def test_handle_submit_run_request(
    mock_run, submit_run_request_data, submit_run_request_files
):
    # MLflow returns run IDs as UUID string without dashes (`uuid.hex`)
    mock_run.return_value.run_id = uuid.uuid4().hex
    mock_run.return_value.job_id = "2"
    with utils.env.env_vars_set({utils.mlflow.TRACKING_URI_ENV_VAR: "foo"}):
        response = backend.handle_submit_run_request(
            **submit_run_request_data, **submit_run_request_files
        )
        assert response
        mock_run.assert_called()
        # Assert that secret environment variables are unset
        testing.env.assert_env_var(_credentials.UNICORE_USERNAME_ENV_VAR, None)


@unittest.mock.patch("mlflow.projects.run")
def test_handle_ssh_submit_run_request(
    mock_run, submit_ssh_run_request_data, submit_run_request_files
):
    mock_run.return_value.run_id = uuid.uuid4().hex
    mock_run.return_value.job_id = "2"
    with utils.env.env_vars_set({utils.mlflow.TRACKING_URI_ENV_VAR: "foo"}):
        response = backend.handle_ssh_submit_run_request(
            **submit_ssh_run_request_data, **submit_run_request_files
        )
        assert response
        mock_run.assert_called()


def test_unzip_to_tmp(zipped_unicore_content):
    with tempfile.TemporaryDirectory() as directory:
        backend._unzip_to_file(zipped_unicore_content, directory)
        files = list(
            map(
                lambda filepath: pathlib.Path(filepath).name,
                glob.glob(directory + "/*.py"),
            )
        )
        assert "main.py" in files
