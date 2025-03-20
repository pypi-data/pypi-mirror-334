import functools
import json
import pathlib
import uuid

import fastapi.testclient
import mlflow.projects
import pytest

import mantik.config as config
import mantik.testing as testing
import mantik.utils.unicore.zip as unicore_zip
import mantik_compute_backend
import mantik_compute_backend.settings as settings
import tokens.verifier as _verifier


@pytest.fixture(scope="function")
def client(monkeypatch) -> fastapi.testclient.TestClient:
    monkeypatch.setattr(
        _verifier,
        "TokenVerifier",
        testing.mlflow_server.FakeTokenVerifier,
    )
    app = mantik_compute_backend.app.create_app()

    return fastapi.testclient.TestClient(app)


@pytest.fixture(scope="function")
def client_suppressing_raise(monkeypatch) -> fastapi.testclient.TestClient:
    monkeypatch.setattr(
        _verifier,
        "TokenVerifier",
        testing.mlflow_server.FakeTokenVerifier,
    )
    app = mantik_compute_backend.app.create_app()

    return fastapi.testclient.TestClient(app, raise_server_exceptions=False)


@pytest.fixture(scope="function")
def client_with_small_size_limitation(
    monkeypatch,
) -> fastapi.testclient.TestClient:
    monkeypatch.setattr(
        _verifier,
        "TokenVerifier",
        testing.mlflow_server.FakeTokenVerifier,
    )
    app = mantik_compute_backend.app.create_app()

    def get_settings_override() -> settings.Settings:
        return settings.Settings(max_file_size=1)

    app.dependency_overrides[settings.get_settings] = get_settings_override

    return fastapi.testclient.TestClient(app, raise_server_exceptions=False)


@pytest.fixture
def submit_run_request_data():
    return {
        "active_run_id": str(uuid.uuid4().hex),
        "entry_point": "main",
        "mlflow_parameters": json.dumps({"foo": "bar"}),
        "hpc_api_username": "bar",
        "hpc_api_password": "bam",
        "compute_budget_account": "baz",
        "compute_backend_config": "compute-backend-config.json",
        "experiment_id": "1",
        "mlflow_tracking_uri": "foo",
        "mlflow_tracking_token": "aasdf",
    }


@pytest.fixture
def submit_ssh_run_request_data():
    return {
        "active_run_id": str(uuid.uuid4().hex),
        "entry_point": "main",
        "mlflow_parameters": json.dumps({"foo": "bar"}),
        "ssh_username": "fake user",
        "ssh_password": "baz",
        "ssh_private_key": "bam",
        "compute_backend_config": "compute-backend-config.json",
        "experiment_id": "1",
        "mlflow_tracking_uri": "foo",
        "mlflow_tracking_token": "aasdf",
    }


@pytest.fixture(scope="session")
def mlproject_path() -> pathlib.Path:
    return (
        pathlib.Path(__file__).parent / "../../../tests/resources/test-project"
    )


@pytest.fixture()
def example_project(
    mlproject_path,
) -> mlflow.projects._project_spec.Project:
    return mlflow.projects.utils.load_project(mlproject_path)


@pytest.fixture(scope="function")
def example_unicore_config() -> config.core.Config:
    return config.core.Config(
        unicore_api_url="test-url",
        user="user",
        password="password",
        project="test-project",
        environment=config.environment.Environment(
            execution=config.executable.Apptainer(
                path=pathlib.Path("mantik-test.sif"),
            ),
            variables={"SRUN_CPUS_PER_TASK": 100},
        ),
        resources=config.resources.Resources(queue="batch"),
        exclude=["*.sif"],
    )


@pytest.fixture()
def example_unicore_config_for_python() -> config.core.Config:
    return config.core.Config(
        unicore_api_url="test-url",
        user="user",
        password="password",
        project="test-project",
        environment=config.environment.Environment(
            execution=config.executable.Python(
                path=pathlib.Path("/venv"),
            ),
            pre_run_command_on_compute_node=["precommand compute node"],
            post_run_command_on_compute_node=["postcommand compute node"],
        ),
        resources=config.resources.Resources(queue="batch"),
        exclude=["*.sif"],
    )


