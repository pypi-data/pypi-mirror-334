import pathlib
import typing as t
import uuid

import click

import mantik.cli._options as _options
import mantik.cli.main as main
import mantik.cli.utils as cli_utils
import mantik.data_repository.data_repository as data_repository
import mantik.utils

GROUP_NAME = "data"


@main.cli.group(GROUP_NAME)
def cli() -> None:
    """Interaction with data through the mantik api."""


@cli.command("download")
@_options.PROJECT_ID
@_options.DATA_REPOSITORY_ID
@click.option(
    "--commit",
    required=False,
    type=str,
    help="Commit hash to checkout. Takes precedence over branch.",
    envvar=mantik.utils.env_vars.DATA_REPOSITORY_COMMIT_ENV_VAR,
    default=None,
)
@click.option(
    "--branch",
    required=False,
    type=str,
    help="Branch to checkout. Defaults main branch.",
    envvar=mantik.utils.env_vars.DATA_REPOSITORY_BRANCH_ENV_VAR,
    default=None,
)
@_options.get_target_dir_option_required(
    help_option="Path to directory where the data will be stored.",
)
def download_data_repository(
    project_id: uuid.UUID,
    data_repository_id: uuid.UUID,
    commit: t.Optional[str],
    branch: t.Optional[str],
    target_dir: str,
) -> None:
    """Download data repository."""
    output = data_repository.download_data_repository(
        project_id=project_id,
        data_repository_id=data_repository_id,
        checkout=commit or branch,
        target_dir=pathlib.Path(target_dir),
        token=cli_utils.access_token_from_env_vars(),
    )
    click.echo(output)
