import copy
import dataclasses
import os
import pathlib
import re
import typing as t

import mantik.config._base as _base
import mantik.config._utils as _utils
import mantik.config.exceptions as exceptions
import mantik.config.executable as _executable
import mantik.config.resources as _resources
import mantik.utils as utils
import mantik.utils.mlflow as mlflow

_MLFLOW_ENV_VAR_PREFIX = "MLFLOW_"
_ALLOWED_EXECUTABLES = {
    "Apptainer": _executable.Apptainer,
    "Python": _executable.Python,
}


@dataclasses.dataclass
class Environment(_base.ConfigObject):
    """Part of the backend-config where all variables
    concerning the running environment are stored."""

    execution: t.Optional[_executable.Execution] = None
    variables: t.Optional[t.Dict] = None
    modules: t.Optional[t.List] = None
    pre_run_command_on_login_node: t.Optional[list] = None
    pre_run_command_on_compute_node: t.Optional[list] = None
    post_run_command_on_compute_node: t.Optional[list] = None
    post_run_command_on_login_node: t.Optional[list] = None

    @classmethod
    def _from_dict(cls, config: t.Dict) -> "Environment":
        execution = _get_execution_environment(config)
        variables = _utils.get_optional_config_value(
            name="Variables",
            value_type=dict,
            config=config,
        )
        modules = _utils.get_optional_config_value(
            name="Modules",
            value_type=list,
            config=config,
        )

        preRunCommandOnLoginNode = _utils.get_optional_config_value(
            name="PreRunCommandOnLoginNode",
            value_type=list,
            config=_cast_run_command_str_to_list(
                config, "PreRunCommandOnLoginNode"
            ),
        )
        preRunCommandOnComputeNode = _utils.get_optional_config_value(
            name="PreRunCommandOnComputeNode",
            value_type=list,
            config=_cast_run_command_str_to_list(
                config, "PreRunCommandOnComputeNode"
            ),
        )
        postRunCommandOnComputeNode = _utils.get_optional_config_value(
            name="PostRunCommandOnComputeNode",
            value_type=list,
            config=_cast_run_command_str_to_list(
                config, "PostRunCommandOnComputeNode"
            ),
        )
        postRunCommandOnLoginNode = _utils.get_optional_config_value(
            name="PostRunCommandOnLoginNode",
            value_type=list,
            config=_cast_run_command_str_to_list(
                config, "PostRunCommandOnLoginNode"
            ),
        )

        return cls(
            execution=execution,
            modules=modules,
            variables=variables,
            pre_run_command_on_login_node=preRunCommandOnLoginNode,
            pre_run_command_on_compute_node=preRunCommandOnComputeNode,
            post_run_command_on_compute_node=postRunCommandOnComputeNode,
            post_run_command_on_login_node=postRunCommandOnLoginNode,
        )

    def __post_init__(self):
        """Add all MLflow environment variables to the environment."""
        self.variables = _add_mlflow_env_vars(self.variables)

    def _to_dict(self) -> t.Dict:
        return {
            "Environment": self.variables,
            "User precommand": self._create_login_node_command(
                self.pre_run_command_on_login_node
            ),
            "RunUserPrecommandOnLoginNode": True,
            "Arguments": [],
            "User postcommand": self._create_login_node_command(
                self.post_run_command_on_login_node
            ),
            "RunUserPostcommandOnLoginNode": True,
        }

    def _create_login_node_command(
        self, commands: t.Optional[list]
    ) -> t.Optional[str]:
        # Login node commands are only allowed by UNICORE, and it allows
        # only single strings as commands. Thus, we concatenate multiple
        # commands using `&&`. This makes the command fail if any of
        # the given commands fails.
        return _concatenate_commands(commands, concatenation_str=" && ")

    def _create_compute_node_command(
        self, commands: t.Optional[list]
    ) -> t.Optional[str]:
        return _concatenate_commands(commands, concatenation_str="\n")

    def _create_pre_run_command_on_compute_node(self) -> t.Optional[str]:
        # Venv MUST be loaded before modules
        # see https://gitlab.com/mantik-ai/mantik/issues/140
        return (
            self._create_compute_node_command(
                [
                    self._create_modules_command(),
                    *self.pre_run_command_on_compute_node,
                ],
            )
            if self.pre_run_command_on_compute_node
            else self._create_modules_command()
        )

    def _create_modules_command(self) -> t.Optional[str]:
        return f"module load {' '.join(self.modules)}" if self.modules else None

    def _create_execution_command(self) -> t.Optional[str]:
        if self.execution is not None:
            execution_command = self.execution.get_execution_command()
            arguments = self.execution.get_arguments()
            joined_str = " ".join(filter(None, [execution_command, arguments]))
            return joined_str or None

    def set_srun_cpus_per_task_if_unset(
        self, resources: _resources.Resources
    ) -> "Environment":
        cpus_per_task = resources.cpus_per_node

        if cpus_per_task is not None:
            if self.variables is None:
                self.variables = {"SRUN_CPUS_PER_TASK": str(cpus_per_task)}
            elif (
                self.variables is not None
                and "SRUN_CPUS_PER_TASK" not in self.variables
            ):
                self.variables["SRUN_CPUS_PER_TASK"] = str(cpus_per_task)

        return self

    def _create_execution_command_with_arguments(
        self, entry_point_arguments
    ) -> str:
        if isinstance(self.execution, _executable.Apptainer):
            # For Apptainer, the `apptainer run` command needs
            # to be joined with the MLproject entry point command
            # with a space to get e.g.
            # `apptainer run image.sif python main.py ...`
            concatenation_string = " "
        else:
            # For Python, the `source <path to venv>/bin/activate`
            # command needs to be joined with the MLproject entry
            # point command using `&&` to get
            # `source /path/venv/bin/activate && python main.py ...`
            # (Using `;` will let the job succeed even if one of the
            # commands fails.)
            concatenation_string = " && "
        execution_command_arguments_string = concatenation_string.join(
            filter(
                None, [self._create_execution_command(), entry_point_arguments]
            )
        )
        list_to_join = [
            self._create_pre_run_command_on_compute_node(),
            execution_command_arguments_string,
            self._create_compute_node_command(
                self.post_run_command_on_compute_node
            ),
        ]
        return " && ".join(filter(None, list_to_join))

    def to_unicore_job_description(self, bash_script_name: str) -> t.Dict:
        """Convert to UNICORE job description.

        Parameters
        ----------
        arguments : str
            Arguments to pass to the executable.

        Returns
        -------
        dict
            The UNICORE job description.

            For details see https://sourceforge.net/p/unicore/wiki/Job_Description  # noqa: E501


        """
        job_description = {
            **self.to_dict(),
            "Executable": f'source $(dirname "$(realpath "$0")")/{bash_script_name}',  # noqa E501
        }
        job_description["Environment"] = job_description.get("Environment", {})
        job_description["Environment"].update(
            {"MANTIK_WORKING_DIRECTORY": "$UC_WORKING_DIRECTORY"}
        )

        return job_description

    def execution_given(self) -> bool:
        return self.execution is not None

    def add_env_vars(self, env_vars: t.Dict) -> None:
        if self.variables is None:
            self.variables = env_vars
        else:
            self.variables.update(env_vars)

    def to_slurm_batch_script(
        self, entry_point_arguments: str, run_dir: pathlib.Path
    ) -> str:
        # Setting env vars via the firecREST API is only supported from
        # version >= v1.14.0. Hence, we set them explicitly.
        env_vars_list = [f"export MANTIK_WORKING_DIRECTORY={run_dir}"]
        if self.variables is not None:
            env_vars_list.extend(
                [
                    f"export {key}={value}"
                    for key, value in self.variables.items()
                ]
            )
        env_vars_str = _concatenate_commands(env_vars_list, "\n")

        job_script = _concatenate_commands(
            commands=[
                env_vars_str,
                self._create_execution_command_with_arguments(
                    entry_point_arguments
                ),
            ],
            concatenation_str="\n",
        )
        return job_script

    def to_bash_script(self, entry_point_arguments: str) -> str:
        """Create a bash script for UNICORE."""
        job_script = _concatenate_commands(
            commands=[
                "echo 'Submitted bash script'",
                'cat "$(realpath "$0")"',
                self._create_execution_command_with_arguments(
                    entry_point_arguments
                ),
            ],
            concatenation_str="\n",
        )
        return job_script


