import datetime

import pytest

import mantik.remote_file_service.abstract_file_service as afs
import mantik.remote_file_service.data_client as _data_client


class TestDataClient:
    def test_list_directory(self, data_client, fake_unicore_fs):
        target = "test_target"
        assert data_client.list_directory(
            target
        ) == fake_unicore_fs.list_directory(target)

    def test_create_directory(self, data_client, fake_unicore_fs, project_id):
        target = "test_target"
        assert data_client.create_directory(
            target,
        ) == fake_unicore_fs.create_directory(target)

    def test_remove_directory(self, data_client, fake_unicore_fs, project_id):
        target = "test_target"
        assert data_client.remove_directory(
            target
        ) == fake_unicore_fs.remove_directory(target)

    def test_copy_directory(self, data_client, fake_unicore_fs, project_id):
        source = "test_source"
        target = "test_target"
        assert data_client.copy_directory(
            source,
            target,
        ) == fake_unicore_fs.copy_directory(source, target)

    def test_create_file_if_not_exists(
        self, data_client, fake_unicore_fs, project_id
    ):
        target = "test_target"
        assert data_client.create_file_if_not_exists(
            target,
        ) == fake_unicore_fs.create_file_if_not_exists(target)

    def test_remove_file(self, data_client, fake_unicore_fs, project_id):
        target = "test_target"
        assert data_client.remove_file(target) == fake_unicore_fs.remove_file(
            target
        )

    def test_copy_file(self, data_client, fake_unicore_fs, project_id):
        source = "test_source"
        target = "test_target"
        assert data_client.copy_file(
            source,
            target,
        ) == fake_unicore_fs.copy_file(source, target)

    def test_user(self, data_client, fake_unicore_fs):
        assert data_client.user == fake_unicore_fs.user

    def test_change_permissions(self, data_client, fake_unicore_fs):
        target = "test_target"
        new_permissions = afs.FileMeta(
            last_changed=datetime.datetime(2022, 1, 1),
            mode="xxx",
            owner=fake_unicore_fs.user,
        )
        assert data_client.change_permissions(
            target, new_permissions
        ) == fake_unicore_fs.change_permissions(target, new_permissions)

    def test_init_not_supported_backend(self, env_vars_set):
        with env_vars_set(
            {
                "MANTIK_PROJECT_ID": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "REMOTE_FS_TYPE": "NEW_BACKEND",
            }
        ), pytest.raises(_data_client.DataClientException) as e:
            assert _data_client.DataClient.from_env()

        expected = (
            "Invalid remote file system type, "
            "set REMOTE_FS_TYPEas one of this supported "
            "types ['S3', 'UNICORE']"
        )

        result = str(e.value)

        assert result == expected
