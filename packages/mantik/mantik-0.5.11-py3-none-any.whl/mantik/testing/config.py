import pathlib
import typing as t

import mantik.config as config
import mantik.utils.credentials as _credentials

MLFLOW_ENV_TEST_ENV_VAR = "MLFLOW_TESTING_MANTIK_TEST_VAR"

_BASE_ENV_VARS = [
    config.core.COMPUTE_BUDGET_ACCOUNT_ENV_VAR,
    MLFLOW_ENV_TEST_ENV_VAR,
]
ALL_UNICORE_ENV_VARS = [
    _credentials.UNICORE_USERNAME_ENV_VAR,
    _credentials.UNICORE_PASSWORD_ENV_VAR,
    config.core.COMPUTE_BUDGET_ACCOUNT_ENV_VAR,
    MLFLOW_ENV_TEST_ENV_VAR,
]
ALL_FIRECREST_ENV_VARS = [
    _credentials.FIRECREST_CLIENT_ID_ENV_VAR,
    _credentials.FIRECREST_CLIENT_SECRET_ENV_VAR,
    config.core.COMPUTE_BUDGET_ACCOUNT_ENV_VAR,
    MLFLOW_ENV_TEST_ENV_VAR,
]

DEFAULT_ENV_VAR_VALUE = "test-val"

EXISTING_FILE = (
    pathlib.Path(__file__).parent / "../../../resources/test-project/recipe.def"
).as_posix()


def _create_apptainer_environment(
    path: pathlib.Path,
    type: str = None,
    variables: t.Optional[t.Dict] = None,
    modules: t.Optional[t.List] = None,
    pre_run_command_on_login_node: t.Optional[list] = None,
    pre_run_command_on_compute_node: t.Optional[list] = None,
    post_run_command_on_compute_node: t.Optional[list] = None,
    post_run_command_on_login_node: t.Optional[list] = None,
    include_mlflow_env_vars: bool = True,
) -> config.environment.Environment:
    if type is None:
        type = "local"
    if include_mlflow_env_vars:
        variables = _include_mlflow_env_vars(variables)

    return config.environment.Environment(
        execution=config.executable.Apptainer(
            path=path,
            type=type,
        ),
        variables=variables,
        modules=modules,
        pre_run_command_on_login_node=pre_run_command_on_login_node,
        pre_run_command_on_compute_node=pre_run_command_on_compute_node,
        post_run_command_on_compute_node=post_run_command_on_compute_node,
        post_run_command_on_login_node=post_run_command_on_login_node,
    )


def _create_python_environment(
    path: pathlib.Path,
    variables: t.Optional[t.Dict] = None,
    modules: t.Optional[t.List] = None,
    pre_run_command_on_login_node: t.Optional[list] = None,
    pre_run_command_on_compute_node: t.Optional[list] = None,
    post_run_command_on_compute_node: t.Optional[list] = None,
    post_run_command_on_login_node: t.Optional[list] = None,
    include_mlflow_env_vars: bool = True,
) -> config.environment.Environment:
    if include_mlflow_env_vars:
        variables = _include_mlflow_env_vars(variables)

    return config.environment.Environment(
        config.executable.Python(
            path=path,
        ),
        variables=variables,
        modules=modules,
        pre_run_command_on_login_node=pre_run_command_on_login_node,
        pre_run_command_on_compute_node=pre_run_command_on_compute_node,
        post_run_command_on_compute_node=post_run_command_on_compute_node,
        post_run_command_on_login_node=post_run_command_on_login_node,
    )


def _include_mlflow_env_vars(env_variables: t.Optional[t.Dict]) -> t.Dict:
    mlflow_env_vars = {
        MLFLOW_ENV_TEST_ENV_VAR: DEFAULT_ENV_VAR_VALUE,
    }
    if env_variables is None:
        env_variables = mlflow_env_vars
    else:
        env_variables = {**env_variables, **mlflow_env_vars}
    return env_variables


def _create_config_with_unicore(
    resources: config.resources.Resources,
    unicore_api_url: str = "test-url",
    user: str = "test-val",
    password: str = "test-val",
    project: str = "test-val",
    env: t.Optional[config.environment.Environment] = None,
) -> config.core.Config:
    env = _get_env_vars(env)
    return config.core.Config(
        unicore_api_url=unicore_api_url,
        user=user,
        password=password,
        project=project,
        resources=resources,
        environment=env,
    )


def _get_env_vars(
    env: t.Optional[config.environment.Environment] = None,
) -> config.environment.Environment:
    if env is None:
        env = config.environment.Environment()
    env.variables = _include_mlflow_env_vars(env.variables)
    return env


def _create_config_with_firecrest(
    resources: config.resources.Resources,
    api_url: str = "test-api-url",
    token_url: str = "test-token-url",
    machine: str = "test-machine",
    user: str = "test-val",
    password: str = "test-val",
    project: str = "test-val",
    env: t.Optional[config.environment.Environment] = None,
) -> config.core.Config:
    env = _get_env_vars(env)
    return config.core.Config(
        firecrest=config.firecrest.Firecrest(
            api_url=api_url, token_url=token_url, machine=machine
        ),
        user=user,
        password=password,
        project=project,
        resources=resources,
        environment=env,
    )
