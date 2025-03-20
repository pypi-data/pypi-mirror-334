import logging
import pathlib
import typing as t
import uuid

import click

import mantik.cli._options as main_options
import mantik.cli.runs._options as _options
import mantik.cli.runs.runs as runs
import mantik.cli.utils as utils
import mantik.runs.local as local_runs
import mantik.utils

logger = logging.getLogger(__name__)


@runs.cli.command("local")
@_options.MLPROJECT_PATH
@main_options.get_name_option(required=True, help_option="Name of the Run.")
@_options.ENTRY_POINT
@main_options.PROJECT_ID
@main_options.DATA_REPOSITORY_ID_OPTIONAL
@main_options.DATA_TARGET_DIR
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
    "--env-manager",
    type=str,
    default="local",
    help="Determines what environment manager is used for installing"
    " dependencies during runs (local, virtualenv or conda).",
)
@_options.PARAMETER
@main_options.VERBOSE
def run_project(
    name: str,
    mlproject_path: pathlib.Path,
    entry_point: str,
    parameter: t.List[str],
    verbose: bool,  # noqa
    project_id: uuid.UUID,
    data_repository_id: t.Optional[uuid.UUID],
    data_target_dir: t.Optional[str],
    data_branch: t.Optional[str],
    data_commit: t.Optional[str],
    experiment_repository_id: uuid.UUID,
    code_repository_id: uuid.UUID,
    branch: t.Optional[str],
    commit: t.Optional[str],
    env_manager: t.Optional[str],
) -> None:
    """Run an MLflow project locally and save the results in Mantik API

    Note that `MLPROJECT_PATH` is the relative path to the MLflow project file
    with your Code Repository as root.

    Remember that when you execute a run, the code is retrieved from your
    remote Git Code Repository. So make sure to commit and push your
    changes before executing a run!

    To find the respective required IDs make sure to check Mantik's UI

    """

    _options.check_commit_or_branch(branch=branch, commit=commit, logger=logger)

    logger.debug("Parsing MLflow entry point parameters")
    parameters = utils.dict_from_list(parameter)

    local_runs.start_local_run(
        project_id=project_id,
        name=name,
        experiment_repository_id=experiment_repository_id,
        data_repository_id=data_repository_id,
        code_repository_id=code_repository_id,
        branch=branch,
        commit=commit,
        data_branch=data_branch,
        data_commit=data_commit,
        mlflow_mlproject_file_path=mlproject_path.as_posix(),
        entry_point=entry_point,
        mlflow_parameters=parameters,
        data_target_dir=data_target_dir,
        env_manager=env_manager,
    )
    click.echo("Done!")
