# import contextlib
import contextlib
import os
import unittest.mock
import uuid

import pytest
import pytest_mock

import mantik
import mantik.utils.mantik_api as mantik_api


def test_submit_run(mock_mantik_api_request, info_caplog):
    submit_run_data = {
        "name": "run-name",
        "experimentRepositoryId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "codeRepositoryId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "branch": "main",
        "commit": "string",
        "dataRepositoryId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "connectionId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "computeBudgetAccount": "a-budget-account",
        "mlflowMlprojectFilePath": "/path",
        "entryPoint": "main",
        "mlflowParameters": {},
        "backendConfig": {
            "UnicoreApiUrl": "https://zam2125.zam.kfa-juelich.de:9112/JUWELS/rest/core",  # noqa F401
            "Environment": {
                "Apptainer": {"Path": "some/image/path.name", "Type": "local"}
            },
            "Resources": {"Queue": "devel", "Nodes": 1},
        },
    }
    project_id = uuid.uuid4()
    with mock_mantik_api_request(
        method="POST",
        end_point=f"/projects/{project_id}/runs",
        status_code=201,
        json_response={},
        expected_error=204,
    ) as (m, error):
        mantik_api.run.submit_run(
            project_id=project_id,
            submit_run_data=submit_run_data,
            token="test_token",
        )
        assert any(
            "Run has been successfully submitted" in message
            for message in info_caplog.messages
        )
    if error:
        assert any(
            "Call to Mantik API" in message for message in info_caplog.messages
        )


def test_save_run(mock_mantik_api_request, info_caplog):
    project_id = uuid.uuid4()
    with mock_mantik_api_request(
        method="POST",
        end_point=f"/projects/{project_id}/runs",
        status_code=201,
        json_response={},
        expected_error=204,
    ) as (m, error):
        mantik_api.run.save_run(
            project_id=project_id,
            run_data={},
            token="test_token",
        )
        assert any(
            "Run has been successfully saved" in message
            for message in info_caplog.messages
        )


def test_update_run_status(mock_mantik_api_request, info_caplog):
    project_id = uuid.uuid4()
    run_id = uuid.uuid4()
    with mock_mantik_api_request(
        method="PUT",
        end_point=f"/projects/{project_id}/runs/{run_id}/status",
        status_code=200,
        json_response={},
        expected_error=204,
    ) as (m, error):
        mantik_api.run.update_run_status(
            project_id=project_id,
            status="FINISHED",
            token="test_token",
            run_id=run_id,
        )
        assert any(
            "Run status has been successfully updated" in message
            for message in info_caplog.messages
        )


def test_update_logs(mock_mantik_api_request, info_caplog):
    project_id = uuid.uuid4()
    run_id = uuid.uuid4()
    with mock_mantik_api_request(
        method="PUT",
        end_point=f"/projects/{project_id}/runs/{run_id}/logs",
        status_code=200,
        json_response={},
        expected_error=204,
    ) as (m, error):
        mantik_api.run.update_logs(
            project_id=project_id,
            logs="Test \n logs",
            token="test_token",
            run_id=run_id,
        )
        assert any(
            "Run logs has been successfully updated" in message
            for message in info_caplog.messages
        )


def test_get_download_artifact_url(mock_mantik_api_request, info_caplog):
    project_id = uuid.uuid4()
    run_id = uuid.uuid4()
    download_url = "test-url"
    with mock_mantik_api_request(
        method="GET",
        end_point=f"/projects/{project_id}/runs/{run_id}/artifacts",
        status_code=200,
        json_response={"url": download_url},
        expected_error=204,
    ) as (m, error):
        url = mantik_api.run.get_download_artifact_url(
            project_id=project_id,
            token="test_token",
            run_id=run_id,
        )
        assert url == download_url
        assert any(
            "Artifacts' download url successfully fetched" in message
            for message in info_caplog.messages
        )


@pytest.fixture(scope="module")
def colab_notebook_source() -> mantik_api.run.NoteBookSource:
    return mantik_api.run.NoteBookSource(
        location="https://colab.research.google.com/drive/1sS7tLqg8T9c"
        "WgPa_W0n0n2nxiz54v1d-?authuser=0#scrollTo=sXTl79-1UjM3",
        version=None,
        provider=mantik_api.run.ProviderType.COLAB,
    )


@pytest.fixture(scope="module")
def jupyter_notebook_source() -> mantik_api.run.NoteBookSource:
    return mantik_api.run.NoteBookSource(
        location="/home/user/projects/analysis/notebooks/data_analysis.ipynb",
        version="a1b2c3d",
        provider=mantik_api.run.ProviderType.JUPYTER,
    )


def test_get_latest_git_commit():
    """
    Given I am running the tests in a Gitlab CI Pipeline
    When I try to retrieve the latest git commit hash
    Then The commit hash retrieved should be the same as the one in the gitlab
    pipeline
    """
    try:
        CI_COMMIT_SHA = os.getenv("CI_COMMIT_SHA")
        if CI_COMMIT_SHA is None:
            # If the environment variable is not set (i.e, not in a gitlab ci)
            # skip the test. There might be a better way for testing locally.
            return
    except Exception:
        # If any exception occurs while trying to fetch the environment
        # variable, skip the test
        return
    assert mantik_api.run.get_latest_git_commit() == CI_COMMIT_SHA


