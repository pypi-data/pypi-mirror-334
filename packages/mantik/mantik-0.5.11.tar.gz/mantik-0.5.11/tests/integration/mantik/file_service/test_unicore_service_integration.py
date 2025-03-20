import pathlib
import shutil
import unittest.mock

import fs
import pytest

import mantik.remote_file_service.unicore_file_service as unicore_fs


LOCAL_WORKING_DIRECTORY = pathlib.Path(__file__).parent / "workspace"

SAMPLE_FOLDER = "sample-directory"
SAMPLE_FILENAME = "hello-world.txt"
SAMPLE_FILE_FILE_PATH = f"{SAMPLE_FOLDER}/{SAMPLE_FILENAME}"

USER = "demouser"

AUTH_URL = "http://test-unicore"


@pytest.fixture
def temp_testing_folder_path(tmp_path) -> str:
    # Copy the source folder to the temporary directory
    shutil.copytree(
        f"{LOCAL_WORKING_DIRECTORY}/{SAMPLE_FOLDER}",
        tmp_path / "local" / SAMPLE_FOLDER,
    )

    yield str(tmp_path)


@pytest.fixture()
def unicore_fs_client(
    temp_testing_folder_path, requests_mock
) -> unicore_fs.UnicoreFileService:
    requests_mock.post(
        url=f"{AUTH_URL}",
        json={
            "serverHost": "http://uftp-host",
            "serverPort": 9000,
            "secret": "secret123",
        },
    )
    client = unicore_fs.UnicoreFileService(
        local_base_path=temp_testing_folder_path + "/local",
        username=USER,
        password="test",
        auth_url="http://test-unicore",
    )

    return client


@pytest.fixture()
def mock_get_remote_fs(temp_testing_folder_path):
    fake_remote_path = pathlib.Path(temp_testing_folder_path) / "remote"
    fake_remote_path.mkdir()
    shutil.copytree(
        f"{LOCAL_WORKING_DIRECTORY}/{SAMPLE_FOLDER}",
        fake_remote_path / SAMPLE_FOLDER,
    )
    with unittest.mock.patch(
        "mantik.remote_file_service.unicore_file_service.UnicoreFileService._get_remote_fs",  # noqa E501
        return_value=fs.open_fs(fake_remote_path.as_posix()),
    ) as patch:
        yield patch


def test_list_directory(unicore_fs_client, mock_get_remote_fs) -> None:
    local_list_dir = unicore_fs_client.list_directory(SAMPLE_FOLDER)
    assert len(local_list_dir) == 1
    assert local_list_dir[0].path == SAMPLE_FILE_FILE_PATH
    remote_list_dir = unicore_fs_client.list_directory(
        f"remote://{SAMPLE_FOLDER}"
    )
    assert len(remote_list_dir) == 1
    assert (
        remote_list_dir[0].path == f"remote:/{SAMPLE_FOLDER}/{SAMPLE_FILENAME}"
    )


def test_copy_file(unicore_fs_client, mock_get_remote_fs) -> None:
    assert not unicore_fs_client.exists(f"remote://{SAMPLE_FILENAME}")

    unicore_fs_client.copy_file(
        f"{SAMPLE_FILE_FILE_PATH}",
        f"remote://{SAMPLE_FILENAME}",
    )
    assert unicore_fs_client.exists(f"remote://{SAMPLE_FILENAME}")


def test_remove_file(unicore_fs_client, mock_get_remote_fs) -> None:
    assert unicore_fs_client.exists(
        f"remote://{SAMPLE_FOLDER}/{SAMPLE_FILENAME}"
    )
    unicore_fs_client.remove_file(f"remote://{SAMPLE_FOLDER}/{SAMPLE_FILENAME}")
    assert not unicore_fs_client.exists(
        f"remote://{SAMPLE_FOLDER}/{SAMPLE_FILENAME}"
    )

    #  local
    assert unicore_fs_client.exists(SAMPLE_FILE_FILE_PATH)
    unicore_fs_client.remove_file(SAMPLE_FILE_FILE_PATH)
    assert not unicore_fs_client.exists(SAMPLE_FILE_FILE_PATH)


def test_copy_directory(unicore_fs_client, mock_get_remote_fs) -> None:
    unicore_fs_client.remove_directory(f"remote://{SAMPLE_FOLDER}")
    assert not unicore_fs_client.exists(f"remote://{SAMPLE_FOLDER}")

    unicore_fs_client.copy_directory(SAMPLE_FOLDER, f"remote://{SAMPLE_FOLDER}")
    assert unicore_fs_client.exists(f"remote://{SAMPLE_FOLDER}")

    assert len(
        unicore_fs_client.list_directory(f"remote://{SAMPLE_FOLDER}")
    ) == len(unicore_fs_client.list_directory(SAMPLE_FOLDER))


def test_remove_directory(unicore_fs_client, mock_get_remote_fs) -> None:
    assert unicore_fs_client.exists(f"remote://{SAMPLE_FOLDER}")
    unicore_fs_client.remove_directory(f"remote://{SAMPLE_FOLDER}")
    assert not unicore_fs_client.exists(f"remote://{SAMPLE_FOLDER}")

    #  local
    assert unicore_fs_client.exists(SAMPLE_FOLDER)
    unicore_fs_client.remove_directory(SAMPLE_FOLDER)
    assert not unicore_fs_client.exists(SAMPLE_FOLDER)


def test_create_directory(unicore_fs_client, mock_get_remote_fs) -> None:
    unicore_fs_client.create_directory("remote://new-folder")
    assert unicore_fs_client.exists("remote://new-folder")


def test_user(unicore_fs_client) -> None:
    assert unicore_fs_client.user == USER
