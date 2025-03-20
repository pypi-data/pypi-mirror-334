import pathlib

import pytest

import mantik.config

FILE_DIR = pathlib.Path(__file__).parent


@pytest.fixture(scope="function")
def example_unicore_config() -> mantik.config.core.Config:
    return mantik.config.core.Config(
        unicore_api_url="test-url",
        user="user",
        password="password",
        project="test-project",
        environment=mantik.config.environment.Environment(
            execution=mantik.config.executable.Apptainer(
                path=pathlib.Path("mantik-test.sif"),
            )
        ),
        resources=mantik.config.resources.Resources(queue="batch"),
        exclude=["*.sif"],
    )


@pytest.fixture()
def example_project_path() -> pathlib.Path:
    return FILE_DIR / "../../../resources/test-project"
