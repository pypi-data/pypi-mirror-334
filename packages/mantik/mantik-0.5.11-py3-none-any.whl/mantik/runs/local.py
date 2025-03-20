import dataclasses
import io
import logging
import os
import pathlib
import sys
import tempfile
import typing as t
import uuid

import mantik.authentication.auth
import mantik.authentication.tokens as tokens
import mantik.runs.schemas as schemas
import mantik.utils.env_vars as env_vars
import mantik.utils.mantik_api as mantik_api
import mantik.utils.mantik_api.code_repository as code_api
import mantik.utils.mantik_api.connection as connection_api
import mantik.utils.mantik_api.experiment_repository as experiment_api
from mantik.utils.other import construct_git_clone_uri

logger = logging.getLogger(__name__)


def start_local_run(
    project_id: uuid.UUID,
    name: str,
    experiment_repository_id: uuid.UUID,
    code_repository_id: t.Optional[uuid.UUID],
    branch: t.Optional[str],
    commit: t.Optional[str],
    data_repository_id: t.Optional[uuid.UUID],
    mlflow_mlproject_file_path: str,
    entry_point: str,
    data_branch: t.Optional[str],
    data_commit: t.Optional[str],
    data_target_dir: t.Optional[str],
    env_manager: t.Optional[str],
    mlflow_parameters: dict,
):
    """

    Parameters
    ----------
    project_id : ID of the project to which the run should be linked
    name : Name of the Run
    experiment_repository_id : ID of the experiment repository
        to which the run should be linked
    code_repository_id : ID of the code repository
        where the mlproject is located
    branch : Name of the code repository's branch
    commit : Name of the code repository's commit (has precedence over branch)
    data_repository_id : ID of the data repository
        where the data is located, this is optional
    mlflow_mlproject_file_path : Path in your code directory
        to the MLproject file
    entry_point : entry point name
    mlflow_parameters : Mlflow parameters present in your entry point
    data_branch : Data branch to checkout. Defaults to newest.
    data_commit : Data commit to checkout. Takes precedence over data_branch.
    env_manager: Which environment manager to use to handle installing run
    dependencies. Could be Local, Conda or Virtualenv
    data_target_dir : Relative path to directory
        where the data will be stored (from code root)

    Returns
    -------
    Response from the mantik API that contains the run id
    """
    token = mantik.authentication.auth.get_valid_access_token()
    run(
        data=schemas.RunConfiguration(
            name=name,
            experiment_repository_id=experiment_repository_id,
            code_repository_id=code_repository_id,
            branch=branch,
            commit=commit,
            data_repository_id=data_repository_id,
            data_branch=data_branch,
            data_commit=data_commit,
            mlflow_mlproject_file_path=mlflow_mlproject_file_path,
            entry_point=entry_point,
            mlflow_parameters=mlflow_parameters,
            backend_config={},
        ),
        data_target_dir=data_target_dir,
        project_id=project_id,
        mantik_token=token,
        env_manager=env_manager,
    )


@dataclasses.dataclass
class LocalRunOutput:
    run_id: uuid.UUID
    exception: t.Optional[BaseException] = None


