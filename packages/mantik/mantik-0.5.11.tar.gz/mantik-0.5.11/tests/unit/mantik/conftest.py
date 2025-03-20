import io
import os
import pathlib
import unittest.mock
import uuid
import zipfile

import pytest
import responses

import mantik.runs.schemas as run_schemas
import mantik.utils.mantik_api.client as mantik_api
import mantik.utils.mantik_api.code_repository as code_api
import mantik.utils.mantik_api.connection as connection
import mantik.utils.mantik_api.experiment_repository as experiment_api
import mantik.utils.mantik_api.user as user


FAKE_API_URL = "https://fake.com"


@pytest.fixture(scope="session")
def sample_experiment_repository_id():
    return uuid.uuid4()


@pytest.fixture(scope="session")
def sample_code_repository_id():
    return uuid.uuid4()


@pytest.fixture(scope="session")
def sample_project_id() -> uuid.UUID:
    return uuid.uuid4()


@pytest.fixture()
def sample_experiment_repository(sample_experiment_repository_id):
    return experiment_api.ExperimentRepository(
        experiment_repository_id=sample_experiment_repository_id,
        mlflow_experiment_id="123",
        name="Name",
        artifact_location="somewhere.com",
    )


@pytest.fixture(scope="session")
def sample_connection_uuid():
    return uuid.uuid4()


@pytest.fixture()
def sample_code_repository(sample_code_repository_id, sample_connection_uuid):
    return code_api.CodeRepository(
        code_repository_id=sample_code_repository_id,
        code_repository_name="Name",
        uri="some/uri.git",
        connection_id=None,
        platform="GitHub",
    )


@pytest.fixture()
def sample_code_repository_with_git_connection(
    sample_code_repository_id, fake_git_connection
):
    return code_api.CodeRepository(
        code_repository_id=sample_code_repository_id,
        code_repository_name="Name",
        uri="some/uri.git",
        connection_id=str(fake_git_connection.connection_id),
        platform="GitHub",
    )


@pytest.fixture()
def fake_git_connection(sample_connection_uuid):
    return connection.Connection(
        connection_id=sample_connection_uuid,
        user=user.User(
            user_id=uuid.UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"),
            name="test-name",
        ),
        connection_name="git access key",
        connection_provider="GitHub",
        auth_method="token",
        token="auth-122434",
    )


@pytest.fixture(scope="session")
def sample_project_uuid():
    return uuid.uuid4()


@pytest.fixture
def mock_mantik_api_url():
    os.environ[mantik_api._MANTIK_API_URL_ENV_VAR] = FAKE_API_URL
    yield
    os.unsetenv(mantik_api._MANTIK_API_URL_ENV_VAR)


@pytest.fixture
def mock_code_git_connection_response(
    sample_project_uuid,
    fake_user_id_str,
    sample_connection_uuid,
    mock_mantik_api_url,
):
    responses.add(
        responses.GET,
        url=f"{FAKE_API_URL}/users/{fake_user_id_str}/settings/"
        f"connections/{str(sample_connection_uuid)}",
        status=200,
        json={
            "connectionId": str(sample_connection_uuid),
            "user": {"userId": fake_user_id_str, "name": "Kiwi"},
            "connectionName": "KiwiConnection",
            "connectionProvider": "GitHub",
            "authMethod": "Token",
            "token": "token",
        },
    )
    yield


@pytest.fixture()
def mock_get_git_connection(mocker, fake_git_connection):
    with mocker.patch(
        "mantik.utils.mantik_api.connection.get",
        return_value=fake_git_connection,
    ):
        yield


@pytest.fixture()
def mock_get_user_id_from_token(mocker, fake_user_id_str):
    with mocker.patch(
        "mantik.authentication.tokens.get_user_id_from_token",
        return_value=fake_user_id_str,
    ):
        yield


@pytest.fixture(scope="session")
def fake_user_id_str():
    return str(uuid.uuid4())


@pytest.fixture(scope="session")
def sample_run_configuration(
    sample_experiment_repository_id, sample_code_repository_id
) -> run_schemas.RunConfiguration:
    return run_schemas.RunConfiguration(
        name="Sample",
        experiment_repository_id=sample_experiment_repository_id,
        code_repository_id=sample_code_repository_id,
        branch="branch",
        commit="commit",
        data_repository_id=uuid.uuid4(),
        mlflow_mlproject_file_path="some/path/MLProject",
        entry_point="main",
        mlflow_parameters={"output": "hello world"},
        backend_config={},
    )


@pytest.fixture()
def fake_token():
    return "1234"


@pytest.fixture
def resource():
    return (
        pathlib.Path(__file__).parent.parent.parent
        / "resources/test-project/MLproject"
    )


@pytest.fixture
def mock_get_artifacts_url():
    yield unittest.mock.patch(
        "mantik.utils.mantik_api.run.get_download_artifact_url",
        return_value="https://fake/url/artifacts.zip?yada&&yada",
    )


@pytest.fixture
def zipped_file_name():
    return "test_file_name"


@pytest.fixture
def zipped_file_bytes(tmpdir, zipped_file_name, resource):
    def create_zip(input_file, output_zip):
        with zipfile.ZipFile(output_zip, "w") as zipf:
            zipf.write(input_file)
        with open(output_zip, "rb") as zip_file:
            byte_stream = io.BytesIO(zip_file.read())
        return byte_stream

    return create_zip(resource, tmpdir / zipped_file_name)


@pytest.fixture
def mock_get_url(zipped_file_bytes):
    yield unittest.mock.patch("requests.get", return_value=zipped_file_bytes)


@pytest.fixture
def mock_authentication():
    with unittest.mock.patch(
        "mantik.authentication.auth.get_valid_access_token",
        return_value="1234-token",
    ):
        yield "1234-token"


@pytest.fixture()
def mock_get_code(mocker, sample_code_repository):
    mocker.patch(
        "mantik.utils.mantik_api.code_repository.get_one",
        return_value=sample_code_repository,
    )
    yield


@pytest.fixture()
def mock_get_code_from_private_repo(
    mocker, sample_code_repository_with_git_connection
):
    mocker.patch(
        "mantik.utils.mantik_api.code_repository.get_one",
        return_value=sample_code_repository_with_git_connection,
    )
    yield


@pytest.fixture()
def mock_get_experiment(mocker, sample_experiment_repository):
    mocker.patch(
        "mantik.utils.mantik_api.experiment_repository.get_one",
        return_value=sample_experiment_repository,
    )
    yield


@pytest.fixture()
def mock_get_unique_run_name(mocker, sample_run_configuration):
    mocker.patch(
        "mantik.utils.mantik_api.experiment_repository.get_unique_run_name",
        return_value=sample_run_configuration.name,
    )
    yield


@pytest.fixture()
def mock_update_run_status():
    with unittest.mock.patch(
        "mantik.utils.mantik_api.run.update_run_status",
    ) as patch:
        yield patch


@pytest.fixture()
def mock_update_run_logs():
    with unittest.mock.patch(
        "mantik.utils.mantik_api.run.update_logs",
    ) as patch:
        yield patch
