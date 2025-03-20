import logging
import os
import unittest.mock
import uuid

import click.testing
import pytest

import mantik.cli.main as main
import mantik.cli.models.models

GROUP_NAME = mantik.cli.models.models.GROUP_NAME

SAMPLE_UUID = uuid.uuid4()


@pytest.fixture
def sample_uuid_str() -> str:
    return str(SAMPLE_UUID)


@pytest.fixture
def mock_project_id_env_var(sample_uuid_str):
    os.environ[mantik.utils.env_vars.PROJECT_ID_ENV_VAR] = sample_uuid_str
    yield
    os.unsetenv(mantik.utils.env_vars.PROJECT_ID_ENV_VAR)


@pytest.fixture
def cli_test_runner():
    yield click.testing.CliRunner()


def test_get_all_project_models(
    mock_authentication, cli_test_runner, sample_uuid_str
):
    with unittest.mock.patch(
        "mantik.utils.mantik_api.models.get_all"
    ) as mocked_function:
        result = cli_test_runner.invoke(
            main.cli,
            [GROUP_NAME, "list", "--project-id", sample_uuid_str],
        )
        assert result.exit_code == 0
        mocked_function.assert_called()


def test_get_model(mock_authentication, cli_test_runner, sample_uuid_str):
    with unittest.mock.patch(
        "mantik.utils.mantik_api.models.get_one"
    ) as mocked_function:
        result = cli_test_runner.invoke(
            main.cli,
            [
                GROUP_NAME,
                "get-one",
                "--model-id",
                sample_uuid_str,
                "--project-id",
                sample_uuid_str,
            ],
        )
        assert result.exit_code == 0
        mocked_function.assert_called()


def test_delete_model(
    mock_authentication,
    mock_project_id_env_var,
    cli_test_runner,
    sample_uuid_str,
):
    with unittest.mock.patch(
        "mantik.utils.mantik_api.models.delete"
    ) as mocked_function:
        result = cli_test_runner.invoke(
            main.cli,
            [GROUP_NAME, "delete", "--model-id", sample_uuid_str],
        )
        assert result.exit_code == 0
        mocked_function.assert_called()


def test_create_model_entry(
    mock_authentication, cli_test_runner, sample_uuid_str
):
    with unittest.mock.patch(
        "mantik.utils.mantik_api.models.add"
    ) as mocked_function:
        result = cli_test_runner.invoke(
            main.cli,
            [
                GROUP_NAME,
                "add",
                "--project-id",
                sample_uuid_str,
                "--uri",
                "URI",
                "--location",
                "something://somewhere.com",
                "--name",
                "new-name",
            ],
        )
        assert result.exit_code == 0
        mocked_function.assert_called()


def test_update_model_entry(
    mock_authentication, cli_test_runner, sample_uuid_str
):
    with unittest.mock.patch(
        "mantik.utils.mantik_api.models.update"
    ) as mocked_function:
        result = cli_test_runner.invoke(
            main.cli,
            [
                GROUP_NAME,
                "update",
                "--project-id",
                sample_uuid_str,
                "--model-id",
                sample_uuid_str,
                "--uri",
                "URI",
                "--location",
                "something://somewhere.com",
                "--name",
                "new-name",
            ],
        )
        assert result.exit_code == 0
        mocked_function.assert_called()


@pytest.mark.parametrize(
    "mlflow_params,expected",
    [
        ('{"hello":"world"}', {"hello": "world"}),
        (None, None),
    ],
)
def test_mlflow_parameters_decoder(mlflow_params, expected):
    assert (
        mantik.cli.models.models.mlflow_parameters_decoder(
            None, None, mlflow_params
        )
        == expected
    )


def test_mlflow_parameters_decoder_raises_error_on_wrong_format():
    with pytest.raises(TypeError):
        mantik.cli.models.models.mlflow_parameters_decoder(
            None, None, "i am a broken json string"
        )


@pytest.fixture
def docker_client():
    class Client:
        class Images:
            def load(self, data):
                pass

        images = Images()

    return Client()


