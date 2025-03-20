import uuid

import click.testing
import pytest

import mantik.cli.main as main


@pytest.mark.parametrize("unzip", ["--unzip", "--no-unzip"])
def test_download_artifacts_cli(
    mock_authentication,
    tmpdir,
    mock_get_artifacts_url,
    mock_get_url,
    info_caplog,
    unzip,
    zipped_file_name,
):
    runner = click.testing.CliRunner()
    with mock_get_artifacts_url as get_artifacts_url, mock_get_url as get_url:
        result = runner.invoke(
            main.cli,
            [
                "runs",
                "download-artifacts",
                "--project-id",
                str(uuid.uuid4()),
                "--run-id",
                str(uuid.uuid4()),
                "--target-dir",
                tmpdir,
                unzip,
            ],
        )
        get_artifacts_url.assert_called()
        get_url.assert_called()

        assert result.exit_code == 0, result.output
