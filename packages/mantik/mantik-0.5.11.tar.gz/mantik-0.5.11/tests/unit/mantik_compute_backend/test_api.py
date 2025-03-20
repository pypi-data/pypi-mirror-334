import dataclasses
import json
import unittest.mock
import uuid

import pytest
import starlette.status

import mantik_compute_backend.api as api
import mantik_compute_backend.models as models
import mantik_compute_backend.ssh_remote_compute_system.exceptions as ssh_exceptions  # noqa E

TEST_UUID = uuid.uuid4()


@dataclasses.dataclass
class FakeSubmittedRun:
    # MLflow returns run IDs as UUID string (`uuid.hex`)
    run_id: str = TEST_UUID.hex
    job_id: str = "1"


@pytest.mark.parametrize(
    ("headers", "expected"),
    [
        ({}, 401),
        (
            {"Authorization": "test-invalid-token"},
            401,
        ),
        (
            {"Authorization": "Bearer test-invalid-token"},
            401,
        ),
        (
            {"Authorization": "Bearer test-valid-token"},
            201,
        ),
    ],
)
@unittest.mock.patch(
    "mlflow.projects.run",
    return_value=FakeSubmittedRun(),
)
def test_submit_run(
    mock_mlflow_run, client, zipped_unicore_content, headers, expected
):
    response = client.post(
        f"{api.SUBMIT_PATH}/0",
        data={
            "active_run_id": str(uuid.uuid4().hex),
            "entry_point": "main",
            "mlflow_parameters": json.dumps({"foo": "bar"}),
            "hpc_api_user": "bar",
            "hpc_api_password": "baz",
            "compute_budget_account": "empty",
            "mlflow_tracking_uri": "foo.bar",
            "mlflow_tracking_token": "abcdefghijk",
        },
        files={"mlproject_zip": zipped_unicore_content.read()},
        headers=headers,
    )

    assert response.status_code == expected, response.text

    if expected == 201:
        expected_json = {
            "experiment_id": 0,
            "run_id": str(TEST_UUID),
            "unicore_job_id": "1",
        }
        result = response.json()

        assert result == expected_json

        mock_mlflow_run.assert_called()


@unittest.mock.patch(
    "mlflow.projects.run",
    return_value=FakeSubmittedRun(),
)
def test_submit_run_invalid_backend_config_type(
    mock_mlflow_run, client, zipped_unicore_content
):
    unsupported_format = ".yamml"
    response = client.post(
        f"{api.SUBMIT_PATH}/0",
        data={
            "active_run_id": str(uuid.uuid4().hex),
            "entry_point": "main",
            "mlflow_parameters": json.dumps({"foo": "bar"}),
            "hpc_api_user": "bar",
            "hpc_api_password": "baz",
            "compute_budget_account": "empty",
            "mlflow_tracking_uri": "foo.bar",
            "mlflow_tracking_token": "abcdefghijk",
            "compute_backend_config": f"compute-backend-config{unsupported_format}",  # noqa: E501
        },
        files={"mlproject_zip": zipped_unicore_content.read()},
        headers={"Authorization": "Bearer test-valid-token"},
    )

    error_message = response.json()["message"]
    mock_mlflow_run.assert_not_called()
    assert response.status_code == 400
    assert (
        error_message == "While submitting the job, "
        "this configuration error occurred: "
        f"The given file type '{unsupported_format}'"
        " is not supported for the config,"
        " the supported ones are: '.json', '.yml', '.yaml'."
    )


@unittest.mock.patch(
    "mantik_compute_backend.handle_submit_run.handle_submit_run_request",
    return_value=models.SubmitRunResponse(
        experiment_id=0, run_id=uuid.uuid4(), unicore_job_id="0"
    ),
)
@unittest.mock.patch("tempfile.TemporaryFile")
def test_memory_freed_when_success(
    mock_temporary_file,
    mock_handle_submit_run_request,
    client,
    zipped_unicore_content,  # noqa
):
    response = client.post(
        f"{api.SUBMIT_PATH}/0",
        data={
            "active_run_id": str(uuid.uuid4().hex),
            "entry_point": "main",
            "mlflow_parameters": json.dumps({"foo": "bar"}),
            "hpc_api_user": "bar",
            "hpc_api_password": "baz",
            "compute_budget_account": "empty",
            "mlflow_tracking_uri": "foo.bar",
            "mlflow_tracking_token": "abcdefghijk",
            "compute_backend_config": "backend-config.yaml",
        },
        files={"mlproject_zip": zipped_unicore_content.read()},
        headers={"Authorization": "Bearer test-valid-token"},
    )
    assert response.status_code == 201
    mock_temporary_file.assert_called()
    mock_temporary_file().write.assert_called()
    mock_temporary_file().seek.assert_called()
    mock_temporary_file().close.assert_called()
    mock_handle_submit_run_request.assert_called()