@pytest.fixture
def mock_get_image_url():
    yield unittest.mock.patch(
        "mantik.utils.mantik_api.models.get_image_url", return_value="test-url"
    )


@pytest.fixture
def mock_get_url():
    yield unittest.mock.patch("requests.get", return_value=[b"1", b"2", b"3"])


@pytest.fixture
def mock_docker_client(docker_client):
    yield unittest.mock.patch("docker.from_env", return_value=docker_client)


def test_download_model(
    mock_authentication,
    cli_test_runner,
    sample_uuid_str,
    tmpdir,
    mock_get_image_url,
    mock_get_url,
    caplog,
):
    caplog.set_level(logging.INFO)
    with mock_get_image_url as get_image_url, mock_get_url as get_url:
        result = cli_test_runner.invoke(
            main.cli,
            [
                GROUP_NAME,
                "download",
                "--project-id",
                sample_uuid_str,
                "--model-id",
                sample_uuid_str,
                "--target-dir",
                tmpdir,
            ],
        )
        assert result.exit_code == 0
        get_image_url.assert_called()
        get_url.assert_called()

        assert "Downloading image" in caplog.text
        assert "Image saved as zipped tarball at" in caplog.text
        assert (
            "In order to load the image into docker, "
            "you can run `docker load <"
        ) in caplog.text


def test_download_model_load(
    mock_authentication,
    cli_test_runner,
    sample_uuid_str,
    tmpdir,
    mock_get_image_url,
    mock_get_url,
    mock_docker_client,
    caplog,
):
    caplog.set_level(logging.INFO)
    with mock_get_image_url as get_image_url, mock_get_url as request, mock_docker_client as load:  # noqa E501
        result = cli_test_runner.invoke(
            main.cli,
            [
                GROUP_NAME,
                "download",
                "--project-id",
                sample_uuid_str,
                "--model-id",
                sample_uuid_str,
                "--target-dir",
                tmpdir,
                "--load",
            ],
        )
        assert result.exit_code == 0, result.output
        get_image_url.assert_called()
        request.assert_called()
        load.assert_called()

        assert "Downloading image" in caplog.text
        assert "Image saved as zipped tarball at" in caplog.text
        assert (
            "Unzipping and loading into docker. This can take a few minutes..."
            in caplog.text
        )
        assert (
            "Run 'docker images', an image named test-url should be present."
        ) in caplog.text


def test_download_model_apptainer(
    mock_authentication,
    cli_test_runner,
    sample_uuid_str,
    tmpdir,
    docker_client,
    caplog,
):
    result = cli_test_runner.invoke(
        main.cli,
        [
            GROUP_NAME,
            "download",
            "--project-id",
            sample_uuid_str,
            "--model-id",
            sample_uuid_str,
            "--target-dir",
            tmpdir,
            "--image-type",
            "apptainer",
        ],
    )
    assert result.exit_code == 1
    assert ("We are sorry, " "apptainer is not supported yet!\n") in caplog.text


def test_start_build(mock_authentication, cli_test_runner, sample_uuid_str):
    with unittest.mock.patch(
        "mantik.utils.mantik_api.models.start_build"
    ) as mocked_function:
        result = cli_test_runner.invoke(
            main.cli,
            [
                GROUP_NAME,
                "build",
                "--model-id",
                sample_uuid_str,
                "--project-id",
                sample_uuid_str,
            ],
        )
        assert result.exit_code == 0
        mocked_function.assert_called()


def test_get_build_status(
    mock_authentication, cli_test_runner, sample_uuid_str
):
    with unittest.mock.patch(
        "mantik.utils.mantik_api.models.get_one"
    ) as mocked_function:
        result = cli_test_runner.invoke(
            main.cli,
            [
                GROUP_NAME,
                "build-status",
                "--model-id",
                sample_uuid_str,
                "--project-id",
                sample_uuid_str,
            ],
        )
        assert result.exit_code == 0
        mocked_function.assert_called()
        assert ("Build Status") in result.output
