import uuid

import click

import mantik.cli._callbacks as _callbacks
import mantik.utils.env_vars as env_vars


VERBOSE = click.option(
    "--verbose",
    "-v",
    is_flag=True,
    callback=_callbacks.set_verbose_logging,
    help="Set logging to verbose mode.",
)

PROJECT_ID = click.option(
    "--project-id",
    type=uuid.UUID,
    required=True,
    envvar=env_vars.PROJECT_ID_ENV_VAR,
    help=f"""Project ID on Mantik.

    If not specified, it is inferred from the environment variable
{env_vars.PROJECT_ID_ENV_VAR}.
    """,
)

MODEL_ID = click.option(
    "--model-id",
    type=uuid.UUID,
    required=True,
    envvar=env_vars.MODEL_ID_ENV_VAR,
    help=f"""Model ID on Mantik.

        If not specified, it is inferred from the environment variable
{env_vars.MODEL_ID_ENV_VAR}.""",
)


def get_connection_id(required: bool):
    return click.option(
        "--connection-id",
        required=required,
        default=None,
        type=uuid.UUID,
        envvar=env_vars.CONNECTION_ID_ENV_VAR,
        help=f"""Connection ID on Mantik.

    If not specified, it is inferred from the environment variable
{env_vars.CONNECTION_ID_ENV_VAR}.""",
    )


EXPERIMENT_REPOSITORY_ID = click.option(
    "--experiment-repository-id",
    required=True,
    type=uuid.UUID,
    envvar=env_vars.EXPERIMENT_REPOSITORY_ID_ENV_VAR,
    help=f"""Experiment Repository ID on Mantik.

    If not specified, it is inferred from the environment variable
{env_vars.EXPERIMENT_REPOSITORY_ID_ENV_VAR}.""",
)

DATA_REPOSITORY_ID = click.option(
    "--data-repository-id",
    type=uuid.UUID,
    required=True,
    envvar=env_vars.DATA_REPOSITORY_ID_ENV_VAR,
    help=f"""Data Repository ID on Mantik.

    If not specified, it is inferred from the environment variable
{env_vars.DATA_REPOSITORY_ID_ENV_VAR}.""",
)

DATA_REPOSITORY_ID_OPTIONAL = click.option(
    "--data-repository-id",
    type=uuid.UUID,
    required=False,
    envvar=env_vars.DATA_REPOSITORY_ID_ENV_VAR,
    help=f"""Data Repository ID on Mantik.

    If not specified, it is inferred from the environment variable
{env_vars.DATA_REPOSITORY_ID_ENV_VAR}.""",
)

CODE_REPOSITORY_ID = click.option(
    "--code-repository-id",
    required=True,
    type=uuid.UUID,
    envvar=env_vars.CODE_REPOSITORY_ID_ENV_VAR,
    help=f"""Code Repository ID on Mantik.

    If not specified, it is inferred from the environment variable
{env_vars.CODE_REPOSITORY_ID_ENV_VAR}.""",
)


def get_run_id(required: bool):
    return click.option(
        "--run-id",
        required=required,
        default=None,
        type=uuid.UUID,
        envvar=env_vars.RUN_ID_ENV_VAR,
        help=f"""Run ID on Mantik.

    If not specified, it is inferred from the environment variable
{env_vars.RUN_ID_ENV_VAR}.""",
    )


def get_target_dir_option(help_option: str):
    return click.option(
        "--target-dir",
        type=click.Path(path_type=str, exists=True),
        default="./",
        help=help_option,
        show_default=True,
    )


DATA_TARGET_DIR = click.option(
    "--data-target-dir",
    type=click.Path(path_type=str),
    default="data",
    help="Relative path to directory where the data will be stored (from code root)",  # noqa E501
    show_default=True,
    envvar=env_vars.TARGET_DIR_ENV_VAR,
)


def get_target_dir_option_required(help_option: str):
    return click.option(
        "--target-dir",
        type=click.Path(path_type=str),
        help=help_option,
        required=True,
        envvar=env_vars.TARGET_DIR_ENV_VAR,
    )


def get_name_option(required: bool, help_option: str):
    return click.option(
        "--name",
        required=required,
        default=None,
        type=str,
        help=help_option,
    )
