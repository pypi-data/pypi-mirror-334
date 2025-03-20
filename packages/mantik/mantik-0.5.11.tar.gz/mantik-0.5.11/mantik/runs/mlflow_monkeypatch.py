"""MLflow local run function.

This source file contains code from [MLflow](https://github.com/mlflow/mlflow)
licensed under Apache-2.0 license, see
[here](https://github.com/mlflow/mlflow/blob/1eef4641df6f605b7d9faa83b0fc25e65877dbf4/LICENSE.txt)
for the original license.

Changes made to the original source code are denoted as such with comments.

For Mantik developers
NOTE: this has to be kept up to date with the different Mlflow versions.

If any changes occur in the original code that can be found here:
https://github.com/mlflow/mlflow/blob/master/mlflow/projects/backend/local.py
"""
import io
import os
import subprocess
import sys

import mlflow


def run_entry_point(command, work_dir, experiment_id, run_id):
    """
    Run an entry point command in a subprocess,
    returning a SubmittedRun that can be used to
    query the run's status.

    Args:
        command: Entry point command to run
        work_dir: Working directory in which to run the command
        run_id: MLflow run ID associated with the entry point execution.
    """
    env = os.environ.copy()
    env.update(mlflow.projects.utils.get_run_env_vars(run_id, experiment_id))
    try:
        env.update(
            mlflow.utils.databricks_utils.get_databricks_env_vars(
                tracking_uri=mlflow.get_tracking_uri()
            )
        )
    except AttributeError:
        env.update(
            mlflow.projects.utils.get_databricks_env_vars(
                tracking_uri=mlflow.get_tracking_uri()
            )
        )
    mlflow.projects.backend.local._logger.info(
        "=== Running command '%s' in run with ID '%s' === ", command, run_id
    )
    # in case os name is not 'nt', we are not running on windows. It introduces
    # bash command otherwise.

    # MANTIK COMMENT
    # Added next line to avoid buffering of output
    # so that we can print it real time
    env["PYTHONUNBUFFERED"] = "1"

    # MANTIK COMMENT
    # Changed next lines to capture output of
    # mantik run subprocess to print it in main process
    # What Changed (All changes refer both to the windows and linux subprocess):
    # - subprocess.Popen called with a context manager
    # - stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    #   and bufsize=-1 added to subprocess.Popen
    # - Added indented lines in the context manager
    #   to print in real time here
    #   in the main process the logs of the subprocess
    if os.name != "nt":
        with subprocess.Popen(
            ["bash", "-c", command],
            close_fds=True,
            cwd=work_dir,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=-1,
        ) as process:
            for line in io.TextIOWrapper(process.stdout, newline=""):
                print(line, flush=True, end="")
    else:
        with subprocess.Popen(
            ["cmd", "/c", command],
            close_fds=True,
            cwd=work_dir,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=-1,
        ) as process:
            for line in io.TextIOWrapper(process.stderr, newline=""):
                print(line, flush=True, end="")
    return mlflow.projects.submitted_run.LocalSubmittedRun(run_id, process)


def run_mlflow_run_cmd(mlflow_run_arr, env_map):
    """
    Invoke ``mlflow run`` in a subprocess,
    which in turn runs the entry point in a child process.
    Returns a handle to the subprocess. Popen launched to invoke ``mlflow run``.
    """
    final_env = os.environ.copy()
    final_env.update(env_map)
    # Launch `mlflow run` command
    # as the leader of its own process group so that we can do a
    # best-effort cleanup of all its descendant processes if needed

    # MANTIK COMMENT
    # Added next line to avoid buffering of output
    # so that we can print it real time
    final_env["PYTHONUNBUFFERED"] = "1"

    # MANTIK COMMENT
    # Changed next lines to capture output of
    # mantik run subprocess to print it in main process
    # What Changed (All changes refer both to the windows and linux subprocess):
    # - subprocess.Popen called with a context manager
    # - stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    #   and bufsize=-1 added to subprocess.Popen
    # - Added indented lines in the context manager
    #   to print in real time here
    #   in the main process the logs of the subprocess
    # - Remove text=True from subprocess.Popen so that output is a bytestream
    if sys.platform == "win32":
        with subprocess.Popen(
            mlflow_run_arr,
            env=final_env,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=-1,
        ) as process:
            for line in io.TextIOWrapper(process.stderr, newline=""):
                print(line, flush=True, end="")
        return process
    else:
        with subprocess.Popen(
            mlflow_run_arr,
            env=final_env,
            preexec_fn=os.setsid,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=-1,
        ) as process:
            for line in io.TextIOWrapper(process.stderr, newline=""):
                print(line, flush=True, end="")
        return process
