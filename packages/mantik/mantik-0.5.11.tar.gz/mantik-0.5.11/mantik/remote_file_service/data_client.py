import logging
import typing as t
import uuid

import fs.base

import mantik.authentication.auth
import mantik.remote_file_service.abstract_file_service as afs
from mantik.remote_file_service.abstract_file_service import FilePath

_PROJECT_ID_ENV_VAR = "MANTIK_PROJECT_ID"

logger = logging.getLogger(__name__)


class DataClientException(Exception):
    pass


class DataClient(afs.AbstractFileService):
    def localise_path(self, target: FilePath) -> FilePath:
        return self.file_service.localise_path(target)

    def is_remote(self, target: FilePath) -> bool:
        return self.file_service.is_remote(target)

    def _get_remote_fs(self, **nargs) -> fs.base.FS:
        return self.file_service._get_remote_fs(**nargs)

    def __init__(
        self,
        file_service: afs.AbstractFileService,
    ):
        self.access_token = mantik.authentication.auth.get_valid_access_token()
        self.file_service = file_service
        super().__init__()

    @classmethod
    def from_env(
        cls,
        connection_id: t.Optional[uuid.UUID] = None,
        remote_fs_type: t.Optional[t.Type[afs.AbstractFileService]] = None,
    ) -> "DataClient":
        if remote_fs_type is None:
            supported_types = _get_available_remote_file_systems()
            remote_fs_type_from_env = mantik.utils.env.get_required_env_var(
                afs.REMOTE_FS_TYPE_ENV_VAR
            )
            try:
                remote_fs_type = supported_types[remote_fs_type_from_env]
            except KeyError:
                raise DataClientException(
                    "Invalid remote file system type, set REMOTE_FS_TYPE"
                    f"as one of this supported types {list(supported_types.keys())}"  # noqa
                )

        return cls(
            file_service=remote_fs_type.from_env(connection_id=connection_id),
        )

    def list_directory(
        self, target: afs.FilePath
    ) -> t.List[t.Union[afs.Directory, afs.File]]:
        return self.file_service.list_directory(target)

    def create_directory(
        self,
        target: afs.FilePath,
    ) -> afs.Directory:
        return self.file_service.create_directory(target)

    def remove_directory(
        self,
        target: afs.FilePath,
    ) -> None:
        self.file_service.remove_directory(target)

    def copy_directory(
        self,
        source: afs.FilePath,
        target: afs.FilePath,
    ) -> afs.Directory:
        return self.file_service.copy_directory(source, target)

    def create_file_if_not_exists(
        self,
        target=afs.FilePath,
    ) -> afs.File:
        return self.file_service.create_file_if_not_exists(target)

    def remove_file(
        self,
        target: afs.FilePath,
    ) -> None:
        self.file_service.remove_file(target)

    def copy_file(
        self,
        source: afs.FilePath,
        target: afs.FilePath,
    ) -> afs.File:
        return self.file_service.copy_file(source, target)

    def exists(self, target=afs.FilePath) -> bool:
        return self.file_service.exists(target=target)

    @property
    def user(self) -> str:
        return self.file_service.user

    def change_permissions(
        self, target: afs.FilePath, new_permissions: afs.FileMeta
    ) -> None:
        self.file_service.change_permissions(target, new_permissions)


def _str_or_uuid_to_uuid(id_: t.Union[str, uuid.UUID]):
    if isinstance(id_, str):
        try:
            id_ = uuid.UUID(id_)
        except ValueError:
            raise DataClientException(
                "Badly formed hexadecimal UUID string for project ID"
            )
    return id_


def _get_available_remote_file_systems() -> t.Dict:
    supported_types = {}
    _attempt_file_service_import(
        supported_types=supported_types,
        name="S3",
        module="s3_file_service",
        cls="S3FileService",
        extras="s3",
    )
    _attempt_file_service_import(
        supported_types=supported_types,
        name="UNICORE",
        module="unicore_file_service",
        cls="UnicoreFileService",
        extras="s3",
    )
    return supported_types


def _attempt_file_service_import(
    supported_types: t.Dict, name: str, module: str, cls: str, extras: str
) -> None:
    """Attempt to import file service from module.

    Parameters
    ----------
    supported_types : dict
        The supported remote file system types.

        If available, the file system will be added.
    name : str
        Name of the remote file system type.

        E.g. ``"S3"`` or ``"UNICORE"``.
    module : str
        Name of the module inside ``mantik.remote_file_system``.

        E.g. ``"s3_file_service"`` or ``"unicore_file_service"``.
    cls : str
        Name of the class inside the respective module.
    extras : str
        Name of the extras inside ``pyproject.toml`` required for
        the remote file system.

    Notes
    -----
    This is required to avoid import errors when extras are not installed.

    Extras for the respective file services are defined in ``pyproject.toml``.

    """
    try:
        sub_module = getattr(mantik.remote_file_service, module)
    except ModuleNotFoundError:
        logger.warning(
            (
                "Unable to import %s remote file service, "
                'install required requirements via `pip install "mantik[%s]"`'
            ),
            name,
            extras,
            exc_info=True,
        )
    else:
        supported_types[name] = getattr(sub_module, cls)
