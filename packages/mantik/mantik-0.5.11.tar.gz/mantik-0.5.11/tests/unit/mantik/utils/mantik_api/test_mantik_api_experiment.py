import pytest
import requests

import mantik.utils.mantik_api.experiment_repository as experiment_api


@pytest.mark.parametrize(
    ("status_code", "expected"), [(200, None), (404, requests.HTTPError())]
)
def test_get_experiment(
    mock_mantik_api_request,
    info_caplog,
    status_code,
    expected,
    sample_experiment_repository_id,
    sample_experiment_repository,
    project_id,
):
    sample_schema = sample_experiment_repository.to_json()

    with mock_mantik_api_request(
        method="GET",
        end_point=f"/projects/{str(project_id)}/"
        f"experiments/{str(sample_experiment_repository_id)}",
        status_code=status_code,
        json_response=sample_schema,
        expected_error=expected,
    ) as (m, error):
        retrieved_model = experiment_api.get_one(
            project_id=project_id,
            experiment_repository_id=sample_experiment_repository_id,
            token="test_token",
        )
        assert retrieved_model == experiment_api.ExperimentRepository.from_json(
            sample_schema
        )
    if error:
        assert any(
            "Call to Mantik API" in message for message in info_caplog.messages
        )


def test_get_unique_run_name(
    mock_mantik_api_request,
    info_caplog,
    sample_experiment_repository_id,
    project_id,
):
    with mock_mantik_api_request(
        method="GET",
        end_point=f"/projects/{str(project_id)}/"
        f"experiments/{str(sample_experiment_repository_id)}/unique-mlflow-run-name",  # noqa
        status_code=200,
        json_response="unique-name",
    ) as (m, error):
        response = experiment_api.get_unique_run_name(
            project_id=project_id,
            experiment_repository_id=sample_experiment_repository_id,
            token="test_token",
            run_name="unique-name",
        )
        assert response == "unique-name"