@unittest.mock.patch(
    "mantik_compute_backend.handle_submit_run.handle_submit_run_request",
    **{"return_value.raiseError.side_effect": Exception},
)
@unittest.mock.patch("tempfile.TemporaryFile")
def test_memory_freed_when_exception(
    mock_temp_file, mocked_run, client_suppressing_raise, zipped_unicore_content
):
    mocked_run.side_effect = Exception
    response = client_suppressing_raise.post(
        f"{api.SUBMIT_PATH}/0",
        data={
            "active_run_id": str(uuid.uuid4().hex),
            "entry_point": "main",
            "mlflow_parameters": json.dumps({"foo": "bar"}),
            "hpc_api_user": "bar",
            "hpc_api_password": "baz",
            "compute_budget_account": "empty",
            "mlflow_tracking_uri": "foo.bar",
            "mlflow_tracking_token": "abcdefghijk",
        },
        files={"mlproject_zip": zipped_unicore_content.read()},
        headers={"Authorization": "Bearer test-valid-token"},
    )

    assert response.status_code == 500
    mock_temp_file().close.assert_called()


def test_submit_too_large_file(
    client_with_small_size_limitation, zipped_unicore_content
):
    response = client_with_small_size_limitation.post(
        f"{api.SUBMIT_PATH}/0",
        data={
            "active_run_id": str(uuid.uuid4().hex),
            "entry_point": "main",
            "mlflow_parameters": json.dumps({"foo": "bar"}),
            "hpc_api_user": "bar",
            "hpc_api_password": "baz",
            "compute_budget_account": "empty",
            "mlflow_tracking_uri": "foo.bar",
            "mlflow_tracking_token": "abcdefghijk",
        },
        files={"mlproject_zip": zipped_unicore_content},
        headers={"Authorization": "Bearer test-valid-token"},
    )
    assert (
        response.status_code
        == starlette.status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
    )


@pytest.fixture
def sample_ssh_run_data():
    return {
        "active_run_id": str(uuid.uuid4().hex),
        "entry_point": "main",
        "mlflow_parameters": json.dumps({"foo": "bar"}),
        "ssh_username": "ssh user",
        "ssh_password": "baz",
        "ssh_private_key": "bam",
        "mlflow_tracking_uri": "foo.bar",
        "mlflow_tracking_token": "abcdefghijk",
    }


@unittest.mock.patch(
    "mlflow.projects.run",
    return_value=FakeSubmittedRun(),
)
def test_request_to_start_slurm_run_through_ssh(
    mock_mlflow_run, client, zipped_unicore_content, sample_ssh_run_data
):
    headers = {"Authorization": "Bearer test-valid-token"}
    response = client.post(
        f"{api.SSH_SUBMIT_PATH}/0",
        data=sample_ssh_run_data,
        files={"mlproject_zip": zipped_unicore_content.read()},
        headers=headers,
    )

    assert response.status_code == 201, response.text

    expected_json = {
        "experiment_id": 0,
        "run_id": str(TEST_UUID),
        "job_id": "1",
    }
    assert response.json() == expected_json


@unittest.mock.patch(
    "mlflow.projects.run",
    return_value=FakeSubmittedRun(),
)
def test_ssh_run_authentication_exception(
    mock_mlflow_run, client, zipped_unicore_content, sample_ssh_run_data
):
    headers = {"Authorization": "Bearer test-valid-token"}

    mock_mlflow_run.side_effect = ssh_exceptions.AuthenticationFailedException(
        "Authentication went wrong"
    )

    response = client.post(
        f"{api.SSH_SUBMIT_PATH}/0",
        data=sample_ssh_run_data,
        files={"mlproject_zip": zipped_unicore_content.read()},
        headers=headers,
    )
    assert response.status_code == 401, response.text
    assert response.json() == {
        "message": "SSH authentication error. Cause: Authentication went wrong"
    }


@unittest.mock.patch(
    "mlflow.projects.run",
    return_value=FakeSubmittedRun(),
)
def test_ssh_general_exception(
    mock_mlflow_run, client, zipped_unicore_content, sample_ssh_run_data
):
    headers = {"Authorization": "Bearer test-valid-token"}

    mock_mlflow_run.side_effect = ssh_exceptions.SSHError(
        "Something else went wrong"
    )

    response = client.post(
        f"{api.SSH_SUBMIT_PATH}/0",
        data=sample_ssh_run_data,
        files={"mlproject_zip": zipped_unicore_content.read()},
        headers=headers,
    )
    assert response.status_code == 400, response.text
    assert response.json() == {
        "message": "SSH backend error. Cause: Something else went wrong"
    }
