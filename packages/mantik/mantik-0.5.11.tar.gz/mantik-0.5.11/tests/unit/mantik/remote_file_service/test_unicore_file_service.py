import pytest

import mantik.remote_file_service.unicore_file_service as unicore_fs


@pytest.mark.parametrize(
    "path,expected",
    [
        ("remote:/path/local.file", True),
        ("/path/local.file", False),
    ],
)
def test_is_remote(path: str, expected: bool) -> None:
    assert unicore_fs.UnicoreFileService.is_remote(path) == expected


@pytest.mark.parametrize(
    "path,expected",
    [
        ("remote:/path/local.file", "/path/local.file"),
        ("remote:/path", "/path"),
    ],
)
def test_localise_path(path, expected) -> None:
    assert unicore_fs.UnicoreFileService.localise_path(path=path) == expected
