"""Test that UnicoreErrors are passed to the client."""
import functools
import json
import os
import unittest.mock
import uuid

import firecrest
import requests
import requests.exceptions as request_exceptions

import mantik.testing as testing
import mantik_compute_backend.exceptions as exceptions


def test_config_error_response(client, broken_zipped_content, tmp_path):
    """Test that ConfigErrors are passed to the client."""
    experiment_id = 0
    response = client.post(
        f"/submit/{experiment_id}",
        data={
            "active_run_id": str(uuid.uuid4().hex),
            "entry_point": "main",
            "mlflow_parameters": json.dumps({"print": "bar"}),
            "hpc_api_user": "me",
            "hpc_api_password": "bar",
            "compute_budget_account": "empty",
            "compute_backend_config": "compute-backend-config.md",
            "mlflow_tracking_uri": (tmp_path / "foo.bar").as_uri(),
            "mlflow_tracking_token": "abc",
        },
        files={"mlproject_zip": broken_zipped_content.read()},
        headers={"Authorization": "Bearer test-valid-token"},
    )
    assert response.status_code == 400, response.text
    assert response.text == (
        '{"message":"While submitting the job, '
        "this configuration error occurred: "
        "The given file type '.md' "
        "is not supported for the config, the "
        "supported ones are: '.json', '.yml', '.yaml'.\"}"
    )


def test_unicore_http_error_response(
    client, mlproject_path, zipped_unicore_content, tmp_path
):
    """Test that UnicoreErrors are passed to the client."""
    experiment_id = 0
    response = client.post(
        f"/submit/{experiment_id}",
        data={
            "active_run_id": str(uuid.uuid4().hex),
            "entry_point": "main",
            "mlflow_parameters": json.dumps({"print": "bar"}),
            "hpc_api_user": "me",
            "hpc_api_password": "bar",
            "compute_budget_account": "empty",
            "compute_backend_config": "compute-backend-config.yaml",
            "mlflow_tracking_uri": (tmp_path / "foo").as_uri(),
            "mlflow_tracking_token": "abc",
        },
        files={"mlproject_zip": zipped_unicore_content.read()},
        headers={"Authorization": "Bearer test-valid-token"},
    )
    assert response.status_code == 400, response.text
    assert response.text == (
        '{"message":"Unicore backend error. '
        "Cause: Failed to connect to "
        "https://zam2125.zam.kfa-juelich.de:9112/JUWELS/rest/core "
        '-- check if user and password are correct"}'
    )
    # Note: Experiment ID environment variable is set implicitly here,
    # breaking other tests
    os.environ.pop("MLFLOW_EXPERIMENT_ID")


@unittest.mock.patch(
    "mantik_compute_backend.handle_submit_run.handle_submit_run_request",
    **{"return_value.raiseError.side_effect": request_exceptions.HTTPError},
)
def test_unicore_error_response(
    mocked_run, client, mlproject_path, zipped_unicore_content, tmp_path
):
    """Test that HTTPErrors are passed to the client."""
    mocked_run.side_effect = request_exceptions.HTTPError("Test")
    experiment_id = 0
    response = client.post(
        f"/submit/{experiment_id}",
        data={
            "active_run_id": str(uuid.uuid4().hex),
            "entry_point": "main",
            "mlflow_parameters": json.dumps({"print": "bar"}),
            "hpc_api_user": "me",
            "hpc_api_password": "bar",
            "compute_budget_account": "empty",
            "compute_backend_config": "compute-backend-config.yaml",
            "mlflow_tracking_uri": (tmp_path / "foo.bar").as_uri(),
            "mlflow_tracking_token": "abc",
        },
        files={"mlproject_zip": zipped_unicore_content.read()},
        headers={"Authorization": "Bearer test-valid-token"},
    )
    assert response.status_code == 400, response.text
    assert (
        response.text == '{"message":"While submitting the job, '
        'this request error occurred: Test"}'
    )


