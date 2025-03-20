import typing as t
import uuid

import click

import mantik.cli._options as _main_options
import mantik.cli.main as main
import mantik.cli.remote_file_service._arguments as _arguments
import mantik.remote_file_service.data_client as data_client

GROUP_NAME = "unicore-file-service"


@main.cli.group(GROUP_NAME)
def cli() -> None:
    """Interaction with the unicore file service."""


@cli.command("copy-file")
@_arguments.SOURCE
@_arguments.TARGET
@_main_options.get_connection_id(required=False)
def copy_file(
    source: str,
    target: str,
    connection_id: t.Optional[uuid.UUID],
) -> None:
    unicore_file_service = _import_unicore_file_service()
    uc_fs = data_client.DataClient.from_env(
        connection_id=connection_id,
        remote_fs_type=unicore_file_service.UnicoreFileService,
    )
    file = uc_fs.copy_file(
        source=source,
        target=target,
    )
    click.echo(file)


@cli.command("remove-file")
@_arguments.TARGET
@_main_options.get_connection_id(required=False)
def remove_file(
    target: str,
    connection_id: t.Optional[uuid.UUID],
) -> None:
    unicore_file_service = _import_unicore_file_service()
    uc_fs = data_client.DataClient.from_env(
        connection_id=connection_id,
        remote_fs_type=unicore_file_service.UnicoreFileService,
    )
    uc_fs.remove_file(target=target)
    click.echo("File removed!")


@cli.command("create-file")
@_arguments.TARGET
@_main_options.get_connection_id(required=False)
def create_file_if_not_exists_file(
    target: str,
    connection_id: t.Optional[uuid.UUID],
) -> None:
    unicore_file_service = _import_unicore_file_service()
    uc_fs = data_client.DataClient.from_env(
        connection_id=connection_id,
        remote_fs_type=unicore_file_service.UnicoreFileService,
    )
    file = uc_fs.create_file_if_not_exists(
        target=target,
    )
    click.echo(file)


@cli.command("list-directory")
@_arguments.TARGET
@_main_options.get_connection_id(required=False)
def list_directory(target: str, connection_id: t.Optional[uuid.UUID]) -> None:
    unicore_file_service = _import_unicore_file_service()
    uc_fs = data_client.DataClient.from_env(
        connection_id=connection_id,
        remote_fs_type=unicore_file_service.UnicoreFileService,
    )
    directory = uc_fs.list_directory(target=target)
    click.echo(directory)


@cli.command("create-directory")
@_arguments.TARGET
@_main_options.get_connection_id(required=False)
def create_directory(
    target: str,
    connection_id: t.Optional[uuid.UUID],
) -> None:
    unicore_file_service = _import_unicore_file_service()
    uc_fs = data_client.DataClient.from_env(
        connection_id=connection_id,
        remote_fs_type=unicore_file_service.UnicoreFileService,
    )
    directory = uc_fs.create_directory(
        target=target,
    )
    click.echo(directory)


@cli.command("remove-directory")
@_arguments.TARGET
@_main_options.get_connection_id(required=False)
def remove_directory(
    target: str,
    connection_id: t.Optional[uuid.UUID],
) -> None:
    unicore_file_service = _import_unicore_file_service()
    uc_fs = data_client.DataClient.from_env(
        connection_id=connection_id,
        remote_fs_type=unicore_file_service.UnicoreFileService,
    )
    uc_fs.remove_directory(target=target)
    click.echo("Directory removed!")


@cli.command("copy-directory")
@_arguments.SOURCE
@_arguments.TARGET
@_main_options.get_connection_id(required=False)
def copy_directory(
    source: str,
    target: str,
    connection_id: t.Optional[uuid.UUID],
) -> None:
    unicore_file_service = _import_unicore_file_service()
    uc_fs = data_client.DataClient.from_env(
        connection_id=connection_id,
        remote_fs_type=unicore_file_service.UnicoreFileService,
    )
    directory = uc_fs.copy_directory(
        source=source,
        target=target,
    )
    click.echo(directory)


@cli.command("exists")
@_arguments.TARGET
@_main_options.get_connection_id(required=False)
def exists(target: str, connection_id: t.Optional[uuid.UUID]) -> None:
    unicore_file_service = _import_unicore_file_service()
    uc_fs = data_client.DataClient.from_env(
        connection_id=connection_id,
        remote_fs_type=unicore_file_service.UnicoreFileService,
    )
    _exists = uc_fs.exists(target=target)
    click.echo(_exists)


@cli.command("user")
@_main_options.get_connection_id(required=False)
def user(connection_id: t.Optional[uuid.UUID]) -> None:
    unicore_file_service = _import_unicore_file_service()
    uc_fs = data_client.DataClient.from_env(
        connection_id=connection_id,
        remote_fs_type=unicore_file_service.UnicoreFileService,
    )
    click.echo(uc_fs.user)


def _import_unicore_file_service():
    try:
        import mantik.remote_file_service.unicore_file_service as unicore_file_service  # noqa: E501
    except ModuleNotFoundError as e:
        raise RuntimeError(
            "Extras for UNICORE file service must be "
            'installed via `pip install "mantik[unicore]"`'
        ) from e
    else:
        return unicore_file_service
