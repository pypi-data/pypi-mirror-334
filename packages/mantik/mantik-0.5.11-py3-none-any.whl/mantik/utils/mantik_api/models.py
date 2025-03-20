"""Interact with trained models in mantik api"""
import dataclasses
import logging
import typing as t
import uuid

import mantik.utils.mantik_api.client as client

logger = logging.getLogger(__name__)

T = t.TypeVar("T")


def optional_cast(_type: T, optional_value: t.Optional[t.Any]) -> t.Optional[T]:
    if optional_value is None:
        return None

    return _type(optional_value)


class InvalidModelError(Exception):
    """The given model payload is invalid"""


@dataclasses.dataclass
class ModelBase:
    name: str


@dataclasses.dataclass
class ModelBaseKeywords:
    uri: t.Optional[str] = None
    location: t.Optional[str] = None
    connection_id: t.Optional[uuid.UUID] = None
    run_id: t.Optional[uuid.UUID] = None
    mlflow_parameters: t.Optional[dict] = None


@dataclasses.dataclass
class GetModelNoKeywords(ModelBase):
    model_id: uuid.UUID
    status: str


@dataclasses.dataclass
class GetModel(ModelBaseKeywords, GetModelNoKeywords):
    @classmethod
    def from_json(cls, json_str):
        return cls(
            model_id=uuid.UUID(json_str["modelId"]),
            uri=json_str["uri"],
            location=json_str["location"],
            connection_id=optional_cast(uuid.UUID, json_str["connectionId"]),
            mlflow_parameters=json_str["mlflowParameters"],
            status=json_str["status"],
            run_id=optional_cast(uuid.UUID, json_str["runId"]),
            name=json_str["name"],
        )


@dataclasses.dataclass
class PostPutModel(ModelBaseKeywords, ModelBase):
    def to_dict(self):
        return {
            "uri": self.uri,
            "location": self.location,
            "connectionId": optional_cast(str, self.connection_id),
            "mlflowParameters": self.mlflow_parameters,
            "runId": optional_cast(str, self.run_id),
            "name": self.name,
        }

    def validate(self):
        if self.run_id and (self.uri and self.location):
            # The precedence is enforced here:
            # https://gitlab.com/mantik-ai/mantik-api/-/blob/main/src/mantik_api/
            # routes/project_routes/model_repository.py?ref_type=heads#L433-436
            logger.warning(
                "If both (run ID) and "
                "(uri and location) are defined the (run ID) takes precedence, "
                "and (uri and location) will be overwritten."
            )
        if (self.run_id is None) and (
            self.uri is None and self.location is None
        ):
            raise InvalidModelError(
                "To add a model either (run ID) or "
                "(uri and location) must be given."
            )


def get_all(
    project_id: uuid.UUID,
    token: str,
) -> t.List[GetModel]:
    """Retrieves trained model entries through the Mantik API"""

    endpoint = f"/projects/{str(project_id)}/models/trained"
    response = client.send_request_to_mantik_api(
        method="GET", data={}, url_endpoint=endpoint, token=token
    )
    return [GetModel.from_json(model) for model in response.json()["models"]]


def get_one(
    project_id: uuid.UUID,
    model_id: uuid.UUID,
    token: str,
) -> GetModel:
    """Retrieves a trained model entry from the Mantik API"""

    endpoint = f"/projects/{str(project_id)}/models/trained/{str(model_id)}"
    response = client.send_request_to_mantik_api(
        method="GET", data={}, url_endpoint=endpoint, token=token
    )
    return GetModel.from_json(response.json())


def delete(
    project_id: uuid.UUID,
    model_id: uuid.UUID,
    token: str,
):
    """Deletes a trained model entry through the Mantik API"""

    endpoint = f"/projects/{str(project_id)}/models/trained/{str(model_id)}"
    client.send_request_to_mantik_api(
        method="DELETE", data={}, url_endpoint=endpoint, token=token
    )
    logger.info(f"Model with ID: {model_id} has been deleted")


def add(
    new_model_schema: PostPutModel,
    project_id: uuid.UUID,
    token: str,
) -> uuid.UUID:
    """Creates a trained model entry through the Mantik API"""

    new_model_schema.validate()
    data = new_model_schema.to_dict()
    endpoint = f"/projects/{str(project_id)}/models/trained"
    response = client.send_request_to_mantik_api(
        method="POST", data=data, url_endpoint=endpoint, token=token
    )
    new_model_id = response.json()["modelId"]
    logger.info(f"A model with ID: {new_model_id} has been created")

    return uuid.UUID(new_model_id)


def update(
    updated_model_schema: PostPutModel,
    project_id: uuid.UUID,
    model_id: uuid.UUID,
    token: str,
):
    """Updates a trained model entry through the Mantik API"""

    data = updated_model_schema.to_dict()
    endpoint = f"/projects/{str(project_id)}/models/trained/{str(model_id)}"
    client.send_request_to_mantik_api(
        method="PUT", data=data, url_endpoint=endpoint, token=token
    )
    logger.info(f"Model with ID: {str(model_id)} has been updated")


def get_image_url(
    project_id: uuid.UUID,
    model_id: uuid.UUID,
    token: str,
) -> str:
    """Retrieves a download url
    for a containerized trained model from the Mantik API"""

    endpoint = (
        f"/projects/{str(project_id)}/models/trained/{str(model_id)}/docker"
    )
    response = client.send_request_to_mantik_api(
        method="GET", data={}, url_endpoint=endpoint, token=token
    )
    return response.json()["url"]


def start_build(
    project_id: uuid.UUID,
    model_id: uuid.UUID,
    token: str,
) -> None:
    """Trigger the build for a containerized trained model
    from the Mantik API"""

    endpoint = (
        f"/projects/{str(project_id)}/models/trained/"
        f"{str(model_id)}/docker/build"
    )
    client.send_request_to_mantik_api(
        method="POST", data={}, url_endpoint=endpoint, token=token
    )
    logger.info(f"Building container for model with ID: {str(model_id)}")
