import logging
import pathlib
import typing as t
import uuid

import click

import mantik.cli._options as main_options
import mantik.cli.runs._options as _options
import mantik.cli.runs.runs as runs
import mantik.cli.utils as utils
import mantik.config.core as core
import mantik.runs.remote
import mantik.runs.schemas

logger = logging.getLogger(__name__)


@runs.cli.command("submit")
@_options.MLPROJECT_PATH
@main_options.get_name_option(required=True, help_option="Name of the Run.")
@_options.ENTRY_POINT
@click.option(
    "--backend-config",
    type=click.Path(dir_okay=False, path_type=pathlib.Path),
    required=True,
    help="Relative or absolute path to backend config file.",
)
@main_options.PROJECT_ID
@main_options.DATA_REPOSITORY_ID_OPTIONAL
@click.option(
    "--data-commit",
    required=False,
    type=str,
    help="Commit hash of data repo to checkout. Takes precedence over data-branch",  # noqa E501
    envvar=mantik.utils.env_vars.DATA_REPOSITORY_COMMIT_ENV_VAR,
    default=None,
)
@click.option(
    "--data-branch",
    required=False,
    type=str,
    help="Branch of data repo to checkout. Defaults main branch.",
    envvar=mantik.utils.env_vars.DATA_REPOSITORY_BRANCH_ENV_VAR,
    default=None,
)
@main_options.EXPERIMENT_REPOSITORY_ID
@main_options.CODE_REPOSITORY_ID
@_options.BRANCH
@_options.COMMIT
@click.option(
    "--compute-budget-account",
    type=str,
    default=None,
    help=f"""Name of your Compute Budget Account on HPC

        If not specified, it is inferred from the environment variable
        {core.COMPUTE_BUDGET_ACCOUNT_ENV_VAR}.

    """,
    envvar=core.COMPUTE_BUDGET_ACCOUNT_ENV_VAR,
)
@_options.PARAMETER
@main_options.VERBOSE
@main_options.get_connection_id(required=True)
def run_project(
    name: str,
    mlproject_path: pathlib.Path,
    entry_point: str,
    backend_config: pathlib.Path,
    parameter: t.List[str],
    verbose: bool,  # noqa
    project_id: t.Optional[uuid.UUID],
    data_repository_id: t.Optional[uuid.UUID],
    data_branch: t.Optional[str],
    data_commit: t.Optional[str],
    experiment_repository_id: t.Optional[uuid.UUID],
    code_repository_id: t.Optional[uuid.UUID],
    branch: t.Optional[str],
    commit: t.Optional[str],
    compute_budget_account: t.Optional[str],
    connection_id: t.Optional[uuid.UUID],
) -> None:
    """Submit an MLflow project as a run to the Mantik Compute Backend.

    Note that `MLPROJECT_PATH` is the relative path to the MLflow project
    folder with your Code Repository as root.

    Remember that when you submit a run, the code is retrieved from your
    remote Git Code Repository. So make sure to commit and push your
    changes before submitting a run! The only file read from your local
    system is the backend config.

    To find the respective required IDs make sure to check Mantik's UI

    """
    _options.check_commit_or_branch(branch=branch, commit=commit, logger=logger)

    logger.debug("Parsing MLflow entry point parameters")
    parameters = utils.dict_from_list(parameter)

    response = mantik.runs.remote.submit_run(
        project_id=project_id,
        name=name,
        experiment_repository_id=experiment_repository_id,
        data_repository_id=data_repository_id,
        data_branch=data_branch,
        data_commit=data_commit,
        code_repository_id=code_repository_id,
        branch=branch,
        commit=commit,
        connection_id=connection_id,
        compute_budget_account=compute_budget_account,
        mlflow_mlproject_file_path=mlproject_path.as_posix(),
        entry_point=entry_point,
        mlflow_parameters=parameters,
        backend_config=backend_config,
    )
    click.echo(response.content)
