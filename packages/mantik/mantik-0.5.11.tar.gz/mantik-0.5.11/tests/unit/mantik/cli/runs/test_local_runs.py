import unittest.mock

import click.testing
import pytest

import mantik.cli.main as main


@pytest.fixture()
def mock_runs_local_run():
    with unittest.mock.patch("mantik.runs.local.run") as _patch:
        yield _patch


@pytest.fixture()
def mock_get_valid_access_token(fake_token):
    with unittest.mock.patch(
        "mantik.authentication.auth.get_valid_access_token",
        return_value=fake_token,
    ) as _patch:
        yield _patch


def test_trigger_local_run_calls_correct_function_with_correct_arguments(
    mock_get_valid_access_token,
    mock_runs_local_run,
    sample_project_id,
    sample_run_configuration,
    fake_token,
) -> None:
    runner = click.testing.CliRunner()
    result = runner.invoke(
        main.cli,
        [
            "runs",
            "local",
            f"{sample_run_configuration.mlflow_mlproject_file_path}",
            f"--project-id={str(sample_project_id)}",
            f"--name={sample_run_configuration.name}",
            f"--entry-point={sample_run_configuration.entry_point}",
            f"--data-repository-id={str(sample_run_configuration.data_repository_id)}",  # noqa
            f"--experiment-repository-id={str(sample_run_configuration.experiment_repository_id)}",  # noqa
            "--data-target-dir=data",
            f"--code-repository-id={str(sample_run_configuration.code_repository_id)}",  # noqa
            f"--branch={sample_run_configuration.branch}",
            f"--commit={sample_run_configuration.commit}",
            '-Poutput="hello world"',
        ],
    )
    assert result.exit_code == 0
    mock_runs_local_run.assert_called_with(
        data=sample_run_configuration,
        project_id=sample_project_id,
        mantik_token=fake_token,
        data_target_dir="data",
        env_manager="local",
    )
