import uuid

import pytest
import requests

import mantik.utils.mantik_api as mantik_api
import mantik.utils.mantik_api.connection
import mantik.utils.mantik_api.data_repository
import mantik.utils.mlflow as mlflow


@pytest.mark.parametrize(
    ("status_code", "expected"), [(200, None), (404, requests.HTTPError())]
)
def test_get_data_repositories(
    mock_mantik_api_request, info_caplog, status_code, expected
):
    project_id = uuid.uuid4()
    name = "data_repo_name"
    with mock_mantik_api_request(
        method="GET",
        end_point=f"/projects/{str(project_id)}/data",
        status_code=status_code,
        json_response={
            "totalRecords": 1,
            "dataRepositories": [
                {
                    "dataRepositoryId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "dataRepositoryName": name,
                    "uri": "string",
                    "accessToken": "string",
                    "description": "string",
                    "labels": [
                        {
                            "labelId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                            "scope": "string",
                            "name": "string",
                            "value": "string",
                        }
                    ],
                }
            ],
        },
        expected_error=expected,
    ) as (m, error):
        data_repositories = mantik.utils.mantik_api.data_repository.get_all(
            project_id=project_id, token="test_token"
        )
        assert data_repositories[0]["dataRepositoryName"] == name
    if error:
        assert any(
            "Call to Mantik API" in message for message in info_caplog.messages
        )


@pytest.mark.parametrize(
    ("status_code", "expected"), [(200, None), (404, requests.HTTPError())]
)
def test_get_connection(
    mock_mantik_api_request, info_caplog, status_code, expected
):
    user_id = uuid.uuid4()
    connection_id = uuid.uuid4()
    name = "unicore_connection"
    with mock_mantik_api_request(
        method="GET",
        end_point=f"/users/{user_id}/settings/connections/{connection_id}",  # noqa
        status_code=status_code,
        json_response={
            "connectionId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "user": {
                "userId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "name": "test-name",
                "email": "email-test",
            },
            "connectionName": name,
            "connectionProvider": "string",
            "authMethod": "string",
            "loginName": "string",
            "password": "string",
            "token": "string",
        },
        expected_error=expected,
    ) as (m, error):
        connection = mantik.utils.mantik_api.connection.get(
            user_id=user_id, connection_id=connection_id, token="test_token"
        )
        assert connection.connection_name == name
    if error:
        assert any(
            "Call to Mantik API" in message for message in info_caplog.messages
        )


@pytest.mark.parametrize(
    ("env_vars", "expected"),
    [
        (
            {
                mantik_api.client._MANTIK_API_URL_ENV_VAR: "https://api.cloud.mantik.ai"  # noqa F401
            },
            "https://api.cloud.mantik.ai",
        ),
        (
            {mlflow.TRACKING_URI_ENV_VAR: "https://tracking.cloud.mantik.ai"},
            "https://api.cloud.mantik.ai",
        ),
        ({}, mantik_api.client._DEFAULT_MANTIK_API_URL),
    ],
)
def test_get_base_url(env_vars_set, env_vars, expected):
    with env_vars_set(env_vars):
        result = mantik_api.client._get_base_url()

    assert result == expected
