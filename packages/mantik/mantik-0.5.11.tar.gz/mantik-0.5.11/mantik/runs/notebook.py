import os
import typing as t


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


import mantik
import uuid
import contextvars
import mlflow
import mantik.runs
import mantik.runs.schemas
import mantik.utils.mantik_api.experiment_repository as experiment_api
import mantik.mlflow
import mantik.utils.mantik_api as mantik_api
import mantik.utils.env_vars as env_vars


active_run_ctx = contextvars.ContextVar("active_run")
project_id_ctx = contextvars.ContextVar("project_id")
run_id_ctx = contextvars.ContextVar("run_id")


def start_run(
    run_name: str,
    project_id: t.Optional[uuid.UUID] = None,
    experiment_repository_id: t.Optional[uuid.UUID] = None,
    nested: bool = False,
):
    """
    Start a new MLflow run with Mantik integration.

    This function initiates a new MLflow tracking run and registers it with
    Mantik.
    It handles run configuration, infrastructure tracking, and notebook
    source detection.

    Parameters
    ----------
    run_name : str
       Name of the run to be created.
    project_id : Optional[uuid.UUID], default=None
       UUID of the project to associate the run with.
       If not provided, will attempt to read from the PROJECT_ID environment
        variable.
    experiment_repository_id : Optional[uuid.UUID], default=None
       UUID of the experiment repository to associate the run with.
       If not provided, will attempt to read from the
       EXPERIMENT_RESPOSITORY_ID environment variable.
    nested : bool, default=False
       If True, creates a nested run within an active parent run.

    Returns
    -------
    mlflow.ActiveRun
       The active MLflow run object that was started.

    Raises
    ------
    ValueError
       If project_id or experiment_repository_id cannot be determined from
       arguments or environment variables.
    Notes
    -----
    Requires the MLFLOW_TRACKING_TOKEN environment variable to be set.
    """

    try:
        project_id = project_id or os.environ[env_vars.PROJECT_ID_ENV_VAR]
        experiment_repository_id = (
            experiment_repository_id
            or os.environ[env_vars.EXPERIMENT_REPOSITORY_ID_ENV_VAR]
        )
    except KeyError as e:
        raise RuntimeError(
            f"mantik.start_run() requires environment variable" f" {e}"
        )

    experiment = experiment_api.get_one(
        experiment_repository_id=experiment_repository_id,
        project_id=project_id,
        token=os.environ["MLFLOW_TRACKING_TOKEN"],
    )
    project_id_ctx.set(project_id)

    mantik_token = os.environ["MLFLOW_TRACKING_TOKEN"]
    data = mantik.runs.schemas.RunConfiguration(
        name=run_name,
        experiment_repository_id=uuid.UUID(
            os.environ["MANTIK_EXPERIMENT_REPOSITORY_ID"]
        ),
    )

    active_run = mlflow.start_run(
        experiment_id=experiment.mlflow_experiment_id,
        run_name=run_name,
        nested=nested,
    )
    active_run_ctx.set(active_run)
    data.backend_config = {}
    data.mlflow_run_id = active_run.info.run_id
    run_id = mantik.runs.local.save_run_data(
        data=data, project_id=project_id, mantik_token=mantik_token
    )
    run_id_ctx.set(run_id)

    mantik_api.run.update_run_infrastructure(
        project_id=project_id,
        run_id=run_id,
        token=mantik_token,
        infrastructure=mantik_api.run.RunInfrastructure.from_system(),
    )

    notebook_type = mantik_api.run.check_notebook_type()
    if notebook_type:
        mantik_api.run.update_notebook_source(
            project_id=project_id,
            run_id=run_id,
            token=mantik_token,
            notebook_source=mantik_api.run.NoteBookSource.create_instance(
                provider=notebook_type
            ),
        )

    mantik.utils.mantik_api.run.update_run_status(
        project_id=project_id,
        token=mantik_token,
        status=active_run.info.status,
        run_id=run_id,
    )

    return active_run


def end_run(status: str = "FINISHED") -> None:
    mantik_token = os.environ["MLFLOW_TRACKING_TOKEN"]
    active_run = active_run_ctx.get()
    project_id = project_id_ctx.get()
    run_id = run_id_ctx.get()

    if active_run is None:
        raise RuntimeError(
            "No active run found. Did you call mantik.start_run(" ")?"
        )

    mlflow.end_run(status=status)

    return mantik.utils.mantik_api.run.update_run_status(
        project_id=project_id,
        token=mantik_token,
        status=status,
        run_id=run_id,
    )


def log_param(key: str, value: t.Any) -> t.Any:
    return mlflow.log_param(key=key, value=value)


def log_params(params: t.Dict[str, t.Any]) -> None:
    return mlflow.log_params(params=params)


def log_metrics(
    metrics: t.Dict[str, float], step: t.Optional[int] = None
) -> None:
    return mlflow.log_metrics(metrics=metrics, step=step)


def log_metric(key: str, value: float, step: t.Optional[int] = None) -> None:
    return mlflow.log_metric(key=key, value=value, step=step)


def log_dict(dictionary: t.Any, artifact_file: str) -> None:
    return mlflow.log_dict(dictionary=dictionary, artifact_file=artifact_file)


def log_text(text: str, artifact_file: str) -> None:
    return mlflow.log_text(text=text, artifact_file=artifact_file)


def log_artifact(
    local_path: str, artifact_path: t.Optional[str] = None
) -> None:
    return mlflow.log_artifact(
        local_path=local_path, artifact_path=artifact_path
    )


def log_artifacts(
    local_dir: str, artifact_path: t.Optional[str] = None
) -> None:
    return mlflow.log_artifacts(
        local_dir=local_dir, artifact_path=artifact_path
    )


def autolog(
    log_input_examples: bool = False,
    log_model_signatures: bool = True,
    log_models: bool = True,
    disable: bool = False,
    exclusive: bool = False,
    disable_for_unsupported_versions: bool = False,
    silent: bool = False,
) -> None:
    return mlflow.autolog(
        log_input_examples=log_input_examples,
        log_model_signatures=-log_model_signatures,
        log_models=log_models,
        disable=disable,
        exclusive=exclusive,
        disable_for_unsupported_versions=disable_for_unsupported_versions,
        silent=silent,
    )