@pytest.mark.parametrize(
    "shell_str, expected",
    [
        ("ipykernel", mantik_api.run.ProviderType.JUPYTER),
        # Jupyter notebook
        ("google.colab", mantik_api.run.ProviderType.COLAB),
        # Google Colab environment
        ("TerminalInteractiveShell", None),  # IPython terminal
        ("OtherShell", None),  # Unknown environment
        (
            NameError,
            None,
        ),  # Standard Python interpreter or no IPython available
    ],
)
def test_check_notebook_type(
    mocker: pytest_mock.MockerFixture, shell_str, expected
):
    """
    Given the mantik package needs to check the running environment
    When the check_notebook_type function is called
    Then it should return `ProviderType.JUPYTER` if the environment is a Jupyter
    notebook
    But it should return `ProviderType.COLAB` if the environment is a Google
    Colab notebook
    But it should return `None` if the environment is an IPython terminal or
    environment is an unrecognized shell or if a `NameError` is raised,
    indicating no IPython is available
    """
    # Mock the get_ipython function
    mock_get_ipython = mocker.patch("IPython.get_ipython")

    if shell_str is NameError:
        # Simulate a NameError when get_ipython is called
        mock_get_ipython.return_value = None
    else:
        # Simulate returning the appropriate shell string or environment
        mock_get_ipython.return_value = shell_str

    # Call the function and assert the result matches the expected value
    result = mantik_api.run.check_notebook_type()
    assert result == expected


@pytest.mark.parametrize(
    "notebook_source", ["jupyter_notebook_source", "colab_notebook_source"]
)
def test_update_notebook_source(
    mock_mantik_api_request, notebook_source, info_caplog, request
):
    """
    Given I have new information about the notebook
    When I update the notebook information
    Then I can retrieve this same new information from mantik API
    """
    notebook_source = request.getfixturevalue(notebook_source)

    project_id = uuid.uuid4()
    run_id = uuid.uuid4()

    with mock_mantik_api_request(
        method="PUT",
        end_point=f"/projects/{project_id}/runs/{run_id}/notebook-source",
        status_code=204,
        json_response={},
        expected_error=404,
    ) as (m, error):
        response = mantik_api.run.update_notebook_source(
            project_id=project_id,
            run_id=run_id,
            notebook_source=notebook_source,
            token="test_token",
        )
        assert response.status_code == 204
        assert any(
            "Run notebook source has been successfully updated" in message
            for message in info_caplog.messages
        )


@pytest.mark.parametrize(
    "notebook_source, ipython, notebook_type",
    [
        ("not_a_notebook", "TerminalInteractiveShell", None),
        (
            "jupyter_notebook_source",
            "ipykernel.zmqshell.ZMQInteractiveShell object at 0x106bb4d10",
            "JUPYTER",
        ),
        (
            "google_colab_source",
            "google.colab._shell.Shell object at " "0x7ca756186bd0",
            "COLAB",
        ),
    ],
)
def test_update_notebook_details(
    mock_get_code,
    mock_get_experiment,
    mock_get_unique_run_name,
    mock_update_run_logs,
    mocker: pytest_mock.MockerFixture,
    notebook_source,
    ipython,
    notebook_type,
    sample_run_configuration,
    sample_project_id,
    mock_get_user_id_from_token,
    mock_code_git_connection_response,
    fake_token,
):
    """
    Given I have a local Jupyter notebook with a Mantik run command in it
    When I execute the cell that calls onto Mantik run
    Then Infrastucture stored with Mantik API
    includes the correct details of the Jupyter notebook file
    """

    context = contextlib.nullcontext()
    with context:
        mocked_local_run_manager = unittest.mock.Mock(
            spec=mantik.runs.local.LocalRunManager
        )
        run_id = uuid.uuid4()

        run_output = mantik.runs.local.LocalRunOutput(
            run_id=run_id, exception=None
        )

        # Mocking the run environment to be like a jupyter notebook
        mock_get_ipython = mocker.patch("IPython.get_ipython")
        mock_get_ipython.return_value = ipython

        mocker.patch(
            "IPython.get_ipython",
            return_value=unittest.mock.Mock(
                kernel=unittest.mock.Mock(
                    shell=unittest.mock.Mock(
                        user_ns={"__session__": "mock/path/to/notebook.ipynb"}
                    )
                )
            ),
        )

        mock_check_notebook_type = mocker.patch(
            "mantik.utils.mantik_api.run.check_notebook_type",
            return_value=notebook_type,
        )

        mock_update_notebook_source = mocker.patch(
            "mantik.utils.mantik_api.run.update_notebook_source"
        )

        mocked_local_run_manager.start_local_run = unittest.mock.Mock(
            return_value=run_output
        )

        mantik.runs.local.run(
            data=sample_run_configuration,
            project_id=sample_project_id,
            mantik_token=fake_token,
            run_manager=mocked_local_run_manager,
            data_target_dir="data",
        )

        if (
            notebook_source == "jupyter_notebook_source"
            or notebook_source == "google_colab_source"
        ):
            # If code is running a notebook
            mock_check_notebook_type.assert_called_once()
            mock_update_notebook_source.assert_called_once()

        else:
            # Case of not running in a jupyter notebook
            mock_check_notebook_type.assert_called_once()
