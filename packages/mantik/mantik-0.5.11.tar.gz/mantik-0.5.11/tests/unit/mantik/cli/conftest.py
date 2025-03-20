import pathlib

import pytest

FILE_DIR = pathlib.Path(__file__).parent


@pytest.fixture()
def example_project_absolute_path() -> str:
    return (FILE_DIR / "../../../resources/test-project").as_posix()


@pytest.fixture()
def example_project_relative_path() -> str:
    return "../test-project"
