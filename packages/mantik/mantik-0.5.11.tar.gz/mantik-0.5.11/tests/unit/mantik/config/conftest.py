import os
import pathlib

import pytest

import mantik.config as config
import mantik.utils as utils
import mantik.utils.credentials as _credentials

FILE_DIR = pathlib.Path(__file__).parent


@pytest.fixture
def required_config_env_vars():
    return {
        _credentials.UNICORE_USERNAME_ENV_VAR: "test-user",
        _credentials.UNICORE_PASSWORD_ENV_VAR: "test-password",
        config.core.COMPUTE_BUDGET_ACCOUNT_ENV_VAR: "test-project",
    }


@pytest.fixture(scope="session")
def mlproject_path() -> pathlib.Path:
    return (
        pathlib.Path(__file__).parent
        / "../../../../tests/resources/test-project"
    )


@pytest.fixture(scope="session")
def invalid_config_type() -> pathlib.Path:
    return (
        pathlib.Path(__file__).parent
        / "../../../../tests/resources/broken-project/compute-backend-config.md"  # noqa: E501
    )


@pytest.fixture(scope="session")
def config_with_errors() -> pathlib.Path:
    return (
        pathlib.Path(__file__).parent / "../../../../tests/resources/"
        "test-project/config-with-errors.yaml"
    )


@pytest.fixture(scope="session")
def compute_backend_config_yaml(mlproject_path) -> pathlib.Path:
    """Return the UNICORE config in YAML format.

    Doesn't contain. `Environment` section

    """
    return pathlib.Path(f"{str(mlproject_path)}/compute-backend-config.yaml")


@pytest.fixture(scope="session")
def compute_backend_config_json(mlproject_path) -> pathlib.Path:
    return pathlib.Path(f"{str(mlproject_path)}/compute-backend-config.json")


@pytest.fixture()
def unset_tracking_token_env_var_before_execution():
    if utils.mlflow.TRACKING_TOKEN_ENV_VAR in os.environ:
        del os.environ[utils.mlflow.TRACKING_TOKEN_ENV_VAR]


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
        exclude=["*.py", "*.sif"],
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
            )
        ),
        resources=config.resources.Resources(queue="batch"),
        exclude=["*.sif"],
    )