class LocalRunManager:
    """
    The purpose of this class is so that the two functions inside it
    can be more easily monkey-patched together,
    feel free to improve this by monkeypatching the functions
    without the need of an extra class to clean up the code
    """

    def __init__(self):
        pass

    @classmethod
    def clone_git_repo(
        cls,
        uri: str,  # public or private
        branch: str,
        target_directory: str,
    ) -> None:
        try:
            import git
        except ModuleNotFoundError as e:
            raise RuntimeError(
                "Please install git module: required to execute local runs"
            ) from e

        logger.debug("Cloning repo...")

        git.Repo.clone_from(uri, target_directory, branch=branch)

        logger.debug("Repo cloned.")

    @staticmethod
    def start_local_run(
        mlflow_experiment_id: str,
        data: schemas.RunConfiguration,
        project_id: uuid.UUID,
        mantik_token: str,
        uri: str,
        env_manager: str = "local",
    ) -> LocalRunOutput:
        # Lazy import so that mantik can be used without mlflow
        import mlflow
        import mantik.mlflow
        import mantik.runs.mlflow_monkeypatch

        # NOTE: If additional mlflow functions need to be monkeypatched,
        # add them to the mlflow_monkeypatch module.
        #
        # - Monkeypatched run_mlflow_run_cmd and run_entry_point
        #   to capture output.
        #
        # Reason: We want to display the logs of a run in the Mantik UI.
        # Since mlflow does not support saving the logs of subprocesses
        # (this might change: https://github.com/mlflow/mlflow/issues/863,
        # but it may only apply to the main process logs),
        # we need to modify how stdout and stderr of the subprocess are handled
        # to capture them for display in the Mantik UI.

        mlflow.projects.backend.local._run_mlflow_run_cmd = (
            mantik.runs.mlflow_monkeypatch.run_mlflow_run_cmd
        )
        mlflow.projects.backend.local._run_entry_point = (
            mantik.runs.mlflow_monkeypatch.run_entry_point
        )

        logger.info(f"Starting mlflow run: '{data.name}' ...")
        mlflow.set_tracking_uri(
            os.getenv(
                mantik.utils.mlflow.TRACKING_URI_ENV_VAR,
                mantik.utils.mlflow.DEFAULT_TRACKING_URI,
            )
        )
        with mantik.mlflow.start_run(
            experiment_id=mlflow_experiment_id,
            run_name=data.name,
        ) as active_run:
            data.mlflow_run_id = active_run.info.run_id
            run_id = save_run_data(
                data=data, project_id=project_id, mantik_token=mantik_token
            )
            mantik_api.run.update_run_status(
                project_id=project_id,
                token=mantik_token,
                status=active_run.info.status,
                run_id=run_id,
            )
        try:
            _run = mlflow.run(
                uri=uri,
                backend="local",
                experiment_id=mlflow_experiment_id,
                run_name=data.name,
                entry_point=data.entry_point,
                parameters=data.mlflow_parameters,
                backend_config={
                    mantik.mlflow.get_local_backend_config_run_id_env_var(): active_run.info.run_id  # noqa: E501
                },
                env_manager=env_manager,
                build_image=True,
                docker_args={
                    "e": f"{mantik.utils.mlflow.TRACKING_TOKEN_ENV_VAR}={os.environ[mantik.utils.mlflow.TRACKING_TOKEN_ENV_VAR]}"  # noqa: E501
                },
            )
        except KeyboardInterrupt as e:
            logger.warning(
                "Keyboard interrupt, setting Mantik run status to KILLED"
            )
            mantik_api.run.update_run_status(
                project_id=project_id,
                token=mantik_token,
                status="KILLED",
                run_id=run_id,
            )
            return LocalRunOutput(run_id, exception=e)
        # MlflowException is raised when something goes wrong with mlflow
        # FileNotFoundError is raised when pyenv or conda are not found
        # This catches any other exception
        # so that we can in any case push the logs and update the status
        except Exception as e:
            logger.warning(
                "Failed to execute run, setting Mantik run status to FAILED"
            )
            mantik_api.run.update_run_status(
                project_id=project_id,
                token=mantik_token,
                status="FAILED",
                run_id=run_id,
            )
            return LocalRunOutput(run_id, exception=e)
        logger.debug("Run finished successfully")
        mantik_api.run.update_run_status(
            project_id=project_id,
            token=mantik_token,
            status=_run.get_status(),
            run_id=run_id,
        )
        return LocalRunOutput(run_id)


def fetch_code_and_experiment(
    project_id: uuid.UUID,
    code_repository_id: uuid.UUID,
    experiment_repository_id: uuid.UUID,
    mantik_token: str,
) -> t.Tuple[code_api.CodeRepository, experiment_api.ExperimentRepository]:
    logger.debug("Fetching code and experiment from Mantik API...")
    code = code_api.get_one(
        code_repository_id=code_repository_id,
        project_id=project_id,
        token=mantik_token,
    )
    experiment = experiment_api.get_one(
        experiment_repository_id=experiment_repository_id,
        project_id=project_id,
        token=mantik_token,
    )
    logger.debug(f"Fetched {code} and {experiment}")
    logger.debug(f"Code repo uri: {code.uri}")
    return code, experiment


def save_run_data(
    data: schemas.RunConfiguration, project_id: uuid.UUID, mantik_token: str
) -> uuid.UUID:
    logger.debug(f"Saving data... {data}")

    response = mantik_api.run.save_run(
        project_id=project_id,
        run_data=data.to_post_payload(),
        token=mantik_token,
    )

    logger.debug("Results saved to Mantik API")
    return uuid.UUID(response.json()["runId"])


