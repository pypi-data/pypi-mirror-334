import pathlib
import typing as t
import uuid

import mantik.authentication.auth
import mantik.runs.schemas as schemas
import mantik.utils.mantik_api as mantik_api


def submit_run(
    project_id: uuid.UUID,
    name: str,
    experiment_repository_id: uuid.UUID,
    code_repository_id: uuid.UUID,
    branch: t.Optional[str],
    commit: t.Optional[str],
    data_repository_id: t.Optional[uuid.UUID],
    data_branch: t.Optional[str],
    data_commit: t.Optional[str],
    mlflow_mlproject_file_path: str,
    entry_point: str,
    mlflow_parameters: dict,
    backend_config: t.Union[pathlib.Path, str, dict],
    connection_id: t.Optional[uuid.UUID],
    compute_budget_account: t.Optional[str],
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
    data_branch : Data branch to checkout. Defaults to newest.
    data_commit : Data commit to checkout. Takes precedence over data_branch.
    mlflow_mlproject_file_path : Path in your code directory
        to the MLproject file
    entry_point : entry point name
    mlflow_parameters : Mlflow parameters present in your entry point
    backend_config : path to backend configuration file
        relative to path from where this command is called.
        It has to be a local file.
    connection_id : Mantik Connection UUID
    compute_budget_account : Name of the compute budget account on HPC

    Returns
    -------
    Response from the mantik API that contains the run id
    """
    run_configuration = schemas.RemoteRunConfiguration(
        name=name,
        experiment_repository_id=experiment_repository_id,
        data_repository_id=data_repository_id,
        data_branch=data_branch,
        data_commit=data_commit,
        code_repository_id=code_repository_id,
        branch=branch,
        commit=commit,
        connection_id=connection_id,
        compute_budget_account=compute_budget_account,
        mlflow_mlproject_file_path=mlflow_mlproject_file_path,
        entry_point=entry_point,
        mlflow_parameters=mlflow_parameters,
        backend_config=backend_config,
    )

    token = mantik.authentication.auth.get_valid_access_token()
    response = mantik_api.run.submit_run(
        project_id=project_id,
        submit_run_data=run_configuration.to_post_payload(),
        token=token,
    )
    return response
