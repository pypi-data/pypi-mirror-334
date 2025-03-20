import functools
import json
import pathlib
import uuid

import firecrest as firecrest
import mlflow.projects as projects

import mantik.config.core as core
import mantik.testing as testing
import mantik.utils as mantik_utils
import mantik.utils.credentials as _credentials
import mantik_compute_backend.backend as backend

FILE_PATH = pathlib.Path(__file__).parent

ALL_ENV_VARS = [
    _credentials.FIRECREST_CLIENT_ID_ENV_VAR,
    _credentials.FIRECREST_CLIENT_SECRET_ENV_VAR,
    core.COMPUTE_BUDGET_ACCOUNT_ENV_VAR,
]


class FakeProject:
    pass


class TestFirecrestBackend:
    def test_run(
        self, monkeypatch, example_project_path, tmp_path, env_vars_set, caplog
    ):
        monkeypatch.setattr(
            firecrest,
            "Firecrest",
            testing.firecrest.FakeClient,
        )
        monkeypatch.setattr(
            firecrest,
            "ClientCredentialsAuth",
            functools.partial(
                testing.firecrest.FakeClientCredentialsAuth,
                login_successful=True,
            ),
        )

        backend_config_path = (
            example_project_path / "compute-backend-firecrest-config.json"
        )
        with open(backend_config_path) as infile:
            backend_config = json.load(infile)
        # Following env vars are set by MLflow before running a project.
        backend_config[
            projects.PROJECT_STORAGE_DIR
        ] = example_project_path.as_posix()

        # Point MLFLOW_TRACKING_URI to a temporary directory
        tracking_uri = tmp_path / "mlruns"

        with env_vars_set(
            {
                # Following env vars must be set for the config.
                **{key: "test-val" for key in ALL_ENV_VARS},
                mantik_utils.mlflow.TRACKING_URI_ENV_VAR: tracking_uri.as_uri(),
                mantik_utils.mlflow.ACTIVE_RUN_ID_ENV_VAR: str(
                    uuid.uuid4().hex
                ),
            }
        ):
            backend.Backend().run(
                project_uri=example_project_path.as_posix(),
                entry_point="main",
                params={"print": "test"},
                version=None,
                backend_config=backend_config,
                tracking_uri=None,
                experiment_id=None,
            )
            assert "Submitted job test-job-id via firecrest" in caplog.text


def test_create_job_script_apptainer(
    example_project_path, example_project, example_firecrest_config
):
    entry_point = example_project.get_entry_point("main")
    parameters = {"print": "whatever"}
    storage_dir = "test-dir"
    run_id = str(uuid.uuid4())
    run_dir = pathlib.Path("test-dir")
    expected = "\n".join(
        [
            "#!/bin/bash -l",
            f"#SBATCH --job-name='mantik-{run_id}'",
            "#SBATCH --partition=batch",
            "#SBATCH --constraint=gpu",
            f"#SBATCH --output={run_dir}/mantik.log",
            f"#SBATCH --error={run_dir}/mantik.log",
            'echo "firecREST working directory is $(pwd)"',
            'echo "Submitted batch script:"',
            "cat $(pwd)/script.batch",
            'echo "Changing to Mantik run directory test-dir"',
            f"cd {run_dir}",
            "export MANTIK_WORKING_DIRECTORY=test-dir",
            "srun apptainer run mantik-test.sif python main.py whatever",
        ]
    )

    arguments = backend._create_arguments(
        entry_point=entry_point, parameters=parameters, storage_dir=storage_dir
    )
    result = example_firecrest_config.to_slurm_batch_script(
        arguments=arguments,
        run_id=run_id,
        run_dir=run_dir,
    )

    assert result == expected


