import json
import os
import pathlib
import tempfile
import uuid
from unittest.mock import Mock
from unittest.mock import patch

import pytest

import mantik.runs.notebook
import mantik.utils.mantik_api.run


@pytest.fixture
def mock_environment():
    with patch.dict(
        os.environ,
        {
            "MLFLOW_TRACKING_TOKEN": "mock_token",
            "MANTIK_EXPERIMENT_REPOSITORY_ID": str(uuid.uuid4()),
        },
    ):
        yield


@pytest.fixture
def mock_mlflow_run():
    mock_run = Mock()
    mock_run.info = Mock()
    mock_run.info.run_id = "mock_run_id"
    mock_run.info.status = "RUNNING"
    return mock_run


@pytest.mark.parametrize(
    "mantik_func,mlflow_mock,kwargs,setup_required",
    [
        # Simple logging functions
        (
            mantik.log_param,
            "mlflow.log_param",
            {"key": "param1", "value": 1},
            False,
        ),
        (
            mantik.log_params,
            "mlflow.log_params",
            {"params": {"param2": 0.01, "param3": 2}},
            False,
        ),
        (
            mantik.log_metric,
            "mlflow.log_metric",
            {"key": "metric1", "value": 1, "step": None},
            False,
        ),
        (
            mantik.log_metrics,
            "mlflow.log_metrics",
            {"metrics": {"metric2": 2, "metric3": 3}, "step": None},
            False,
        ),
        (
            mantik.log_dict,
            "mlflow.log_dict",
            {"dictionary": {"k": "v"}, "artifact_file": "data.json"},
            False,
        ),
        (
            mantik.log_text,
            "mlflow.log_text",
            {"text": "text1", "artifact_file": "file1.txt"},
            False,
        ),
        # Functions requiring file setup
        (
            mantik.log_artifact,
            "mlflow.log_artifact",
            {"local_path": "TEMP_PATH", "artifact_path": None},
            True,
        ),
        (
            mantik.log_artifacts,
            "mlflow.log_artifacts",
            {"local_dir": "TEMP_DIR", "artifact_path": "states"},
            True,
        ),
    ],
)
def test_mantik_logging_functions(
    mock_environment,
    mock_mlflow_run,
    mantik_func,
    mlflow_mock,
    kwargs,
    setup_required,
):
    """
    Test various Mantik logging functions and their integration with MLflow.

    Background:
        Given a mock MLflow environment is set up
        And a mock MLflow run is active
        And all necessary Mantik API calls are mocked

    Scenario Outline: Log different types of data through Mantik
        Given a specific Mantik logging function
        And its corresponding MLflow function is mocked
        When I call the Mantik function with specific parameters
        Then the corresponding MLflow function should be called with the same
        parameters

    Examples:
        | Function Type | Setup Required |
        | Parameters   | No             |
        | Artifacts    | Yes            |

    Parameters
    ----------
    mock_environment : fixture
        Pytest fixture that sets up a mock environment with necessary
        environment variables and context.
    mock_mlflow_run : fixture
        Pytest fixture that provides a mock MLflow ActiveRun object.
    mantik_func : function
        The Mantik logging function to test (e.g., log_param, log_metric).
    mlflow_mock : str
        The path to the MLflow function to mock (e.g., "mlflow.log_param").
    kwargs : dict
        Keyword arguments to pass to the function being tested.
    setup_required : bool
        Indicates whether the test requires temporary file setup (True for
        artifact logging).

    Returns
    -------
    None

    Raises
    ------
    AssertionError
        If the MLflow mock isn't called with the expected parameters.
    """

    # Setup for run initialization
    mock_experiment = Mock()
    mock_experiment.mlflow_experiment_id = "mock_experiment_id"
    test_project_id = uuid.uuid4()
    test_experiment_repository_id = uuid.uuid4()

    # Common patches
    with patch(
        "mantik.utils.mantik_api.experiment_repository.get_one",
        return_value=mock_experiment,
    ), patch("mantik.runs.local.save_run_data"), patch(
        "mantik.utils.mantik_api.run.update_run_status"
    ), patch(
        "mantik.utils.mantik_api.run.update_run_infrastructure"
    ), patch(
        "mantik.utils.mantik_api.run.find_notebook_location",
        return_value="example.ipynb",
    ), patch(
        "mantik.utils.mantik_api.run.check_notebook_type",
        return_value=mantik.utils.mantik_api.run.ProviderType.JUPYTER,
    ), patch(
        "mantik.utils.mantik_api.run.update_notebook_source"
    ), patch(
        "IPython.get_ipython"
    ), patch(
        "mlflow.start_run", return_value=mock_mlflow_run
    ), patch(
        mlflow_mock
    ) as mock_func:
        # Start the run
        mantik.start_run(
            run_name="test_run",
            project_id=test_project_id,
            experiment_repository_id=test_experiment_repository_id,
        )

        if setup_required:
            with tempfile.TemporaryDirectory() as tmp_dir:
                tmp_dir_path = pathlib.Path(tmp_dir)

                if mantik_func == mantik.log_artifact:
                    # Setup for log_artifact
                    features = (
                        "rooms, zipcode, median_price, school_rating, transport"
                    )
                    file_path = tmp_dir_path / "features.txt"
                    file_path.write_text(features)
                    kwargs["local_path"] = str(file_path)

                elif mantik_func == mantik.log_artifacts:
                    # Setup for log_artifacts
                    features = (
                        "rooms, zipcode, median_price, school_rating, transport"
                    )
                    data = {"state": "TX", "Available": 25, "Type": "Detached"}

                    with (tmp_dir_path / "data.json").open("w") as f:
                        json.dump(data, f, indent=2)
                    with (tmp_dir_path / "features.json").open("w") as f:
                        f.write(features)

                    kwargs["local_dir"] = str(tmp_dir_path)

                # Execute function and verify
                mantik_func(**kwargs)
                mock_func.assert_called_once_with(**kwargs)
        else:
            # Execute function and verify
            mantik_func(**kwargs)
            mock_func.assert_called_once_with(**kwargs)


