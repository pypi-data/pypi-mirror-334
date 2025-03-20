import os
import pathlib
import unittest.mock
import uuid

import click.testing
import pytest

import mantik.cli.data
import mantik.cli.main as main
import mantik.data_repository.data_repository


GROUP_NAME = mantik.cli.data.data.GROUP_NAME


@pytest.fixture
def cli_test_runner():
    yield click.testing.CliRunner()


@pytest.fixture(scope="function")
def sample_project_uuid():
    return uuid.uuid4()


@pytest.fixture(scope="function")
def mocked_token(mock_authentication):
    return mock_authentication


@pytest.fixture(scope="function")
def sample_data_repository_uuid():
    return uuid.uuid4()


@pytest.fixture(scope="function")
def sample_target_dir() -> str:
    return "/sample/target/dir"


@pytest.fixture(scope="function")
def sample_version() -> str:
    return "1234"


@pytest.fixture
def mock_project_id_env_var(sample_uuid_str):
    os.environ[mantik.utils.env_vars.PROJECT_ID_ENV_VAR] = sample_uuid_str
    yield
    os.unsetenv(mantik.utils.env_vars.PROJECT_ID_ENV_VAR)


def test_download_data_repository(
    mocked_token,
    cli_test_runner,
    sample_project_uuid,
    sample_data_repository_uuid,
    sample_target_dir,
    sample_version,
):
    with unittest.mock.patch(
        "mantik.data_repository.data_repository.download_data_repository"
    ) as mocked_function:
        result = cli_test_runner.invoke(
            main.cli,
            [
                GROUP_NAME,
                "download",
                "--project-id",
                str(sample_project_uuid),
                "--data-repository-id",
                str(sample_data_repository_uuid),
                "--branch",
                sample_version,
                "--target-dir",
                sample_target_dir,
            ],
        )
        assert result.exit_code == 0
        mocked_function.assert_called_once_with(
            project_id=sample_project_uuid,
            data_repository_id=sample_data_repository_uuid,
            checkout=sample_version,
            target_dir=pathlib.Path(sample_target_dir),
            token=mocked_token,
        )
