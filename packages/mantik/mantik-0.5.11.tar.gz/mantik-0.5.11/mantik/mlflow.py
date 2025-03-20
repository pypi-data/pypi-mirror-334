import contextlib
import functools
import logging
import pathlib
import typing as t

import mantik.tracking.environment as _environment
import mantik.tracking.track as track

try:
    import mlflow
    import mlflow.entities
    import mlflow.entities.model_registry
    import mlflow.utils.file_utils
    import mlflow.projects.utils
except ModuleNotFoundError as exc:
    raise RuntimeError(
        "Install supported MLflow version (`pip install mantik[mlflow]`)"
        "or any desired MLflow version"
    ) from exc


logger = logging.getLogger(__name__)


def _catch_exceptions(func: t.Callable) -> t.Callable:
    """Catch MLflow exceptions and log them instead of raising."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> t.Any:
        try:
            return func(*args, **kwargs)
        except mlflow.exceptions.MlflowException:
            logger.warning(
                "MLflow API request failed for %s with args %s and kwargs %s",
                func.__name__,
                args,
                kwargs,
                exc_info=True,
            )
            return None

    return wrapper


def init_tracking() -> _environment.Environment:
    """Attempts to initialize tracking to Mantik, emits warning if it fails.

    If successful, this sets the `MLFLOW_TRACKING_TOKEN` environment variable
    to the access token retrieved from the Mantik API.

    Returns
    -------
    mantik.tracking.environment.Environment
        Holds the access token for the Mantik and MLflow API.

    """
    try:
        return track.init_tracking()
    except Exception:
        logger.warning(
            "Unable to retrieve access token from Mantik API", exc_info=True
        )


@contextlib.contextmanager
def start_run(
    run_id: str = None,
    experiment_id: t.Optional[str] = None,
    run_name: t.Optional[str] = None,
    nested: bool = False,
    tags: t.Optional[t.Dict[str, t.Any]] = None,
    description: t.Optional[str] = None,
) -> mlflow.ActiveRun:
    """Start a new MLflow run or pick up the run specified as `MLFLOW_RUN_ID`,
    which is set by the Mantik Compute Backend when submitting a run."""
    try:
        yield mlflow.start_run(
            run_id=run_id,
            experiment_id=experiment_id,
            run_name=run_name,
            nested=nested,
            tags=tags,
            description=description,
        )
    except mlflow.exceptions.MlflowException:
        logger.warning("Start MLflow run failed", exc_info=True)
        yield None


@_catch_exceptions
def active_run() -> t.Optional[mlflow.ActiveRun]:
    """Get the currently active run, or `None` if no such run exists."""
    return mlflow.active_run()


@_catch_exceptions
def end_run(
    status: str = mlflow.entities.RunStatus.to_string(
        mlflow.entities.RunStatus.FINISHED
    ),
) -> None:
    """End an active MLflow run."""
    return mlflow.end_run(status=status)


def delete_run(run_id: str) -> None:
    """Not supported: only permitted via the Mantik platform."""
    raise NotImplementedError(
        "Deleting a run is only permitted via the Mantik platform"
    )


def create_experiment(
    name: str,
    artifact_location: t.Optional[str] = None,
    tags: t.Optional[t.Dict[str, t.Any]] = None,
) -> None:
    """Not supported: only permitted via the Mantik platform."""
    raise NotImplementedError(
        "Creating an experiment is only permitted via the Mantik platform"
    )


def delete_experiment(experiment_id: int) -> None:
    """Not supported: only permitted via the Mantik platform."""
    raise NotImplementedError(
        "Deleting an experiment is only permitted via the Mantik platform"
    )


@_catch_exceptions
def log_artifact(
    local_path: str, artifact_path: t.Optional[str] = None
) -> None:
    """Log a local file or directory as an artifact of the currently
    active run."""
    return mlflow.log_artifact(
        local_path=local_path, artifact_path=artifact_path
    )


@_catch_exceptions
def log_artifacts(
    local_dir: str, artifact_path: t.Optional[str] = None
) -> None:
    """Log all the contents of a local directory as artifacts of the run."""
    return mlflow.log_artifacts(
        local_dir=local_dir, artifact_path=artifact_path
    )


@_catch_exceptions
def log_dict(dictionary: t.Any, artifact_file: str) -> t.Any:
    """Log a JSON/YAML-serializable object (e.g. dict) as an artifact."""
    return mlflow.log_dict(dictionary=dictionary, artifact_file=artifact_file)


@_catch_exceptions
def log_figure(figure, artifact_file: str) -> t.Any:
    """Log a figure as an artifact."""
    return mlflow.log_figure(figure=figure, artifact_file=artifact_file)


@_catch_exceptions
def log_image(image, artifact_file: str) -> t.Any:
    """Log an image as an artifact."""
    return mlflow.log_image(image=image, artifact_file=artifact_file)


@_catch_exceptions
def log_metric(key: str, value: float, step: t.Optional[int] = None) -> None:
    """Log a metric for the current run."""
    return mlflow.log_metric(key=key, value=value, step=step)


@_catch_exceptions
def log_metrics(
    metrics: t.Dict[str, float], step: t.Optional[int] = None
) -> None:
    """Log a batch of metrics for the current run."""
    return mlflow.log_metrics(metrics=metrics, step=step)


@_catch_exceptions
def log_param(key: str, value: t.Any) -> t.Any:
    """Log a parameter (e.g. model hyperparameter) for the current run."""
    return mlflow.log_param(key=key, value=value)


@_catch_exceptions
def log_params(params: t.Dict[str, t.Any]) -> None:
    """Log a batch of params for the current run."""
    return mlflow.log_params(params)


@_catch_exceptions
def log_text(text: str, artifact_file: str) -> None:
    """Log text as an artifact."""
    return mlflow.log_text(text=text, artifact_file=artifact_file)


@_catch_exceptions
def register_model(
    model_uri,
    name,
    *,
    tags: t.Optional[t.Dict[str, t.Any]] = None,
) -> mlflow.entities.model_registry.ModelVersion:
    """Create a new model version in the model registry."""
    return mlflow.register_model(model_uri=model_uri, name=name, tags=tags)


@_catch_exceptions
def set_tag(key: str, value: t.Any) -> None:
    """Log a tag for the current run."""
    return mlflow.set_tag(key=key, value=value)


@_catch_exceptions
def set_tags(tags: t.Dict[str, t.Any]) -> None:
    """Log a batch of tags for the current run."""
    return mlflow.set_tags(tags=tags)


@_catch_exceptions
def delete_tag(key: str) -> None:
    """Delete a tag."""
    return mlflow.delete_tag(key=key)


@_catch_exceptions
def set_tracking_uri(uri: t.Union[str, pathlib.Path]) -> None:
    """Set the tracking server URI (`MLFLOW_TRACKING_URI` environment
    variable).

    """
    return mlflow.set_tracking_uri(uri=uri)


@_catch_exceptions
def get_tracking_uri() -> str:
    """Get the MLflow tracking URI set as `MLFLOW_TRACKING_URI`."""
    return mlflow.get_tracking_uri()


@_catch_exceptions
def get_local_backend_config_run_id_env_var() -> str:
    """Get the MLflow local backend config run id environment variable."""
    return mlflow.projects.utils.MLFLOW_LOCAL_BACKEND_RUN_ID_CONFIG


def call_method(method: t.Union[t.Callable, str], *args, **kwargs) -> t.Any:
    """A general function to call any given MLflow method.

    Parameters
    ----------
    method : Callable or str
        MLflow method to invoke.

        If `str`, only the method name is requried, e.g.
        for `mlflow.log_param`, `method="log_param"` is required.

    args
        Passed to the MLflow method.
    kwargs
        Passed to the MLflow method.

    Examples
    --------
    With the mlflow method:

    >>> import mantik.mlflow
    >>> import mlflow
    >>> mantik.mlflow.call_method(mlflow.log_param, key="<name>", value="<value>")  # noqa: E501

    or with a `str`:

    >>> import mantik.mlflow as mlflow
    >>> mlflow.call_method("log_param", key="<name>", value="<value>")  # noqa: E501

    Returns
    -------
    The returned instance of the MLflow method.

    """
    if isinstance(method, str):
        method = getattr(mlflow, method)

    try:
        return method(*args, **kwargs)
    except mlflow.exceptions.MlflowException:
        logger.exception(
            "Calling mlflow.%s with args=%s and kwargs=%s has failed",
            method.__name__,
            args,
            kwargs,
            exc_info=True,
        )
        return None
