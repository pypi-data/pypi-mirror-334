import dataclasses
import typing as t
import uuid

import mantik.utils.mantik_api.client as client


@dataclasses.dataclass
class ExperimentRepository:
    experiment_repository_id: uuid.UUID
    mlflow_experiment_id: str
    name: str
    artifact_location: t.Optional[str]

    @classmethod
    def from_json(cls, json_str):
        return cls(
            experiment_repository_id=uuid.UUID(
                json_str["experimentRepositoryId"]
            ),
            mlflow_experiment_id=json_str["mlflowExperimentId"],
            name=json_str["name"],
            artifact_location=json_str.get("artifactLocation"),
        )

    def to_json(self):
        return {
            "experimentRepositoryId": str(self.experiment_repository_id),
            "mlflowExperimentId": self.mlflow_experiment_id,
            "name": self.name,
            "artifact_location": self.artifact_location,
        }


def get_one(
    experiment_repository_id: uuid.UUID,
    project_id: uuid.UUID,
    token: str,
) -> ExperimentRepository:
    """Retrieves an experiment repository entry from the Mantik API"""

    endpoint = f"/projects/{str(project_id)}/experiments/{str(experiment_repository_id)}"  # noqa
    response = client.send_request_to_mantik_api(
        method="GET", data={}, url_endpoint=endpoint, token=token
    )
    return ExperimentRepository.from_json(response.json())


def get_unique_run_name(
    experiment_repository_id: uuid.UUID,
    project_id: uuid.UUID,
    token: str,
    run_name: str,
) -> str:
    """Retrieves a unique mlflow run name from the Mantik API"""

    endpoint = f"/projects/{str(project_id)}/experiments/{str(experiment_repository_id)}/unique-mlflow-run-name"  # noqa
    response = client.send_request_to_mantik_api(
        method="GET",
        data={},
        url_endpoint=endpoint,
        token=token,
        query_params={"runName": run_name},
    )
    return response.json()
