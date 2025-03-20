import pathlib

import mlflow.entities as entities
import pytest

import mantik.testing as testing
import mantik.testing.pyunicore as test_unicore
import mantik_compute_backend.firecrest._properties as _firecrest_properties
import mantik_compute_backend.firecrest.job as _job
import mantik_compute_backend.submitted_run as _submitted_run
import mantik_compute_backend.unicore._properties as _unicore_properties

FILE_DIR = pathlib.Path(__file__).parent


class TestSubmittedRunFirecrest:
    @pytest.mark.parametrize(
        "status", [e.value for e in _firecrest_properties.Status]
    )
    def test_get_status(self, status: str):
        job = _job.Job(
            client=testing.firecrest.FakeClient(job_status=status),
            machine="test-machine",
            job_id="test-job-id",
            job_dir=pathlib.Path("test-rundir"),
        )
        submitted_run = _submitted_run.SubmittedRun(
            run_id="test-run-id", job=job
        )
        submitted_run.get_status()

    def test_wait(self):
        job = _job.Job(
            client=testing.firecrest.FakeClient(
                job_status=_firecrest_properties.Status.COMPLETED.value
            ),
            machine="test-machine",
            job_id="test-job-id",
            job_dir=pathlib.Path("test-rundir"),
        )
        submitted_run = _submitted_run.SubmittedRun(
            run_id="test-run-id", job=job
        )
        submitted_run.wait()
        assert submitted_run.get_status() == entities.RunStatus.FINISHED


class TestSubmittedRunUnicore:
    def test_run_id(self):
        run = test_unicore._create_run()
        expected = "test-job"

        result = run.run_id

        assert result == expected

    @pytest.mark.parametrize(
        ("will_be_successful", "expected"),
        [
            (
                True,
                True,
            ),
            (
                False,
                False,
            ),
        ],
    )
    def test_wait(self, will_be_successful, expected):
        run = test_unicore._create_run(
            will_be_successful=will_be_successful,
        )
        result = run.wait()

        assert result == expected

    @pytest.mark.parametrize(
        ("status", "expected"),
        [
            (
                _unicore_properties.Status.STAGING_IN,
                entities.RunStatus.SCHEDULED,
            ),
            (
                _unicore_properties.Status.READY,
                entities.RunStatus.SCHEDULED,
            ),
            (
                _unicore_properties.Status.QUEUED,
                entities.RunStatus.SCHEDULED,
            ),
            (
                _unicore_properties.Status.RUNNING,
                entities.RunStatus.RUNNING,
            ),
            (
                _unicore_properties.Status.STAGING_OUT,
                entities.RunStatus.RUNNING,
            ),
            (
                _unicore_properties.Status.SUCCESSFUL,
                entities.RunStatus.FINISHED,
            ),
            (
                _unicore_properties.Status.FAILED,
                entities.RunStatus.FAILED,
            ),
            (
                _unicore_properties.Status.UNKNOWN,
                entities.RunStatus.RUNNING,
            ),
        ],
    )
    def test_get_status(self, status, expected):
        run = test_unicore._create_run(status=status)
        result = run.get_status()

        assert result == expected

    def test_cancel(self):
        run = test_unicore._create_run()

        run.cancel()