@unittest.mock.patch(
    "mantik_compute_backend.handle_submit_run.handle_submit_run_request",
    **{"return_value.raiseError.side_effect": ConnectionError},
)
def test_unicore_connection_error_response(
    mocked_run, client, mlproject_path, zipped_unicore_content, tmp_path
):
    """Test that ConnectionErrors are passed to the client."""
    mocked_run.side_effect = ConnectionError("Test")
    experiment_id = 0
    response = client.post(
        f"/submit/{experiment_id}",
        data={
            "active_run_id": str(uuid.uuid4().hex),
            "entry_point": "main",
            "mlflow_parameters": json.dumps({"print": "bar"}),
            "hpc_api_user": "me",
            "hpc_api_password": "bar",
            "compute_budget_account": "empty",
            "compute_backend_config": "compute-backend-config.yaml",
            "mlflow_tracking_uri": (tmp_path / "foo.bar").as_uri(),
            "mlflow_tracking_token": "abc",
        },
        files={"mlproject_zip": zipped_unicore_content.read()},
        headers={"Authorization": "Bearer test-valid-token"},
    )
    assert response.status_code == 400, response.text
    assert response.text == (
        '{"message":"While submitting the job, '
        'this connection error occurred: Test"}'
    )


@unittest.mock.patch(
    "mantik_compute_backend.handle_submit_run.handle_submit_run_request",
    **{"return_value.raiseError.side_effect": firecrest.FirecrestException},
)
def test_firecrest_error_response(
    mocked_run,
    client,
    mlproject_path,
    zipped_firecrest_content,
    tmp_path,
    monkeypatch,
):
    """Test that HTTPErrors are passed to the client."""
    fake_response_object = requests.models.Response()
    fake_response_object.status_code = 400
    mocked_run.side_effect = firecrest.FirecrestException(
        responses=[fake_response_object]
    )
    monkeypatch.setattr(
        firecrest,
        "ClientCredentialsAuth",
        functools.partial(
            testing.firecrest.FakeClientCredentialsAuth,
            login_successful=True,
        ),
    )
    experiment_id = 0
    response = client.post(
        f"/submit/{experiment_id}",
        data={
            "active_run_id": str(uuid.uuid4().hex),
            "entry_point": "main",
            "mlflow_parameters": json.dumps({"print": "bar"}),
            "hpc_api_user": "me",
            "hpc_api_password": "bar",
            "compute_budget_account": "empty",
            "compute_backend_config": "compute-backend-firecrest-config.yaml",
            "mlflow_tracking_uri": (tmp_path / "foo.bar").as_uri(),
            "mlflow_tracking_token": "abc",
        },
        files={"mlproject_zip": zipped_firecrest_content.read()},
        headers={"Authorization": "Bearer test-valid-token"},
    )
    assert response.status_code == 400, response.text
    assert response.text == (
        '{"message":"Firecrest backend error. Cause: last request: 400 None"}'
    )


def test_firecrest_credentials_response(
    client, mlproject_path, zipped_firecrest_content, tmp_path
):
    """Test that HTTPErrors are passed to the client."""
    experiment_id = 0
    response = client.post(
        f"/submit/{experiment_id}",
        data={
            "active_run_id": str(uuid.uuid4().hex),
            "entry_point": "main",
            "mlflow_parameters": json.dumps({"print": "bar"}),
            "hpc_api_user": "me",
            "hpc_api_password": "bar",
            "compute_budget_account": "empty",
            "compute_backend_config": "compute-backend-firecrest-config.yaml",
            "mlflow_tracking_uri": (tmp_path / "foo.bar").as_uri(),
            "mlflow_tracking_token": "abc",
        },
        files={"mlproject_zip": zipped_firecrest_content.read()},
        headers={"Authorization": "Bearer test-valid-token"},
    )
    assert response.status_code == 401, response.text
    assert response.text == (
        '{"message":"Firecrest backend error. Cause: Failed to connect to '
        "https://auth.cscs.ch/auth/realms/firecrest-clients/protocol/openid-connect/token "  # noqa E501
        '-- check if client ID and secret are correct"}'
    )