@pytest.fixture(scope="function")
def example_firecrest_config() -> config.core.Config:
    return config.core.Config(
        firecrest=config.firecrest.Firecrest(
            api_url="test-url",
            machine="test-machine",
            token_url="test-token-url",
        ),
        user="user",
        password="password",
        project="test-project",
        environment=config.environment.Environment(
            execution=config.executable.Apptainer(
                path=pathlib.Path("mantik-test.sif"),
            )
        ),
        resources=config.resources.Resources(
            queue="batch", node_constraints="gpu"
        ),
        exclude=[],
    )


@pytest.fixture(scope="function")
def example_firecrest_config_long_resources() -> config.core.Config:
    return config.core.Config(
        firecrest=config.firecrest.Firecrest(
            api_url="test-url",
            machine="test-machine",
            token_url="test-token-url",
        ),
        user="user",
        password="password",
        project="test-project",
        environment=config.environment.Environment(
            execution=config.executable.Apptainer(
                path=pathlib.Path("mantik-test.sif"),
            )
        ),
        resources=config.resources.Resources(
            queue="batch",
            node_constraints="gpu",
            runtime="1h",
            nodes=1,
            total_cpus=1,
            cpus_per_node=1,
            gpus_per_node=1,
            memory_per_node="1",
            reservation="test-reservation",
            qos="test-qos,",
        ),
        exclude=[],
    )


@pytest.fixture()
def example_firecrest_config_for_python() -> config.core.Config:
    return config.core.Config(
        firecrest=config.firecrest.Firecrest(
            api_url="test-url",
            machine="test-machine",
            token_url="test-token-url",
        ),
        user="user",
        password="password",
        project="test-project",
        environment=config.environment.Environment(
            execution=config.executable.Python(
                path=pathlib.Path("/venv"),
            ),
            pre_run_command_on_compute_node=["precommand compute node"],
            post_run_command_on_compute_node=["postcommand compute node"],
        ),
        resources=config.resources.Resources(
            queue="batch", node_constraints="gpu"
        ),
        exclude=["*.sif"],
    )


@pytest.fixture()
def zipped_unicore_content(mlproject_path, example_unicore_config):
    return unicore_zip.zip_directory_with_exclusion(
        mlproject_path, example_unicore_config
    )


@pytest.fixture()
def zipped_firecrest_content(mlproject_path, example_firecrest_config):
    return unicore_zip.zip_directory_with_exclusion(
        mlproject_path, example_firecrest_config
    )


@pytest.fixture()
def submit_run_request_files(zipped_unicore_content):
    return {"mlproject_zip": zipped_unicore_content}


@pytest.fixture(scope="session")
def broken_mlproject_path() -> pathlib.Path:
    return pathlib.Path(__file__).parent / "../../resources/broken-project"


@pytest.fixture(scope="function")
def broken_config() -> config.core.Config:
    return config.core.Config(
        unicore_api_url="test-url",
        user="user",
        password="password",
        project="test-project",
        environment=config.environment.Environment(
            execution=config.executable.Apptainer(
                path=pathlib.Path("/mantik-test.sif"), type="remote"
            )
        ),
        resources=config.resources.Resources(queue="batch"),
        exclude=[],
    )


@pytest.fixture()
def broken_zipped_content(broken_mlproject_path, broken_config):
    return unicore_zip.zip_directory_with_exclusion(
        broken_mlproject_path, broken_config
    )


@pytest.fixture()
def example_broken_project(
    broken_mlproject_path,
) -> mlflow.projects._project_spec.Project:
    return mlflow.projects.utils.load_project(broken_mlproject_path)


@pytest.fixture()
def create_firecrest_fake_client_credentials_auth(
    login_successful: bool,
) -> functools.partial:
    return functools.partial(
        testing.firecrest.FakeClientCredentialsAuth,
        login_successful=login_successful,
    )
