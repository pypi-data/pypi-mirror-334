import pathlib

import pytest
from mlflow.projects import _project_spec

import mantik.config.core as core
import mantik.config.exceptions as exceptions
import mantik.utils.credentials as _credentials
import mantik_compute_backend.backend as backend

FILE_PATH = pathlib.Path(__file__).parent

ALL_ENV_VARS = [
    _credentials.UNICORE_USERNAME_ENV_VAR,
    _credentials.UNICORE_PASSWORD_ENV_VAR,
    core.COMPUTE_BUDGET_ACCOUNT_ENV_VAR,
]


def test_ml_project_command_validation():
    entry_point = _project_spec.EntryPoint(
        name="main",
        parameters={
            "optional": {"default": "test", "type": "string"},
        },
        command=(
            "python main.py "
            "{optional} --nproc-per-node=$(${{SLURM_STEP_GPUS: -1}} + 1 )"
        ),
    )
    parameters = {"optional": "whatever"}
    storage_dir = "test-dir"

    backend._create_arguments(
        entry_point=entry_point,
        parameters=parameters,
        storage_dir=storage_dir,
    )


@pytest.mark.parametrize(
    ("entry_point", "user_parameters", "expected"),
    [
        (
            _project_spec.EntryPoint(
                name="main",
                parameters={
                    "required": {"type": "string"},
                    "optional": {"default": "test", "type": "string"},
                },
                command="python main.py {incorrect-parameter} {optional}",
            ),
            {"required": "whatever"},
            "Mismatch between entry point parameter names and parameter "
            "placeholders in the command: ['incorrect-parameter', 'required']. "
            "Please revise the MLproject file for "
            "typos or inconsistencies between parameter names and their "
            "corresponding placeholders in the command.",
        ),
        (
            _project_spec.EntryPoint(
                name="main",
                parameters={
                    "optional": {"default": "test", "type": "string"},
                },
                command=(
                    "python main.py "
                    "{optional} --nproc-per-node=$(${SLURM_STEP_GPUS: -1} + 1 )"
                ),
            ),
            {"optional": "whatever"},
            "Entry point command contains improperly formatted environment "
            "variable expansions: ['${SLURM_STEP_GPUS: -1}']. Ensure "
            "expansions use exactly two opening and closing braces, "
            "e.g. ${{ENV_VAR}}.",
        ),
    ],
    ids=[
        "incorrect parameter in command with optional parameter given",
        "expansion variable given with single curly braces",
    ],
)
def test_ml_project_command_validation_fails(
    entry_point, user_parameters, expected, expect_raise_if_exception
):
    storage_dir = "test-dir"

    with expect_raise_if_exception(
        exceptions.MLprojectFileValidationError()
    ) as e:
        backend._create_arguments(
            entry_point=entry_point,
            parameters=user_parameters,
            storage_dir=storage_dir,
        )
    result = str(e.value)
    assert result == expected


@pytest.mark.parametrize(
    ("entry_point", "user_parameters"),
    [
        (
            _project_spec.EntryPoint(
                name="main",
                parameters={
                    "required": {"type": "string"},
                    "optional": {"default": "test", "type": "string"},
                },
                command="python main.py {required} {optional}",
            ),
            {"required": "whatever"},
        ),
        (
            _project_spec.EntryPoint(
                name="main",
                parameters={
                    "required": {"type": "string"},
                    "optional": {"default": "test", "type": "string"},
                },
                command="python main.py {required} {optional}",
            ),
            {"required": "whatever", "optional": "whatever"},
        ),
    ],
    ids=[
        "required parameter given, optional parameter not given",
        "required and optional parameter given",
    ],
)
def test_validate_parameters_placeholders_entry_point(
    entry_point, user_parameters
):
    backend._validate_parameters_placeholders_entry_point(
        entry_point=entry_point, user_parameters=user_parameters
    )


@pytest.mark.parametrize(
    ("entry_point", "user_parameters", "expected"),
    [
        (
            _project_spec.EntryPoint(
                name="main",
                parameters={
                    "required": {"type": "string"},
                    "optional": {"default": "test", "type": "string"},
                },
                command="python main.py {incorrect-parameter} {optional}",
            ),
            {"required": "whatever"},
            "Mismatch between entry point parameter names and parameter "
            "placeholders in the command: ['incorrect-parameter', 'required']. "
            "Please revise the MLproject file for "
            "typos or inconsistencies between parameter names and their "
            "corresponding placeholders in the command.",
        ),
        (
            _project_spec.EntryPoint(
                name="main",
                parameters={
                    "required": {"type": "string"},
                    "optional": {"default": "test", "type": "string"},
                },
                command="python main.py {required} {optional}",
            ),
            {"incorrect-parameter": "whatever", "optional": "whatever"},
            "Mismatch between entry point parameters and entered parameters: "
            "['incorrect-parameter', 'required']. Please revise the MLproject "
            "file or your submit command for typos or inconsistencies",
        ),
    ],
    ids=[
        "typo in user parameter with optional parameter given",
        "incorrect parameter in command with optional parameter given",
    ],
)
def test_validate_parameters_placeholders_entry_point_fails(
    entry_point, user_parameters, expected, expect_raise_if_exception
):
    with expect_raise_if_exception(
        exceptions.MLprojectFileValidationError()
    ) as e:
        backend._validate_parameters_placeholders_entry_point(
            entry_point=entry_point, user_parameters=user_parameters
        )
    result = str(e.value)
    assert result == expected


def test_environment_variable_expansion_validation():
    broken_entry_point = _project_spec.EntryPoint(
        name="main",
        parameters={},
        command=(
            "python main.py "
            "--nproc-per-node=$(( ${{SLURM_STEP_GPUS: -1}} + 1 ))"
        ),
    )

    backend._validate_env_var_expansion_in_entry_point(
        entry_point=broken_entry_point
    )


@pytest.mark.parametrize(
    ("env_var_expansion", "env_var_expansion_list"),
    [
        ("$(( ${SLURM_STEP_GPUS: -1} + 1 ))", "['${SLURM_STEP_GPUS: -1}']"),
        (
            "$(( ${{{SLURM_STEP_GPUS: -1}}} + 1 ))",
            "['${{{SLURM_STEP_GPUS: -1}}}']",
        ),
        (
            "$(( ${{{SLURM_STEP_GPUS: -1}} + 1 ))",
            "['${{{SLURM_STEP_GPUS: -1}}']",
        ),
    ],
    ids=[
        "Single opening and closing curly braces",
        "Matching number of opening and closing curly braces, "
        "but incorrect number",
        "Not matching numbers of opening and closing curly braces",
    ],
)
def test_environment_variable_expansion_fails(
    env_var_expansion, env_var_expansion_list, expect_raise_if_exception
):
    broken_entry_point = _project_spec.EntryPoint(
        name="main",
        parameters={},
        command=f"python main.py --nproc-per-node={env_var_expansion}",
    )
    expected = (
        "Entry point command contains improperly formatted environment "
        f"variable expansions: {env_var_expansion_list}. Ensure "
        "expansions use exactly two opening and closing braces, "
        "e.g. ${{ENV_VAR}}."
    )
    with expect_raise_if_exception(
        exceptions.MLprojectFileValidationError()
    ) as e:
        backend._validate_env_var_expansion_in_entry_point(
            entry_point=broken_entry_point
        )
    result = str(e.value)
    assert result == expected
