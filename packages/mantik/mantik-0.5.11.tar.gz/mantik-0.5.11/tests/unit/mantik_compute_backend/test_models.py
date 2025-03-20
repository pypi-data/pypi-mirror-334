import uuid

import mantik_compute_backend.models as models


def test_submit_run_response():
    run_id = uuid.uuid4()
    response = models.SubmitRunResponse(
        experiment_id=1,
        run_id=run_id,
        unicore_job_id="3",
        tracking_uri="foo.bar",
    )
    assert response.experiment_id == 1
    assert response.run_id == run_id
    assert response.unicore_job_id == "3"
