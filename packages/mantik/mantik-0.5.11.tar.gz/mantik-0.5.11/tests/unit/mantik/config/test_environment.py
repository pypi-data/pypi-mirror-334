import os
import pathlib

import pytest

import mantik.config.environment as environment
import mantik.config.exceptions as exceptions
import mantik.config.executable as executable
import mantik.testing as testing


class TestEnvironment:
    @pytest.mark.parametrize(
        ("env_vars", "d", "expected"),
        [
            (
                testing.config.ALL_UNICORE_ENV_VARS,
                {
                    "Apptainer": {
                        "Path": "image.sif",
                    },
                },
                testing.config._create_apptainer_environment(
                    path=pathlib.Path("image.sif")
                ),
            ),
            (
                testing.config.ALL_UNICORE_ENV_VARS,
                {"Python": "/path/to/venv"},
                testing.config._create_python_environment(
                    path=pathlib.Path("/path/to/venv")
                ),
            ),
            (
                testing.config.ALL_UNICORE_ENV_VARS,
                {"Python": {"Path": "/path/to/venv"}},
                testing.config._create_python_environment(
                    path=pathlib.Path("/path/to/venv")
                ),
            ),
            (
                testing.config.ALL_UNICORE_ENV_VARS,
                {
                    "Python": {"Path": "/path/to/venv"},
                    "PreRunCommandOnLoginNode": "precommand login node",
                    "PostRunCommandOnLoginNode": "postcommand login node",
                    "PreRunCommandOnComputeNode": "precommand compute node",
                    "PostRunCommandOnComputeNode": "postcommand compute node",
                },
                testing.config._create_python_environment(
                    path=pathlib.Path("/path/to/venv"),
                    pre_run_command_on_login_node=["precommand login node"],
                    post_run_command_on_login_node=["postcommand login node"],
                    pre_run_command_on_compute_node=["precommand compute node"],
                    post_run_command_on_compute_node=[
                        "postcommand compute node"
                    ],
                ),
            ),
        ],
    )
    def test_from_dict(
        self, monkeypatch, expect_raise_if_exception, env_vars, d, expected
    ):
        if "MLFLOW_TRACKING_TOKEN" in os.environ:
            del os.environ["MLFLOW_TRACKING_TOKEN"]
        if "MLFLOW_EXPERIMENT_ID" in os.environ:
            del os.environ["MLFLOW_EXPERIMENT_ID"]
        for key in env_vars:
            os.environ[key] = testing.config.DEFAULT_ENV_VAR_VALUE

        with expect_raise_if_exception(expected):
            result = environment.Environment.from_dict(d)

            assert result == expected

    @pytest.mark.parametrize(
        (
            "env",
            "expected",
        ),
        [
            # Test case: No execution environment
            (
                environment.Environment(),
                None,
            ),
            # Test case: Apptainer
            (
                testing.config._create_apptainer_environment(
                    path=pathlib.Path("/path/to/venv")
                ),
                "srun apptainer run venv",
            ),
            # Test case: Python
            (
                testing.config._create_python_environment(
                    modules=None,
                    path=pathlib.Path("/path/to/venv"),
                ),
                "source /path/to/venv/bin/activate",
            ),
        ],
    )
    def test_create_execution_command(self, env, expected):
        result = env._create_execution_command()

        assert expected == result

    @pytest.mark.parametrize(
        (
            "env",
            "expected",
        ),
        [
            # Test case: Apptainer with no modules and no precommand
            (
                testing.config._create_apptainer_environment(
                    modules=None, path=pathlib.Path("/path/to/venv")
                ),
                None,
            ),
            # Test case: Apptainer with no modules and precommand
            (
                testing.config._create_apptainer_environment(
                    modules=None,
                    path=pathlib.Path("/path/to/venv"),
                    pre_run_command_on_compute_node=[
                        "a precommand",
                        "another precommand",
                    ],
                ),
                "a precommand\nanother precommand",
            ),
            # Test case: Apptainer with 1 module and no precommand
            (
                testing.config._create_apptainer_environment(
                    modules=["Module"], path=pathlib.Path("/path/to/venv")
                ),
                "module load Module",
            ),
            # Test case: Apptainer with 1 module and precommand
            (
                testing.config._create_apptainer_environment(
                    modules=["Module"],
                    path=pathlib.Path("/path/to/venv"),
                    pre_run_command_on_compute_node=[
                        "a precommand",
                        "another precommand",
                    ],
                ),
                "module load Module\na precommand\nanother precommand",
            ),
            # Test case: Apptainer with 2 modules and no precommand
            (
                testing.config._create_apptainer_environment(
                    modules=["Module"], path=pathlib.Path("/path/to/venv")
                ),
                "module load Module",
            ),
            # Test case: Apptainer with 2 modules and precommand as a list
            (
                testing.config._create_apptainer_environment(
                    modules=["Module1", "Module2"],
                    path=pathlib.Path("/path/to/venv"),
                    pre_run_command_on_compute_node=[
                        "a precommand",
                        "another precommand",
                    ],
                ),
                "module load Module1 Module2\na precommand\n"
                "another precommand",
            ),
            # Test case: Python with no modules and no precommand
            (
                testing.config._create_python_environment(
                    modules=None, path=pathlib.Path("/path/to/venv")
                ),
                None,
            ),
            # Test case: Python with no modules and precommand
            (
                testing.config._create_python_environment(
                    modules=None,
                    path=pathlib.Path("/path/to/venv"),
                    pre_run_command_on_compute_node=[
                        "a precommand",
                        "another precommand",
                    ],
                ),
                "a precommand\nanother precommand",
            ),
            # Test case: Python with 1 module and no precommand
            (
                testing.config._create_python_environment(
                    modules=["Module"],
                    path=pathlib.Path("/path/to/venv"),
                ),
                "module load Module",
            ),
            # Test case: Python with 1 module and precommand
            (
                testing.config._create_python_environment(
                    modules=["Module"],
                    path=pathlib.Path("/path/to/venv"),
                    pre_run_command_on_compute_node=[
                        "a precommand",
                        "another precommand",
                    ],
                ),
                "module load Module\na precommand\nanother precommand",
            ),
            # Test case: Python with 2 modules and no precommand
            (
                testing.config._create_python_environment(
                    modules=["Module1", "Module2"],
                    path=pathlib.Path("/path/to/venv"),
                ),
                "module load Module1 Module2",
            ),
            # Test case: Python with 2 modules and precommand
            (
                testing.config._create_python_environment(
                    modules=["Module1", "Module2"],
                    path=pathlib.Path("/path/to/venv"),
                    pre_run_command_on_compute_node=[
                        "a precommand",
                        "another precommand",
                    ],
                ),
                "module load Module1 Module2\na precommand\n"
                "another precommand",
            ),
            # Test case: No execution environment
            (
                environment.Environment(
                    modules=["Module1", "Module2"],
                    pre_run_command_on_compute_node=[
                        "a precommand",
                        "another precommand",
                    ],
                ),
                "module load Module1 Module2\na precommand\n"
                "another precommand",
            ),
        ],
    )
    def test_create_precommand_on_compute_node(self, env, expected):
        result = env._create_pre_run_command_on_compute_node()

        assert expected == result

    def test_create_postcommand_on_login_node(self):
        expected = "a postcommand && another postcommand"
        env = testing.config._create_python_environment(
            path=pathlib.Path("/path/to/venv"),
            post_run_command_on_login_node=[
                "a postcommand",
                "another postcommand",
            ],
        )

        result = env._create_login_node_command(
            env.post_run_command_on_login_node
        )

        assert expected == result

    @pytest.mark.parametrize(
        (
            "env",
            "expected",
        ),
        [
            # Test case: No execution environment
            (
                environment.Environment(
                    modules=["Module1", "Module2"],
                    pre_run_command_on_compute_node=["a precommand"],
                    post_run_command_on_compute_node=["a postcommand"],
                ),
                (
                    "module load Module1 Module2\n"
                    "a precommand && "
                    "python main.py test && "
                    "a postcommand"
                ),
            ),
            # Test case: Apptainer with no precommand, no postcommand, no modules # noqa E501
            (
                testing.config._create_apptainer_environment(
                    path=pathlib.Path("/path/to/venv")
                ),
                "srun apptainer run venv python main.py test",
            ),
            # Test case: Apptainer with a precommand, a postcommand and modules
            (
                testing.config._create_apptainer_environment(
                    path=pathlib.Path("/path/to/venv"),
                    modules=["Module1", "Module2"],
                    pre_run_command_on_compute_node=["a precommand"],
                    post_run_command_on_compute_node=["a postcommand"],
                ),
                (
                    "module load Module1 Module2\n"
                    "a precommand && "
                    "srun apptainer run venv "
                    "python main.py test && "
                    "a postcommand"
                ),
            ),
            # Test case: Python with no precommand, no postcommand, no modules
            (
                testing.config._create_python_environment(
                    path=pathlib.Path("/path/to/venv")
                ),
                "source /path/to/venv/bin/activate && python main.py test",
            ),
            # Test case: Python with a precommand, a postcommand and modules
            (
                testing.config._create_python_environment(
                    path=pathlib.Path("/path/to/venv"),
                    modules=["Module1", "Module2"],
                    pre_run_command_on_compute_node=["a precommand"],
                    post_run_command_on_compute_node=["a postcommand"],
                ),
                (
                    "module load Module1 Module2\n"
                    "a precommand && "
                    "source /path/to/venv/bin/activate && "
                    "python main.py test && "
                    "a postcommand"
                ),
            ),
        ],
    )
    def test_create_execution_command_with_arguments(self, env, expected):
        entry_point_arguments = "python main.py test"
        result = env._create_execution_command_with_arguments(
            entry_point_arguments
        )
        assert result == expected

    @pytest.mark.parametrize(
        "env",
        [
            # Test case: Apptainer with no variables
            testing.config._create_apptainer_environment(
                modules=None,
                path=pathlib.Path("/path/to/venv"),
                include_mlflow_env_vars=False,
            ),
            # Test case: Python with no variables
            testing.config._create_python_environment(
                modules=None,
                path=pathlib.Path("/path/to/venv"),
                include_mlflow_env_vars=False,
            ),
        ],
    )
    def test_add_env_variables(self, env):
        assert env.variables is None
        expected = {"env_var": "ENV_VAR"}
        env.add_env_vars(expected)
        result = env.variables
        assert expected == result

    @pytest.mark.parametrize(
        ("config", "expected", "error_message"),
        [
            # Test case: No execution environment given
            (
                {"Resources": {}},
                None,
                None,
            ),
            # Test case: One execution environment given
            (
                {"Apptainer": {"Path": "image.sif"}},
                executable.Apptainer(path=pathlib.Path("image.sif")),
                None,
            ),
            # Test case: Two execution environments given, should raise
            (
                {"Apptainer": {}, "Python": {}},
                exceptions.ConfigValidationError(),
                "Only one execution environment is allowed, "
                "but in config these have been "
                "found: 'Apptainer', 'Python'.",
            ),
        ],
    )
    def test_get_execution_environment(
        self, expect_raise_if_exception, config, expected, error_message
    ):
        with expect_raise_if_exception(expected) as e:
            result = environment._get_execution_environment(config)
            assert result == expected

        if error_message is not None:
            assert str(e.value) == error_message

    @pytest.mark.parametrize(
        (
            "env",
            "expected",
        ),
        [
            # Test case: Apptainer with no modules and no env vars
            (
                testing.config._create_apptainer_environment(
                    modules=None,
                    path=pathlib.Path("/path/to/venv"),
                    include_mlflow_env_vars=False,
                ),
                (
                    "export MANTIK_WORKING_DIRECTORY=/test-scratch-dir/test-user-name/mantik/test-run-dir\n"  # noqa E501
                    "srun apptainer run venv python main.py test"
                ),
            ),
            # Test case: Apptainer with 1 module and env vars
            (
                testing.config._create_apptainer_environment(
                    modules=["Module"],
                    path=pathlib.Path("/path/to/venv"),
                    variables={"TEST_ENV_VAR": "test-value"},
                    include_mlflow_env_vars=False,
                ),
                (
                    "export MANTIK_WORKING_DIRECTORY=/test-scratch-dir/test-user-name/mantik/test-run-dir\n"  # noqa E501
                    "export TEST_ENV_VAR=test-value\n"
                    "module load Module && "
                    "srun apptainer run venv python main.py test"
                ),
            ),
            # Test case: Python with no modules and no env vars
            (
                testing.config._create_python_environment(
                    modules=None,
                    path=pathlib.Path("/path/to/venv"),
                    include_mlflow_env_vars=False,
                ),
                (
                    "export MANTIK_WORKING_DIRECTORY=/test-scratch-dir/test-user-name/mantik/test-run-dir\n"  # noqa E501
                    "source /path/to/venv/bin/activate && python main.py test"
                ),
            ),
            # Test case: Python with 1 module and env vars
            (
                testing.config._create_python_environment(
                    modules=["Module"],
                    path=pathlib.Path("/path/to/venv"),
                    variables={"TEST_ENV_VAR": "test-value"},
                    include_mlflow_env_vars=False,
                ),
                (
                    "export MANTIK_WORKING_DIRECTORY=/test-scratch-dir/test-user-name/mantik/test-run-dir\n"  # noqa E501
                    "export TEST_ENV_VAR=test-value\n"
                    "module load Module && "
                    "source /path/to/venv/bin/activate && "
                    "python main.py test"
                ),
            ),
            # Test case: No execution environment
            (
                environment.Environment(
                    modules=["Module1", "Module2"],
                    variables={"TEST_ENV_VAR": "test-value"},
                ),
                (
                    "export MANTIK_WORKING_DIRECTORY=/test-scratch-dir/test-user-name/mantik/test-run-dir\n"  # noqa E501
                    "export TEST_ENV_VAR=test-value\n"
                    "module load Module1 Module2 && "
                    "python main.py test"
                ),
            ),
        ],
    )
    def test_to_slurm_batch_script(self, env, expected):
        entry_point_arguments = "python main.py test"
        result = env.to_slurm_batch_script(
            entry_point_arguments=entry_point_arguments,
            run_dir=pathlib.Path(
                "/test-scratch-dir/test-user-name/mantik/test-run-dir"
            ),
        )

        assert result == expected
