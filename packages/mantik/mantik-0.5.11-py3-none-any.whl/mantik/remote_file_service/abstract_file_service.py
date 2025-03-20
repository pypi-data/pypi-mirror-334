import abc
import dataclasses
import datetime
import pathlib
import typing as t
import uuid

import fs.base

FilePath = t.Union[str, pathlib.Path]

REMOTE_FS_BASE_PATH_ENV_VAR = "MANTIK_REMOTE_FS_BASE_PATH"
LOCAL_FS_BASE_PATH_ENV_VAR = "MANTIK_LOCAL_FS_BASE_PATH"
REMOTE_FS_TYPE_ENV_VAR = "REMOTE_FS_TYPE"


@dataclasses.dataclass
class FileMeta:
    owner: str
    mode: str
    last_changed: datetime.datetime


@dataclasses.dataclass
class File:
    path: FilePath
    metadata: FileMeta
    is_remote: bool


@dataclasses.dataclass
class Directory(File):
    children: t.List[t.Union["Directory", "File"]]


class AbstractFileService(abc.ABC):
    """
    Abstract class to define methods used for (remote) file handling.

    This interface must be easily implementable with common file transfer
    methods (FTP, boto/S3, GNU filesystem, pathlib + python IO ...).
    """

    def __init__(
        self,
        local_base_path: str = ".",
    ):
        self.relative_local_fs = fs.open_fs(local_base_path)
        self.absolute_local_fs = fs.open_fs("/")

    @abc.abstractmethod
    def list_directory(
        self, target: FilePath
    ) -> t.List[t.Union[Directory, File]]:
        """
        List content of directory.

        Note: bash ls
        """

    @abc.abstractmethod
    def create_directory(self, target: FilePath) -> Directory:
        """
        Make a new directory.

        Note: bash mkdir
        """

    @abc.abstractmethod
    def remove_directory(self, target: FilePath) -> None:
        """Remove a directory.

        Note: bash rm -r
        """

    @abc.abstractmethod
    def copy_directory(
        self,
        source: FilePath,
        target: FilePath,
    ) -> Directory:
        """Copy directory.

        Note: bash cp
        """

    @abc.abstractmethod
    def create_file_if_not_exists(self, target: FilePath) -> File:
        """Create (empty) file if not exists.

        Note: bash touch
        """

    @abc.abstractmethod
    def remove_file(self, target: FilePath) -> None:
        """Remove file or directory.

        Note: bash rm
        """

    @abc.abstractmethod
    def copy_file(
        self,
        source: FilePath,
        target: FilePath,
    ) -> File:
        """Copy file.

        Note: bash cp
        """

    @abc.abstractmethod
    def exists(self, target=FilePath) -> bool:
        """Return if file exists"""

    @property
    @abc.abstractmethod
    def user(self) -> str:
        """Return current user."""

    @abc.abstractmethod
    def change_permissions(
        self, target: FilePath, new_permissions: FileMeta
    ) -> None:
        """Change metadata (permissions) of a file.

        Note: bash chmod
        """

    @classmethod
    @abc.abstractmethod
    def from_env(
        cls, connection_id: t.Optional[uuid.UUID] = None
    ) -> "AbstractFileService":
        """Instantiate with environment variables.

        Credentials are either fetched from mantik api
        or passed in through end vars.
        """

    @classmethod
    @abc.abstractmethod
    def localise_path(self, target: FilePath) -> FilePath:
        """Localize a remote path"""

    @classmethod
    @abc.abstractmethod
    def is_remote(self, target: FilePath) -> bool:
        """Return if a path is remote or not"""

    @abc.abstractmethod
    def _get_remote_fs(self, **nargs) -> fs.base.FS:
        """Return the remote file system"""

    def _get_current_fs_and_relative_filepath(self, path: FilePath):
        current_fs = self._get_fs(path)
        relative_path = (
            self.localise_path(path) if self.is_remote(path) else path
        )

        return current_fs, relative_path

    def _get_fs(self, path: FilePath):
        if self.is_remote(path):
            return self._get_remote_fs(**self._get_fs_nargs(path=path))
        if isinstance(path, pathlib.Path):
            path = path.as_posix()
        if path.startswith("/"):
            return self.absolute_local_fs
        return self.relative_local_fs

    def _get_fs_nargs(self, path: FilePath) -> dict:
        """Extra nargs that might be needed for getting the remote fs"""
        return {}
