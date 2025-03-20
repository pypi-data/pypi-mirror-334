import uuid

import click.testing
import pytest

import mantik.cli.main as main
import mantik.config.core as core
import mantik.testing.token as testing_token
import mantik.utils as utils
import mantik.utils.env_vars as env_vars
import mantik.utils.mantik_api.credentials as _credentials

TEST_MLFLOW_TRACKING_URI = "https://tracking.test-uri.com"
TEST_COMPUTE_BACKEND_URL = "https://compute.test-uri.com"

ENV_VARS = {
    utils.credentials.UNICORE_USERNAME_ENV_VAR: "test-user",
    utils.credentials.UNICORE_PASSWORD_ENV_VAR: "test-password",
    core.COMPUTE_BUDGET_ACCOUNT_ENV_VAR: "test-project",
    utils.mlflow.TRACKING_URI_ENV_VAR: TEST_MLFLOW_TRACKING_URI,
    utils.mlflow.EXPERIMENT_ID_ENV_VAR: "0",
    utils.mlflow.TRACKING_TOKEN_ENV_VAR: "test-token",
    _credentials._MANTIK_USERNAME_ENV_VAR: "mantik-user",
    _credentials._MANTIK_PASSWORD_ENV_VAR: "matik_password",
    env_vars.DATA_REPOSITORY_ID_ENV_VAR: str(uuid.uuid4()),
    env_vars.EXPERIMENT_REPOSITORY_ID_ENV_VAR: str(uuid.uuid4()),
    env_vars.CODE_REPOSITORY_ID_ENV_VAR: str(uuid.uuid4()),
}

SUCCESS_JSON_RESPONSE = {
    "runId": "25d2dad9-dfe2-4971-ad95-b3a9dc363700",
    "timestamp": None,
}


SUCCESS_JSON_RESPONSE_STR = (
    '{"runId": "25d2dad9-dfe2-4971-ad95-b3a9dc363700", "timestamp": null}\n'
)


@testing_token.set_token()
@pytest.mark.parametrize(
    ("cli_args", "expected_exit_code", "expected_output"),
    [
        (
            [
                "--name=test-run",
                "--backend-config=compute-backend-config.json",
                "--branch=main",
                "--entry-point=main",
            ],
            0,
            SUCCESS_JSON_RESPONSE_STR,
        ),
        (
            [
                "--name=test-run",
                "--backend-config=compute-backend-config.json",
                "--branch=main",
                "--entry-point=main",
                "-P a=99",
                "-P b=hello",
            ],
            0,
            SUCCESS_JSON_RESPONSE_STR,
        ),
        ([], 2, "Usage: cli runs submit [OPTIONS] MLPROJECT_PATH\n"),
    ],
)
def test_run_project(
    cli_args,
    expected_exit_code,
    expected_output,
    example_project_absolute_path,
    example_project_relative_path,
    mock_mantik_api_request,
    project_id,
    monkeypatch,
):
    monkeypatch.chdir(example_project_absolute_path)
    with mock_mantik_api_request(
        method="POST",
        end_point=f"/projects/{project_id}/runs",
        status_code=201,
        json_response=SUCCESS_JSON_RESPONSE,
    ) as (m, error):
        with utils.env.env_vars_set(ENV_VARS):
            runner = click.testing.CliRunner()
            result = runner.invoke(
                main.cli,
                [
                    "runs",
                    "submit",
                    example_project_relative_path,
                    *cli_args,
                    f"--project-id={project_id}",
                    f"--connection-id={uuid.uuid4()}",
                ],
            )
        assert result.exit_code == expected_exit_code, result.output
        assert expected_output in result.output


@testing_token.set_token()
def test_run_project_with_absolute_path_for_backend_config(
    example_project_absolute_path,
    example_project_relative_path,
    mock_mantik_api_request,
    project_id,
):
    cli_args = [
        example_project_relative_path,
        f"--backend-config={example_project_absolute_path}/compute-backend-config.json",  # noqa E501
        "--name=test-run",
        "--branch=main",
        f"--connection-id={uuid.uuid4()}",
    ]
    with mock_mantik_api_request(
        method="POST",
        end_point=f"/projects/{project_id}/runs",
        status_code=201,
        json_response=SUCCESS_JSON_RESPONSE,
    ) as (m, error):
        with utils.env.env_vars_set(ENV_VARS):
            runner = click.testing.CliRunner()
            result = runner.invoke(
                main.cli,
                ["runs", "submit", *cli_args, f"--project-id={project_id}"],
            )

        assert result.exit_code == 0, result.output
        assert result.output == SUCCESS_JSON_RESPONSE_STR


@testing_token.set_token()
def test_run_project_with_set_log_level(
    example_project_relative_path,
    example_project_absolute_path,
    caplog,
    mock_mantik_api_request,
    project_id,
):
    with mock_mantik_api_request(
        method="POST",
        end_point=f"/projects/{project_id}/runs",
        status_code=201,
        json_response=SUCCESS_JSON_RESPONSE,
    ) as (m, error):
        with utils.env.env_vars_set(ENV_VARS):
            runner = click.testing.CliRunner()
            _ = runner.invoke(
                main.cli,
                [
                    "runs",
                    "submit",
                    example_project_relative_path,
                    f"--backend-config={example_project_absolute_path}/compute-backend-config.json",  # noqa: E501
                    "--verbose",
                    "--name=test-run",
                    "--branch=main",
                    f"--connection-id={str(uuid.uuid4())}",
                ],
            )
            assert any("DEBUG" in m for m in caplog.messages)
