import mlflow.environment_variables
import pytest

import mantik.mlflow
import mantik.utils as utils


@pytest.fixture(autouse=True)
def set_mlflow_env_vars() -> None:
    with utils.env.env_vars_set(
        {
            utils.mlflow.TRACKING_URI_ENV_VAR: "https://invalid",
            mlflow.environment_variables.MLFLOW_HTTP_REQUEST_TIMEOUT.name: "0",
            mlflow.environment_variables.MLFLOW_HTTP_REQUEST_BACKOFF_FACTOR.name: "0",  # noqa: E501
            mlflow.environment_variables.MLFLOW_HTTP_REQUEST_MAX_RETRIES.name: "0",  # noqa: E501
        }
    ):
        yield


def test_init_tracking(caplog):
    mantik.mlflow.init_tracking()

    assert "Unable to retrieve access token from Mantik API" in caplog.text


def test_start_run(caplog):
    with mantik.mlflow.start_run():
        pass
    assert "Start MLflow run failed" in caplog.text


def test_active_run(caplog):
    assert mantik.mlflow.active_run() is None


def test_end_run(caplog):
    mantik.mlflow.end_run()


def test_delete_run(caplog):
    with pytest.raises(NotImplementedError):
        mantik.mlflow.delete_run("id")


def test_create_experiment(caplog):
    with pytest.raises(NotImplementedError):
        mantik.mlflow.create_experiment("name")


def test_delete_experiment(caplog):
    with pytest.raises(NotImplementedError):
        mantik.mlflow.delete_experiment(0)


def test_log_artifact(caplog, tmp_path):
    mantik.mlflow.log_artifact(tmp_path)
    _assert_expected_error_in_logs(caplog)


def test_log_artifacts(caplog, tmp_path):
    mantik.mlflow.log_artifacts(tmp_path)
    _assert_expected_error_in_logs(caplog)


def test_log_figure(caplog, tmp_path):
    mantik.mlflow.log_figure(tmp_path, "filename")
    _assert_expected_error_in_logs(caplog)


def test_log_image(caplog, tmp_path):
    mantik.mlflow.log_image(tmp_path, "filename")
    _assert_expected_error_in_logs(caplog)


def test_log_metric(caplog):
    mantik.mlflow.log_metric(key="key", value=0, step=0)
    _assert_expected_error_in_logs(caplog)


def test_log_metrics(caplog):
    mantik.mlflow.log_metrics({"key": 0}, step=0)
    _assert_expected_error_in_logs(caplog)


def test_log_param(caplog):
    mantik.mlflow.log_param(key="key", value="value")
    _assert_expected_error_in_logs(caplog)


def test_log_params(caplog):
    mantik.mlflow.log_params({"key": "value"})
    _assert_expected_error_in_logs(caplog)


def test_log_text(caplog):
    mantik.mlflow.log_text("text", "filename")
    _assert_expected_error_in_logs(caplog)


def test_register_model(caplog):
    mantik.mlflow.register_model("uri", "modelname")
    _assert_expected_error_in_logs(caplog)


def test_set_tag(caplog):
    mantik.mlflow.set_tag(key="name", value="value")
    _assert_expected_error_in_logs(caplog)


def test_set_tags(caplog):
    mantik.mlflow.set_tags({"name": "value"})
    _assert_expected_error_in_logs(caplog)


def test_delete_tag(caplog):
    mantik.mlflow.delete_tag("name")
    _assert_expected_error_in_logs(caplog)


def test_set_tracking_uri(caplog):
    mantik.mlflow.set_tracking_uri("mlruns")


def test_get_tracking_uri(caplog):
    result = mantik.mlflow.get_tracking_uri()
    assert result == "mlruns"


@pytest.mark.parametrize(("method"), [mlflow.start_run, "start_run"])
def test_call_method(caplog, method):
    result = mantik.mlflow.call_method(method, "id")

    assert result is None

    assert "Calling mlflow.start_run with args=('id',)" in caplog.text


def _assert_expected_error_in_logs(caplog):
    assert "MLflow API request failed" in caplog.text