def run(
    data: schemas.RunConfiguration,
    project_id: uuid.UUID,
    mantik_token: str,
    data_target_dir: t.Optional[str] = None,
    run_manager: LocalRunManager = LocalRunManager(),
    env_manager: t.Optional[str] = "local",
):
    notebook_type = mantik_api.run.check_notebook_type()
    code, experiment = fetch_code_and_experiment(
        project_id=project_id,
        code_repository_id=data.code_repository_id,
        experiment_repository_id=data.experiment_repository_id,
        mantik_token=mantik_token,
    )

    data.name = experiment_api.get_unique_run_name(
        experiment_repository_id=data.experiment_repository_id,
        project_id=project_id,
        token=mantik_token,
        run_name=data.name,
    )
    git_connection = (
        connection_api.get(
            user_id=uuid.UUID(tokens.get_user_id_from_token(mantik_token)),
            connection_id=uuid.UUID(code.connection_id),
            token=mantik_token,
        )
        if code.connection_id
        else None
    )
    uri = code.uri
    if (
        git_connection
    ):  # means that the git is private, therefore token needs to be injected
        uri = construct_git_clone_uri(
            uri=uri,
            git_access_token=git_connection.token,
            platform=code.platform,
        )
    with tempfile.TemporaryDirectory() as temp_dir:
        run_manager.clone_git_repo(
            uri=uri,
            branch=data.commit or data.branch,
            target_directory=temp_dir,
        )

        with mantik.utils.env.env_vars_overwrite_temporarily(
            get_env_vars_for_run(
                run_config=data,
                mantik_token=mantik_token,
                project_id=str(project_id),
                data_target_dir=data_target_dir,
            )
        ):
            start_local_run_output, captured_output = capture_and_print_output(
                func=run_manager.start_local_run,
                uri=path_directory_of_mlproject_file(
                    str(
                        pathlib.Path(temp_dir).joinpath(
                            data.mlflow_mlproject_file_path
                        )
                    )
                ),
                data=data,
                mlflow_experiment_id=experiment.mlflow_experiment_id,
                mantik_token=mantik_token,
                project_id=project_id,
                env_manager=env_manager,
            )
        if notebook_type:
            mantik_api.run.update_notebook_source(
                project_id=project_id,
                run_id=start_local_run_output.run_id,
                token=mantik_token,
                notebook_source=mantik_api.run.NoteBookSource.create_instance(
                    provider=notebook_type
                ),
            )
        mantik_api.run.update_logs(
            project_id=project_id,
            token=mantik_token,
            logs=captured_output,
            run_id=start_local_run_output.run_id,
        )

        if start_local_run_output.exception:
            raise start_local_run_output.exception


def path_directory_of_mlproject_file(mlproject_file_path: str) -> str:
    return str(pathlib.Path(mlproject_file_path).parent)


class Tee(io.StringIO):
    """
    Like the tee linux command that prints to stdout
    and save to a/multiple file the output of a command.
    This class takes n streams and populates them with the same data.
    A stream could be sys.stdout or sys.stderr, to keep printing to them.
    """

    def __init__(self, *streams):
        super().__init__()
        self.streams = streams

    def write(self, data):
        for stream in self.streams:
            stream.write(data)
        super().write(data)

    def flush(self):
        for stream in self.streams:
            stream.flush()
        super().flush()


def capture_and_print_output(func, *args, **kwargs) -> t.Tuple[t.Any, str]:
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    output = io.StringIO()

    tee_stdout = Tee(sys.stdout, output)
    tee_stderr = Tee(sys.stderr, output)
    sys.stdout = tee_stdout
    sys.stderr = tee_stderr

    try:
        result = func(*args, **kwargs)
    finally:
        # Restore original stdout and stderr
        sys.stdout = original_stdout
        sys.stderr = original_stderr

    captured_output = output.getvalue()
    return result, captured_output


def get_env_vars_for_run(
    run_config: schemas.RunConfiguration,
    mantik_token: str,
    project_id: str,
    data_target_dir: t.Optional[str] = None,
) -> dict:
    entrypoint_env_vars = {
        env_vars.MANTIK_ACCESS_TOKEN_ENV_VAR: mantik_token,
        env_vars.PROJECT_ID_ENV_VAR: project_id,
    }

    if not run_config.data_repository_id:
        return entrypoint_env_vars

    entrypoint_env_vars[env_vars.DATA_REPOSITORY_ID_ENV_VAR] = str(
        run_config.data_repository_id
    )

    if run_config.data_branch:
        entrypoint_env_vars[
            env_vars.DATA_REPOSITORY_BRANCH_ENV_VAR
        ] = run_config.data_branch

    if run_config.data_commit:
        entrypoint_env_vars[
            env_vars.DATA_REPOSITORY_COMMIT_ENV_VAR
        ] = run_config.data_commit

    if not data_target_dir:
        raise ValueError(
            "Required to specify `data_target_dir` if data used for local run!"
        )

    entrypoint_env_vars[env_vars.TARGET_DIR_ENV_VAR] = data_target_dir

    return entrypoint_env_vars
