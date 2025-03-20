import uuid

import pytest
import responses

import mantik
import mantik.utils.env as env
import mantik.utils.env_vars as env_vars
import mantik.utils.mantik_api.client as mantik_api_client


@pytest.fixture(scope="session")
def sample_project_id():
    return str(uuid.uuid4())


@pytest.fixture(scope="session")
def sample_run_id():
    return str(uuid.uuid4())


@pytest.fixture(scope="function")
def mock_init_environment(
    sample_run_id, sample_project_id, mantik_api_url
) -> None:
    with env.env_vars_overwrite_temporarily(
        {
            mantik_api_client._MANTIK_API_URL_ENV_VAR: mantik_api_url,
            env_vars.MANTIK_ACCESS_TOKEN_ENV_VAR: "1234",
            env_vars.PROJECT_ID_ENV_VAR: sample_project_id,
            env_vars.MLFLOW_RUN_ID_ENV_VAR: sample_run_id,
        }
    ):
        yield


@pytest.fixture
def mock_bookkeep_infrastructure_api_request(
    mantik_api_url, sample_project_id, sample_run_id
):
    url = (
        f"{mantik_api_url}/projects/{sample_project_id}"
        f"/runs/{sample_run_id}/infrastructure"
    )
    responses.add(
        method="PUT",
        url=url,
        status=200,
    )
    yield url


@responses.activate
def test_init_with_correct_environment_setup_bookkeeps_infrastructure(
    mock_bookkeep_infrastructure_api_request,
    mock_init_environment,
) -> None:
    """
    Given I have project id, run id and in the environment
    When  I call the `mantik.init()` function
    Then  my infrastructure gets bookkept
    And   it gets bookkept on the correct project and run
    """
    mantik.init()
    responses.assert_call_count(
        url=mock_bookkeep_infrastructure_api_request, count=1
    )


def test_init_without_environment_setup_returns_errors() -> None:
    """
    Given I don't have project/run ids in the environment
    When  I call the `mantik.init()` function
    Then  my code crashes
    """
    with pytest.raises(RuntimeError):
        mantik.init()