def test_mantik_run_lifecycle(mock_environment, mock_mlflow_run):
    """
    Test the lifecycle of a Mantik run, including initialization and
    termination.

    Scenario: Initialize and terminate a Mantik run
        Given a mock MLflow environment
        And a mock experiment with MLflow experiment ID
        When I start a Mantik run with specific parameters
        Then MLflow should start a run with correct configuration
        And run infrastructure should be updated
        And notebook type should be checked
        And notebook source should be updated
        When I end the run
        Then MLflow should properly terminate the run

    Parameters
    ----------
    mock_environment : fixture
        Pytest fixture that sets up a mock environment with necessary
        environment variables and context.
    mock_mlflow_run : fixture
        Pytest fixture that provides a mock MLflow ActiveRun object.

    Returns
    -------
    None

    Raises
    ------
    AssertionError
        If any of the expected interactions with mock objects fail.
    """
    mock_experiment = Mock()
    mock_experiment.mlflow_experiment_id = "mock_experiment_id"
    test_project_id = uuid.uuid4()
    test_experiment_repository_id = uuid.uuid4()

    with patch(
        "mantik.utils.mantik_api.experiment_repository.get_one",
        return_value=mock_experiment,
    ), patch("mantik.runs.local.save_run_data"), patch(
        "mantik.utils.mantik_api.run.update_run_status"
    ), patch(
        "mantik.utils.mantik_api.run.update_run_infrastructure"
    ) as update_infra, patch(
        "mantik.utils.mantik_api.run.check_notebook_type",
        return_value=mantik.utils.mantik_api.run.ProviderType.JUPYTER,
    ) as check_notebook, patch(
        "mantik.utils.mantik_api.run.find_notebook_location",
        return_value="example.ipynb",
    ), patch(
        "mantik.utils.mantik_api.run.update_notebook_source"
    ) as notebook_source, patch(
        "IPython.get_ipython"
    ), patch(
        "mlflow.start_run", return_value=mock_mlflow_run
    ) as mock_start_run, patch(
        "mlflow.end_run"
    ) as mock_end_run:
        # Test start_run
        mantik.start_run(
            run_name="test_run",
            project_id=test_project_id,
            experiment_repository_id=test_experiment_repository_id,
        )

        mock_start_run.assert_called_once_with(
            experiment_id="mock_experiment_id",
            run_name="test_run",
            nested=False,
        )
        update_infra.assert_called_once()
        check_notebook.assert_called_once()
        notebook_source.assert_called_once()

        # Test end_run
        mantik.end_run()
        mock_end_run.assert_called_once()
