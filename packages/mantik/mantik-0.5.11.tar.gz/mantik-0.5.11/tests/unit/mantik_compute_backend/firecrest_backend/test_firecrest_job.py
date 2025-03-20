import pathlib

import mantik.testing as testing
import mantik_compute_backend.firecrest._properties as _properties
import mantik_compute_backend.firecrest.job as _job


class TestJob:
    def test_wait(self):
        job = _job.Job(
            client=testing.firecrest.FakeClient(),
            machine="test-machine",
            job_id="test-job-id",
            job_dir=pathlib.Path("test-rundir"),
        )
        job.wait()
        assert job.status == _properties.Status.COMPLETED