def _get_execution_environment(
    config: t.Dict,
) -> t.Optional[_executable.Execution]:
    envs = [env for env in _ALLOWED_EXECUTABLES if env in config]
    execution = _get_only_one_environment_or_none(envs)
    if execution is not None:
        return execution.from_dict(config)
    return


def _get_only_one_environment_or_none(
    env_found: t.List,
) -> t.Optional[t.Type[_executable.Execution]]:
    if not env_found:
        return None
    elif len(env_found) > 1:
        raise exceptions.ConfigValidationError(
            "Only one execution environment is allowed, "
            "but in config these have been found: "
            f"{utils.formatting.iterable_to_string(env_found)}."
        )

    try:
        return _ALLOWED_EXECUTABLES[env_found[0]]
    except KeyError as e:
        raise ValueError(
            f"Environment of type {env_found} not supported"
        ) from e


def _add_mlflow_env_vars(environment: t.Optional[t.Dict]) -> t.Optional[t.Dict]:
    mlflow_env_vars = _get_mlflow_env_vars()
    if mlflow_env_vars:
        if environment is None:
            return mlflow_env_vars
        return {**mlflow_env_vars, **environment}
    return environment


def _get_mlflow_env_vars() -> t.Dict:
    pattern = re.compile(rf"{_MLFLOW_ENV_VAR_PREFIX}\w+")
    return {
        key: value
        for key, value in os.environ.items()
        if pattern.match(key) and key not in mlflow.CONFLICTING_ENV_VARS
    }


def _concatenate_commands(
    commands: t.Optional[list], concatenation_str: str
) -> t.Optional[str]:
    return concatenation_str.join(filter(None, commands)) if commands else None


def _cast_run_command_str_to_list(
    config: t.Dict, run_command_name: str
) -> t.Dict:
    """
    Converts the Pre/PostRunCommands specified in the config from a string
    to list format. This ensures the backward compatibility with configs
    that allow strings in the run commands.
    """
    config = copy.deepcopy(config)
    run_command_value = config.get(run_command_name, None)
    if run_command_value is not None:
        if isinstance(run_command_value, str):
            config[run_command_name] = [run_command_value]
            return config
        elif isinstance(run_command_value, list):
            config[run_command_name] = [
                str(command) for command in run_command_value
            ]
            return config
        else:
            raise exceptions.ConfigValidationError(
                f"Config value for {run_command_name!r} has to be of type str "
                "or list"
            )
    return config