def test_create_job_script_apptainer_long_resources(
    example_project_path,
    example_project,
    example_firecrest_config_long_resources,
):
    entry_point = example_project.get_entry_point("main")
    parameters = {"print": "whatever"}
    storage_dir = "test-dir"
    run_id = str(uuid.uuid4())
    run_dir = pathlib.Path("test-dir")
    expected = "\n".join(
        [
            "#!/bin/bash -l",
            f"#SBATCH --job-name='mantik-{run_id}'",
            "#SBATCH --partition=batch",
            "#SBATCH --time=0-01:00:00",
            "#SBATCH --nodes=1",
            "#SBATCH --ntasks=1",
            "#SBATCH --ntasks-per-node=1",
            "#SBATCH --gpus-per-node=1",
            "#SBATCH --mem=1",
            "#SBATCH --reservation=test-reservation",
            "#SBATCH --constraint=gpu",
            "#SBATCH --qos=test-qos,",
            "#SBATCH --output=test-dir/mantik.log",
            "#SBATCH --error=test-dir/mantik.log",
            'echo "firecREST working directory is $(pwd)"',
            'echo "Submitted batch script:"',
            "cat $(pwd)/script.batch",
            'echo "Changing to Mantik run directory test-dir"',
            f"cd {run_dir}",
            "export MANTIK_WORKING_DIRECTORY=test-dir",
            "export SRUN_CPUS_PER_TASK=1",
            "srun apptainer run mantik-test.sif python main.py whatever",
        ]
    )

    arguments = backend._create_arguments(
        entry_point=entry_point, parameters=parameters, storage_dir=storage_dir
    )
    result = example_firecrest_config_long_resources.to_slurm_batch_script(
        arguments=arguments,
        run_id=run_id,
        run_dir=run_dir,
    )

    assert result == expected


def test_create_job_script_apptainer_entry_point_multi_line(
    example_project_path, example_project, example_firecrest_config
):
    entry_point = example_project.get_entry_point("multi-line")
    parameters = {"print": "whatever"}
    storage_dir = "test-dir"
    run_id = str(uuid.uuid4())
    run_dir = pathlib.Path("test-dir")
    expected = "\n".join(
        [
            "#!/bin/bash -l",
            f"#SBATCH --job-name='mantik-{run_id}'",
            "#SBATCH --partition=batch",
            "#SBATCH --constraint=gpu",
            f"#SBATCH --output={run_dir}/mantik.log",
            f"#SBATCH --error={run_dir}/mantik.log",
            'echo "firecREST working directory is $(pwd)"',
            'echo "Submitted batch script:"',
            "cat $(pwd)/script.batch",
            'echo "Changing to Mantik run directory test-dir"',
            f"cd {run_dir}",
            "export MANTIK_WORKING_DIRECTORY=test-dir",
            (
                "srun apptainer run mantik-test.sif python main.py whatever  "
                "--o option1  --i option2"
            ),
        ]
    )

    arguments = backend._create_arguments(
        entry_point=entry_point, parameters=parameters, storage_dir=storage_dir
    )
    result = example_firecrest_config.to_slurm_batch_script(
        arguments=arguments,
        run_id=run_id,
        run_dir=run_dir,
    )
    assert result == expected


def test_create_job_description_python(
    example_project_path, example_project, example_firecrest_config_for_python
):
    entry_point = example_project.get_entry_point("main")
    parameters = {"print": "whatever"}
    storage_dir = "test-dir"
    run_id = str(uuid.uuid4())
    run_dir = pathlib.Path("test-dir")
    expected = "\n".join(
        [
            "#!/bin/bash -l",
            f"#SBATCH --job-name='mantik-{run_id}'",
            "#SBATCH --partition=batch",
            "#SBATCH --constraint=gpu",
            f"#SBATCH --output={run_dir}/mantik.log",
            f"#SBATCH --error={run_dir}/mantik.log",
            'echo "firecREST working directory is $(pwd)"',
            'echo "Submitted batch script:"',
            "cat $(pwd)/script.batch",
            'echo "Changing to Mantik run directory test-dir"',
            f"cd {run_dir}",
            "export MANTIK_WORKING_DIRECTORY=test-dir",
            "precommand compute node && source /venv/bin/activate "
            "&& python main.py "
            "whatever && postcommand compute node",
        ]
    )

    arguments = backend._create_arguments(
        entry_point=entry_point, parameters=parameters, storage_dir=storage_dir
    )
    result = example_firecrest_config_for_python.to_slurm_batch_script(
        arguments=arguments,
        run_id=run_id,
        run_dir=run_dir,
    )
    assert result == expected
