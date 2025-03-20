import pathlib
import typing as t

import click

MLPROJECT_PATH = click.argument(
    "mlproject-path",
    type=click.Path(path_type=pathlib.Path),
    required=True,
)

ENTRY_POINT = click.option(
    "--entry-point",
    required=False,
    default="main",
    show_default=True,
    help="Entrypoint of the MLproject file.",
)

BRANCH = click.option(
    "--branch",
    default=None,
    type=str,
    help="Name of the code repository's branch you want to use for this run",
    required=True,
)

COMMIT = click.option(
    "--commit",
    default=None,
    type=str,
    help="""Name of the code repository's full commit hash you want to use for
        this run.

        If both branch and commit hash are given, the commit hash is preferred
        over the branch.
    """,
    required=False,
)

PARAMETER = click.option(
    "--parameter", "-P", show_default=True, default=lambda: [], multiple=True
)


def check_commit_or_branch(
    branch: t.Optional[str], commit: t.Optional[str], logger
):
    if branch is None and commit is None:
        raise ValueError(
            "Either provide a branch or full commit hash to submit"
        )
    elif branch is not None and commit is not None:
        logger.warning(
            "Both branch name %s and commit hash %s given, using commit hash to"
            " submit run",
            branch,
            commit,
        )
