import pathlib

import pytest

import mantik.config
import mantik.config.exceptions as exceptions
import mantik.testing as testing


class TestConfig:
    @pytest.mark.parametrize(
        ("env_vars", "d", "expected", "expected_messgage"),
        [
            # Test case: Neither UnicoreApiUrl nor Firecrest section given
            (
                testing.config.ALL_UNICORE_ENV_VARS,
                {},
                exceptions.ConfigValidationError(),
                "Either UnicoreApiUrl or Firecrest details must be provided",
            ),
            # Test cases: UNICORE environment variables not set.
            (
                [],
                {
                    "UnicoreApiUrl": "test-url",
                    "Resources": {"Queue": "batch"},
                },
                NameError(),
                "Environment variable 'MANTIK_UNICORE_USERNAME' not set",
            ),
            (
                testing.config.ALL_UNICORE_ENV_VARS[:1],
                {
                    "UnicoreApiUrl": "test-url",
                    "Resources": {"Queue": "batch"},
                },
                NameError(),
                "Environment variable 'MANTIK_UNICORE_PASSWORD' not set",
            ),
            # Test cases: firecREST environment variables not set.
            (
                [],
                {
                    "Firecrest": {
                        "ApiUrl": "test-api-url",
                        "TokenUrl": "test-token-url",
                        "Machine": "test-machine",
                    },
                    "Resources": {"Queue": "batch"},
                },
                NameError(),
                "Environment variable 'MANTIK_FIRECREST_CLIENT_ID' not set",
            ),
            (
                testing.config.ALL_FIRECREST_ENV_VARS[:1],
                {
                    "Firecrest": {
                        "ApiUrl": "test-api-url",
                        "TokenUrl": "test-token-url",
                        "Machine": "test-machine",
                    },
                    "Resources": {"Queue": "batch"},
                },
                NameError(),
                "Environment variable 'MANTIK_FIRECREST_CLIENT_SECRET' not set",
            ),
            # Test cases: No compute budget account env var set
            (
                testing.config.ALL_UNICORE_ENV_VARS[:2],
                {
                    "UnicoreApiUrl": "test-url",
                    "Resources": {"Queue": "batch"},
                },
                NameError(),
                "Environment variable 'MANTIK_COMPUTE_BUDGET_ACCOUNT' not set",
            ),
            (
                testing.config.ALL_FIRECREST_ENV_VARS[:2],
                {
                    "Firecrest": {
                        "ApiUrl": "test-api-url",
                        "TokenUrl": "test-token-url",
                        "Machine": "test-machine",
                    },
                    "Resources": {"Queue": "batch"},
                },
                NameError(),
                "Environment variable 'MANTIK_COMPUTE_BUDGET_ACCOUNT' not set",
            ),
            # Test case: backend config missing Resources section.
            (
                testing.config.ALL_UNICORE_ENV_VARS,
                {"Queue": "batch"},
                exceptions.ConfigValidationError(),
                "Either UnicoreApiUrl or Firecrest details must be provided",
            ),
            # Test case: Neither unicore nor firecrest given.
            (
                testing.config.ALL_UNICORE_ENV_VARS,
                {
                    "Environment": {
                        "Apptainer": {
                            "Path": "image.sif",
                        },
                    },
                    "Resources": {"Queue": "batch"},
                },
                exceptions.ConfigValidationError(),
                "Either UnicoreApiUrl or Firecrest details must be provided",
            ),
            # Test case: Both unicore and firecrest given
            (
                testing.config.ALL_FIRECREST_ENV_VARS,
                {
                    "UnicoreApiUrl": "test-url",
                    "Firecrest": {
                        "ApiUrl": "test-api-url",
                        "TokenUrl": "test-token-url",
                        "Machine": "test-machine",
                    },
                    "Environment": {
                        "Apptainer": {
                            "Path": "image.sif",
                        },
                    },
                    "Resources": {"Queue": "batch"},
                },
                exceptions.ConfigValidationError(),
                (
                    "Either UnicoreApiUrl or Firecrest details must be "
                    "provided, but both are given"
                ),
            ),
            # Test case: Remote Apptainer image given but relative path.
            (
                testing.config.ALL_UNICORE_ENV_VARS,
                {
                    "UnicoreApiUrl": "test-url",
                    "Resources": {"Queue": "batch"},
                    "Environment": {
                        "Apptainer": {
                            "Path": "../relative/path/to/image.sif",
                            "Type": "remote",
                        },
                    },
                },
                mantik.config.exceptions.ConfigValidationError(),
                (
                    "If image type 'remote' is given for an Apptainer image, "
                    "the given path must be absolute. The given path is: "
                    "'../relative/path/to/image.sif'."
                ),
            ),
            # Test case: Config entry has incorrect type.
            (
                testing.config.ALL_UNICORE_ENV_VARS,
                {
                    "UnicoreApiUrl": "test-url",
                    "Resources": {"Queue": "batch", "Nodes": "incorrect type"},
                },
                mantik.config.exceptions.ConfigValidationError(),
                "Config value for 'Nodes' has to be of type int",
            ),
        ],
    )
    @pytest.mark.usefixtures("unset_tracking_token_env_var_before_execution")
    def test_from_dict_raises(
        self,
        expect_raise_if_exception,
        env_vars_set,
        env_vars,
        d,
        expected,
        expected_messgage,
    ):
        env_vars = {
            var: testing.config.DEFAULT_ENV_VAR_VALUE for var in env_vars
        }

        with env_vars_set(env_vars), expect_raise_if_exception(expected) as e:
            mantik.config.core.Config.from_dict(d)

        result = str(e.value)

        assert result == expected_messgage, "Incorrect error message raised"

    @pytest.mark.parametrize(
        ("env_vars", "d", "expected"),
        [
            # Test case: Everything correct.
            (
                testing.config.ALL_UNICORE_ENV_VARS,
                {
                    "UnicoreApiUrl": "test-url",
                    "Environment": {
                        "Apptainer": {
                            "Path": "image.sif",
                        },
                    },
                    "Resources": {"Queue": "batch"},
                },
                testing.config._create_config_with_unicore(
                    resources=mantik.config.resources.Resources(queue="batch"),
                    env=mantik.config.environment.Environment(
                        execution=mantik.config.executable.Apptainer(
                            path=pathlib.Path("image.sif"),
                        ),
                    ),
                ),
            ),
            # Test case: Using firecrest
            (
                testing.config.ALL_FIRECREST_ENV_VARS,
                {
                    "Firecrest": {
                        "ApiUrl": "test-api-url",
                        "TokenUrl": "test-token-url",
                        "Machine": "test-machine",
                    },
                    "Environment": {
                        "Apptainer": {
                            "Path": "image.sif",
                        },
                    },
                    "Resources": {"Queue": "batch", "NodeConstraints": "gpu"},
                },
                testing.config._create_config_with_firecrest(
                    resources=mantik.config.resources.Resources(
                        queue="batch", node_constraints="gpu"
                    ),
                    env=mantik.config.environment.Environment(
                        execution=mantik.config.executable.Apptainer(
                            path=pathlib.Path("image.sif"),
                        ),
                    ),
                ),
            ),
            # Test case: Using firecrest
            (
                testing.config.ALL_FIRECREST_ENV_VARS,
                {
                    "Firecrest": {
                        "ApiUrl": "test-api-url",
                        "TokenUrl": "test-token-url",
                        "Machine": "test-machine",
                    },
                    "Environment": {
                        "Apptainer": {
                            "Path": "image.sif",
                        },
                    },
                    "Resources": {"Queue": "batch", "NodeConstraints": "gpu"},
                },
                testing.config._create_config_with_firecrest(
                    resources=mantik.config.resources.Resources(
                        queue="batch", node_constraints="gpu"
                    ),
                    env=mantik.config.environment.Environment(
                        execution=mantik.config.executable.Apptainer(
                            path=pathlib.Path("image.sif"),
                        ),
                    ),
                ),
            ),
            # Test case: No environment given
            (
                testing.config.ALL_UNICORE_ENV_VARS,
                {
                    "UnicoreApiUrl": "test-url",
                    "Resources": {"Queue": "batch"},
                },
                testing.config._create_config_with_unicore(
                    resources=mantik.config.resources.Resources(queue="batch"),
                ),
            ),
            # Test case: No environment given, but resources
            (
                testing.config.ALL_UNICORE_ENV_VARS,
                {
                    "UnicoreApiUrl": "test-url",
                    "Resources": {
                        "Queue": "batch",
                        "Runtime": "2h",
                        "Nodes": 1,
                        "TotalCPUs": 2,
                        "CPUsPerNode": 3,
                        "GPUsPerNode": 4,
                        "MemoryPerNode": "10G",
                        "Reservation": "test-reservation",
                        "NodeConstraints": "mem192",
                        "QoS": "test-qos",
                    },
                },
                testing.config._create_config_with_unicore(
                    resources=mantik.config.resources.Resources(
                        queue="batch",
                        runtime="2h",
                        nodes=1,
                        total_cpus=2,
                        cpus_per_node=3,
                        gpus_per_node=4,
                        memory_per_node="10G",
                        reservation="test-reservation",
                        node_constraints="mem192",
                        qos="test-qos",
                    ),
                ),
            ),
            # Test case: Only modules given in environment
            (
                testing.config.ALL_UNICORE_ENV_VARS,
                {
                    "UnicoreApiUrl": "test-url",
                    "Environment": {
                        "Modules": ["module"],
                    },
                    "Resources": {"Queue": "batch"},
                },
                testing.config._create_config_with_unicore(
                    resources=mantik.config.resources.Resources(queue="batch"),
                    env=mantik.config.environment.Environment(
                        modules=["module"],
                    ),
                ),
            ),
            # Test case: Local Apptainer image given.
            (
                testing.config.ALL_UNICORE_ENV_VARS,
                {
                    "UnicoreApiUrl": "test-url",
                    "Resources": {"Queue": "batch"},
                    "Environment": {
                        "Apptainer": {
                            "Path": "image.sif",
                        },
                    },
                },
                testing.config._create_config_with_unicore(
                    resources=mantik.config.resources.Resources(queue="batch"),
                    env=mantik.config.environment.Environment(
                        execution=mantik.config.executable.Apptainer(
                            path=pathlib.Path("image.sif"),
                        ),
                    ),
                ),
            ),
            # Test case: Local Apptainer image given with additional options
            # as list of strings
            (
                testing.config.ALL_UNICORE_ENV_VARS,
                {
                    "UnicoreApiUrl": "test-url",
                    "Resources": {"Queue": "batch"},
                    "Environment": {
                        "Apptainer": {
                            "Path": "image.sif",
                            "Options": ["--nv", "-B /data:/data"],
                        },
                    },
                },
                testing.config._create_config_with_unicore(
                    resources=mantik.config.resources.Resources(queue="batch"),
                    env=mantik.config.environment.Environment(
                        execution=mantik.config.executable.Apptainer(
                            path=pathlib.Path("image.sif"),
                            options=["--nv", "-B /data:/data"],
                        )
                    ),
                ),
            ),
            # Test case: Local Apptainer image given with additional options
            # as string
            (
                testing.config.ALL_UNICORE_ENV_VARS,
                {
                    "UnicoreApiUrl": "test-url",
                    "Resources": {"Queue": "batch"},
                    "Environment": {
                        "Apptainer": {
                            "Path": "image.sif",
                            "Options": "--nv -B /data:/data",
                        },
                    },
                },
                testing.config._create_config_with_unicore(
                    resources=mantik.config.resources.Resources(queue="batch"),
                    env=mantik.config.environment.Environment(
                        execution=mantik.config.executable.Apptainer(
                            path=pathlib.Path("image.sif"),
                            options=["--nv -B /data:/data"],
                        )
                    ),
                ),
            ),
            # Test case: Remote Apptainer image given.
            (
                testing.config.ALL_UNICORE_ENV_VARS,
                {
                    "UnicoreApiUrl": "test-url",
                    "Resources": {"Queue": "batch"},
                    "Environment": {
                        "Apptainer": {
                            "Path": "/absolute/path/to/image.sif",
                            "Type": "remote",
                        },
                    },
                },
                testing.config._create_config_with_unicore(
                    resources=mantik.config.resources.Resources(queue="batch"),
                    env=mantik.config.environment.Environment(
                        execution=mantik.config.executable.Apptainer(
                            path=pathlib.Path("/absolute/path/to/image.sif"),
                            type="remote",
                        ),
                    ),
                ),
            ),
            # Test case: More variables and modules given.
            (
                testing.config.ALL_UNICORE_ENV_VARS,
                {
                    "UnicoreApiUrl": "test-url",
                    "Resources": {"Queue": "batch"},
                    "Environment": {
                        "Apptainer": {
                            "Path": "/absolute/path/to/image.sif",
                            "Type": "remote",
                        },
                        "Variables": {"TEST_ENV_VAR": "value"},
                        "Modules": [
                            "TensorFlow/2.5.0-Python-3.8.5",
                            "Horovod/0.23.0-Python-3.8.5",
                            "PyTorch/1.8.1-Python-3.8.5",
                        ],
                    },
                },
                testing.config._create_config_with_unicore(
                    resources=mantik.config.resources.Resources(queue="batch"),
                    env=mantik.config.environment.Environment(
                        execution=mantik.config.executable.Apptainer(
                            path=pathlib.Path("/absolute/path/to/image.sif"),
                            type="remote",
                        ),
                        modules=[
                            "TensorFlow/2.5.0-Python-3.8.5",
                            "Horovod/0.23.0-Python-3.8.5",
                            "PyTorch/1.8.1-Python-3.8.5",
                        ],
                        variables={"TEST_ENV_VAR": "value"},
                    ),
                ),
            ),
        ],
    )
    @pytest.mark.usefixtures("unset_tracking_token_env_var_before_execution")
    def test_from_dict(
        self, expect_raise_if_exception, env_vars_set, env_vars, d, expected
    ):
        env_vars = {
            var: testing.config.DEFAULT_ENV_VAR_VALUE for var in env_vars
        }

        with env_vars_set(env_vars):
            result = mantik.config.core.Config.from_dict(d)

            assert result == expected

    @pytest.mark.parametrize(
        "d",
        [
            {
                "Firecrest": {
                    "ApiUrl": "test-api-url",
                    "TokenUrl": "test-token-url",
                    "Machine": "test-machine",
                },
                "Environment": {
                    "PreRunCommandOnLoginNode": "echo hello",
                },
                "Resources": {"Queue": "batch", "NodeConstraints": "gpu"},
            },
            {
                "Firecrest": {
                    "ApiUrl": "test-api-url",
                    "TokenUrl": "test-token-url",
                    "Machine": "test-machine",
                },
                "Environment": {
                    "PostRunCommandOnLoginNode": "echo hello",
                },
                "Resources": {"Queue": "batch", "NodeConstraints": "gpu"},
            },
            {
                "Firecrest": {
                    "ApiUrl": "test-api-url",
                    "TokenUrl": "test-token-url",
                    "Machine": "test-machine",
                },
                "Environment": {
                    "PreRunCommandOnLoginNode": "echo hello",
                    "PostRunCommandOnLoginNode": "echo hello",
                },
                "Resources": {"Queue": "batch", "NodeConstraints": "gpu"},
            },
        ],
    )
    def test_command_on_login_node_raises_for_firecrest(
        self, env_vars_set, expect_raise_if_exception, d
    ):
        env_vars = {
            var: testing.config.DEFAULT_ENV_VAR_VALUE
            for var in testing.config.ALL_FIRECREST_ENV_VARS
        }
        expected = "Pre-/PostRunCommandOnLoginNode not supported by firecREST"

        with env_vars_set(env_vars), expect_raise_if_exception(
            exceptions.ConfigValidationError()
        ) as e:
            mantik.config.core.Config.from_dict(d)

        assert str(e.value) == expected

    @pytest.mark.parametrize(
        ("config", "expected"),
        [
            # Test case: Only project, resources and
            # environment are included in the returned dict.
            (
                mantik.config.core.Config(
                    unicore_api_url="not_included",
                    user="not_included",
                    password="not_included",
                    project="test-project",
                    resources=mantik.config.resources.Resources(
                        queue="batch",
                    ),
                    environment=mantik.config.environment.Environment(
                        execution=mantik.config.executable.Apptainer(
                            path=pathlib.Path("test-image")
                        ),
                    ),
                ),
                {
                    "Project": "test-project",
                    "Resources": {"Queue": "batch"},
                    "Arguments": [],
                    "RunUserPrecommandOnLoginNode": True,
                    "RunUserPostcommandOnLoginNode": True,
                    "Stdout": "mantik.log",
                    "Stderr": "mantik.log",
                },
            ),
            # Test case: All given values included.
            (
                mantik.config.core.Config(
                    unicore_api_url="not_included",
                    user="not_included",
                    password="not_included",
                    project="test-project",
                    resources=mantik.config.resources.Resources(
                        queue="batch",
                        runtime="1h",
                        nodes=2,
                        total_cpus=48,
                        cpus_per_node=24,
                        memory_per_node="10G",
                        gpus_per_node=1,
                        reservation="test-reservation",
                        node_constraints="test-node-constraints",
                        qos="test-qos",
                    ),
                    environment=mantik.config.environment.Environment(
                        execution=mantik.config.executable.Apptainer(
                            path=pathlib.Path("test-image"),
                        ),
                        variables={"TEST": "test"},
                    ),
                ),
                {
                    "Project": "test-project",
                    "Resources": {
                        "Queue": "batch",
                        "Runtime": "1h",
                        "Nodes": 2,
                        "TotalCPUs": 48,
                        "CPUsPerNode": 24,
                        "GPUS": 1,
                        "MemoryPerNode": "10G",
                        "Reservation": "test-reservation",
                        "NodeConstraints": "test-node-constraints",
                        "QoS": "test-qos",
                    },
                    "Environment": {"TEST": "test", "SRUN_CPUS_PER_TASK": "24"},
                    "Arguments": [],
                    "RunUserPrecommandOnLoginNode": True,
                    "RunUserPostcommandOnLoginNode": True,
                    "Stdout": "mantik.log",
                    "Stderr": "mantik.log",
                },
            ),
        ],
    )
    def test_to_dict(self, config, expected):
        result = config.to_dict()

        assert result == expected

    @pytest.mark.parametrize(
        ("config", "expected"),
        [
            # Test case: No environment section, and cpus_per_node unset
            (
                mantik.config.core.Config(
                    unicore_api_url="not_included",
                    user="not_included",
                    password="not_included",
                    project="test-project",
                    resources=mantik.config.resources.Resources(
                        queue="batch",
                    ),
                ),
                None,
            ),
            # Test case: Environment section, but no Variables, and
            # cpus_per_node unset
            (
                mantik.config.core.Config(
                    unicore_api_url="not_included",
                    user="not_included",
                    password="not_included",
                    project="test-project",
                    resources=mantik.config.resources.Resources(
                        queue="batch",
                    ),
                    environment=mantik.config.environment.Environment(),  # noqa E501
                ),
                None,
            ),
            # Test case: Environment section with Variables, and
            # cpus_per_node unset
            (
                mantik.config.core.Config(
                    unicore_api_url="not_included",
                    user="not_included",
                    password="not_included",
                    project="test-project",
                    resources=mantik.config.resources.Resources(
                        queue="batch",
                    ),
                    environment=mantik.config.environment.Environment(
                        variables={"TEST_VAR": "test_value"}
                    ),
                ),
                {"TEST_VAR": "test_value"},
            ),
            # Test case: SRUN_CPUS_PER_TASK set explicitly by user,
            # and cpus_per_node unset
            (
                mantik.config.core.Config(
                    unicore_api_url="not_included",
                    user="not_included",
                    password="not_included",
                    project="test-project",
                    resources=mantik.config.resources.Resources(
                        queue="batch",
                    ),
                    environment=mantik.config.environment.Environment(
                        variables={"SRUN_CPUS_PER_TASK": "2"},
                    ),
                ),
                {"SRUN_CPUS_PER_TASK": "2"},
            ),
            # Test case: No environment section, and cpus_per_node set
            (
                mantik.config.core.Config(
                    unicore_api_url="not_included",
                    user="not_included",
                    password="not_included",
                    project="test-project",
                    resources=mantik.config.resources.Resources(
                        queue="batch",
                        cpus_per_node=2,
                    ),
                ),
                {"SRUN_CPUS_PER_TASK": "2"},
            ),
            # Test case: Environment section, but no Variables, and
            # cpus_per_node set
            (
                mantik.config.core.Config(
                    unicore_api_url="not_included",
                    user="not_included",
                    password="not_included",
                    project="test-project",
                    resources=mantik.config.resources.Resources(
                        queue="batch",
                        cpus_per_node=2,
                    ),
                    environment=mantik.config.environment.Environment(),  # noqa E501
                ),
                {"SRUN_CPUS_PER_TASK": "2"},
            ),
            # Test case: Environment section with Variables, and
            # cpus_per_node set
            (
                mantik.config.core.Config(
                    unicore_api_url="not_included",
                    user="not_included",
                    password="not_included",
                    project="test-project",
                    resources=mantik.config.resources.Resources(
                        queue="batch",
                        cpus_per_node=2,
                    ),
                    environment=mantik.config.environment.Environment(
                        variables={"TEST_VAR": "test_value"},
                    ),
                ),
                {"TEST_VAR": "test_value", "SRUN_CPUS_PER_TASK": "2"},
            ),
            # Test case: SRUN_CPUS_PER_TASK set explicitly by user, and
            # cpus_per_node set
            (
                mantik.config.core.Config(
                    unicore_api_url="not_included",
                    user="not_included",
                    password="not_included",
                    project="test-project",
                    resources=mantik.config.resources.Resources(
                        queue="batch",
                        cpus_per_node=1,
                    ),
                    environment=mantik.config.environment.Environment(
                        variables={
                            "TEST_VAR": "test_value",
                            "SRUN_CPUS_PER_TASK": "2",
                        }
                    ),
                ),
                {"TEST_VAR": "test_value", "SRUN_CPUS_PER_TASK": "2"},
            ),
        ],
    )
    def test_with_optional_add_srun_cpus_per_task_to_environment(
        self, config, expected
    ) -> None:
        result = config.environment.variables

        assert result == expected

    @pytest.mark.parametrize(
        ("test_config", "expected"),
        [
            (
                mantik.config.core.Config(
                    unicore_api_url="not_included",
                    user="not_included",
                    password="not_included",
                    project="test-project",
                    resources=mantik.config.resources.Resources(
                        queue="batch",
                        cpus_per_node=1,
                    ),
                    environment=mantik.config.environment.Environment(
                        execution=mantik.config.executable.Apptainer(
                            path=pathlib.Path("test-image"),
                        ),
                        variables={"TEST": "test"},
                        pre_run_command_on_compute_node="echo precommand on compute node",  # noqa E501
                        post_run_command_on_compute_node="echo postcommand on compute node",  # noqa E501
                    ),
                ),
                {
                    "Project": "test-project",
                    "Resources": {"Queue": "batch", "CPUsPerNode": 1},
                    "Stdout": "mantik.log",
                    "Stderr": "mantik.log",
                    "Environment": {
                        "TEST": "test",
                        "SRUN_CPUS_PER_TASK": "1",
                        "MANTIK_WORKING_DIRECTORY": "$UC_WORKING_DIRECTORY",
                    },
                    "RunUserPrecommandOnLoginNode": True,
                    "Executable": 'source $(dirname "$(realpath "$0")")/mantik.sh',  # noqa E501
                    "Arguments": [],
                    "RunUserPostcommandOnLoginNode": True,
                },
            ),
            (
                mantik.config.core.Config(
                    unicore_api_url="not_included",
                    user="not_included",
                    password="not_included",
                    project="test-project",
                    resources=mantik.config.resources.Resources(
                        queue="batch",
                        cpus_per_node=1,
                    ),
                    environment=mantik.config.environment.Environment(
                        execution=mantik.config.executable.Python(
                            path=pathlib.Path("/venv"),
                        ),
                        variables={"TEST": "test"},
                        pre_run_command_on_compute_node="echo precommand on compute node",  # noqa E501
                        post_run_command_on_compute_node="echo postcommand on compute node",  # noqa E501
                    ),
                ),
                {
                    "Project": "test-project",
                    "Resources": {"Queue": "batch", "CPUsPerNode": 1},
                    "Stdout": "mantik.log",
                    "Stderr": "mantik.log",
                    "Environment": {
                        "TEST": "test",
                        "SRUN_CPUS_PER_TASK": "1",
                        "MANTIK_WORKING_DIRECTORY": "$UC_WORKING_DIRECTORY",
                    },
                    "RunUserPrecommandOnLoginNode": True,
                    "Arguments": [],
                    "Executable": 'source $(dirname "$(realpath "$0")")/mantik.sh',  # noqa E501
                    "RunUserPostcommandOnLoginNode": True,
                },
            ),
        ],
    )
    def test_to_job_description(self, test_config, expected):
        bash_script_name = "mantik.sh"
        result = test_config.to_unicore_job_description(bash_script_name)
        assert result == expected
