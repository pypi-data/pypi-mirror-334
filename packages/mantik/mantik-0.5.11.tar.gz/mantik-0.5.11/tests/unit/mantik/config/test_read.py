import pathlib

import mantik.config
import mantik.config.environment as environment
import mantik.config.read as read


def test_read_config(compute_backend_config_yaml):
    backend_config = read.read_config(compute_backend_config_yaml)
    assert (
        backend_config["UnicoreApiUrl"]
        == "https://zam2125.zam.kfa-juelich.de:9112/JUWELS/rest/core"
    )
    assert backend_config["Resources"]["Queue"] == "devel"
    assert backend_config["Resources"]["Nodes"] == 2


def test_read_config_file_not_fund(
    expect_raise_if_exception, compute_backend_config_yaml
):
    with expect_raise_if_exception(
        mantik.config.exceptions.ConfigValidationError()
    ) as e:
        read.read_config(pathlib.Path("/does/not/exist.yaml"))

        assert "No such config: exist.yaml" in str(e)


def test_read_config_unsupported_type(expect_raise_if_exception):
    unsupported_format = ".yamml"
    with expect_raise_if_exception(
        mantik.config.exceptions.ConfigValidationError()
    ) as e:
        read.read_config(pathlib.Path(f"backend-config{unsupported_format}"))
    assert (
        "The given file type '.yamml' is not supported for the config, "
        "the supported ones are: '.json', '.yml', '.yaml'."
    ) == str(e.value)


def test_read_yaml_config(compute_backend_config_yaml):
    backend_config = read._read_yaml_config(compute_backend_config_yaml)
    assert (
        backend_config["UnicoreApiUrl"]
        == "https://zam2125.zam.kfa-juelich.de:9112/JUWELS/rest/core"
    )
    assert backend_config["Resources"]["Queue"] == "devel"
    assert backend_config["Resources"]["Nodes"] == 2


def test_read_json_config(compute_backend_config_json):
    backend_config = read._read_yaml_config(compute_backend_config_json)
    assert (
        backend_config["UnicoreApiUrl"]
        == "https://zam2125.zam.kfa-juelich.de:9112/JUWELS/rest/core"
    )
    assert backend_config["Resources"]["Queue"] == "devel"
    assert backend_config["Resources"]["Nodes"] == 2
    assert backend_config["Environment"]["Apptainer"] == {
        "Path": "mantik-test.sif",
        "Type": "lOcAl",
    }


def test_read_run_commands_from_config(compute_backend_config_yaml):
    backend_config = read._read_yaml_config(compute_backend_config_yaml)
    assert backend_config["Environment"]["PreRunCommandOnComputeNode"] == [
        "echo precommand",
        "echo on compute node",
        1,
    ]
    assert backend_config["Environment"]["PostRunCommandOnComputeNode"] == [
        "echo postcommand",
        "echo on compute node",
    ]
    assert backend_config["Environment"]["PreRunCommandOnLoginNode"] == [
        "echo precommand",
        "echo on login node",
    ]
    assert (
        backend_config["Environment"]["PostRunCommandOnLoginNode"]
        == "echo postcommand echo on login node"
    )

    env = environment.Environment.from_dict(
        config=backend_config["Environment"]
    )

    assert env.pre_run_command_on_compute_node == [
        "echo precommand",
        "echo on compute node",
        "1",
    ]
    assert env.post_run_command_on_compute_node == [
        "echo postcommand",
        "echo on compute node",
    ]
    assert env.pre_run_command_on_login_node == [
        "echo precommand",
        "echo on login node",
    ]
    assert env.post_run_command_on_compute_node == [
        "echo postcommand",
        "echo on compute node",
    ]
