import pytest
import requests

import mantik.utils.mantik_api.code_repository as code_api


@pytest.mark.parametrize(
    ("status_code", "expected"), [(200, None), (404, requests.HTTPError())]
)
def test_get_model(
    mock_mantik_api_request,
    info_caplog,
    status_code,
    expected,
    sample_code_repository_id,
    sample_code_repository,
    project_id,
):
    sample_schema = sample_code_repository.to_json()

    with mock_mantik_api_request(
        method="GET",
        end_point=f"/projects/{str(project_id)}/"
        f"code/{str(sample_code_repository_id)}",
        status_code=status_code,
        json_response=sample_schema,
        expected_error=expected,
    ) as (m, error):
        retrieved_model = code_api.get_one(
            project_id=project_id,
            code_repository_id=sample_code_repository_id,
            token="test_token",
        )
        assert retrieved_model == code_api.CodeRepository.from_json(
            sample_schema
        )
    if error:
        assert any(
            "Call to Mantik API" in message for message in info_caplog.messages
        )