def test_mlflow_error_response(
    client, mlproject_path, zipped_unicore_content, tmp_path
):
    """Test that MLflow exceptions are passed to the client."""
    experiment_id = 0
    response = client.post(
        f"/submit/{experiment_id}",
        data={
            "active_run_id": str(uuid.uuid4().hex),
            "entry_point": "non-existent-entry-point",
            "mlflow_parameters": json.dumps({"foo": "bar"}),
            "hpc_api_user": "me",
            "hpc_api_password": "bar",
            "compute_budget_account": "empty",
            "compute_backend_config": "compute-backend-config.yaml",
            "mlflow_tracking_uri": (tmp_path / "foo.bar").as_uri(),
            "mlflow_tracking_token": "abc",
        },
        files={"mlproject_zip": zipped_unicore_content.read()},
        headers={"Authorization": "Bearer test-valid-token"},
    )
    assert response.status_code == 400, response.text
    assert response.text == (
        '{"message":"While submitting the job, '
        "this mlflow error occurred: Could not "
        "find non-existent-entry-point among "
        "entry points ['main', 'echo', 'multi-line'] or interpret "
        "non-existent-entry-point as a runnable script. "
        "Supported script file "
        "extensions: ['.py', '.sh']\"}"
    )
    # Note: Experiment ID environment variable and Mlflow tracking uri,
    # is set implicitly here,
    # breaking other tests
    os.environ.pop("MLFLOW_EXPERIMENT_ID")
    os.environ.pop("MLFLOW_TRACKING_URI")


@unittest.mock.patch(
    "mantik_compute_backend.handle_submit_run.handle_submit_run_request",
    **{"return_value.raiseError.side_effect": Exception},
)
def test_custom_500_internal_server_error(
    mocked_run,
    client_suppressing_raise,
    mlproject_path,
    zipped_unicore_content,
    tmp_path,
):
    """Test custom internal server error."""
    mocked_run.side_effect = Exception
    experiment_id = 0
    response = client_suppressing_raise.post(
        f"/submit/{experiment_id}",
        data={
            "active_run_id": str(uuid.uuid4().hex),
            "entry_point": "main",
            "mlflow_parameters": json.dumps({"foo": "bar"}),
            "hpc_api_user": "me",
            "hpc_api_password": "bar",
            "compute_budget_account": "empty",
            "compute_backend_config": "compute-backend-config.yaml",
            "mlflow_tracking_uri": (tmp_path / "foo.bar").as_uri(),
            "mlflow_tracking_token": "abc",
        },
        files={"mlproject_zip": zipped_unicore_content.read()},
        headers={"Authorization": "Bearer test-valid-token"},
    )
    assert response.status_code == 500, response.text
    assert response.text == '{"message":"Mantik Internal Server Error"}'


@unittest.mock.patch(
    "mantik_compute_backend.handle_submit_run.handle_submit_run_request",
    **{
        "return_value.raiseError.side_effect": exceptions.RequestEntityTooLargeException  # noqa
    },
)
def test_file_too_large_exception(
    mocked_run, client, mlproject_path, zipped_unicore_content, tmp_path
):
    """Test custom internal server error."""
    experiment_id = 0
    mocked_run.side_effect = exceptions.RequestEntityTooLargeException()
    response = client.post(
        f"/submit/{experiment_id}",
        data={
            "active_run_id": str(uuid.uuid4().hex),
            "entry_point": "main",
            "mlflow_parameters": json.dumps({"foo": "bar"}),
            "hpc_api_user": "me",
            "hpc_api_password": "bar",
            "compute_budget_account": "empty",
            "compute_backend_config": "compute-backend-config.yaml",
            "mlflow_tracking_uri": (tmp_path / "foo.bar").as_uri(),
            "mlflow_tracking_token": "abc",
        },
        files={"mlproject_zip": zipped_unicore_content.read()},
        headers={"Authorization": "Bearer test-valid-token"},
    )
    print(response.text)
    assert response.status_code == 413, response.text
    assert (
        response.text
        == '{"message":"The files you sent were too large to be handled by '
        "the API. Consider using scp for direct file transfer to remote "
        'compute resources. The maximum allowed size is 100.0 MB."}'
    )
