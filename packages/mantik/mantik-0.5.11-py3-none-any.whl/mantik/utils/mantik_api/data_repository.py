import dataclasses
import typing as t
import uuid

import mantik.utils.mantik_api.client as client


@dataclasses.dataclass
class DataRepository:
    uri: str
    is_dvc_enabled: bool
    dvc_connection_id: t.Optional[uuid.UUID]
    connection_id: t.Optional[uuid.UUID]
    versions: t.Dict[str, str]
    platform: str

    @classmethod
    def from_json(cls, response: dict):
        return cls(
            uri=response["uri"],
            is_dvc_enabled=response["isDvcEnabled"],
            dvc_connection_id=uuid.UUID(response["dvcConnectionId"])
            if response.get("dvcConnectionId")
            else None,
            connection_id=uuid.UUID(response["connectionId"])
            if response.get("connectionId")
            else None,
            versions=response["versions"] or {},
            platform=response["platform"],
        )


def get_all(
    project_id: uuid.UUID,
    token: str,
) -> t.List[t.Dict]:
    endpoint = f"/projects/{str(project_id)}/data"
    response = client.send_request_to_mantik_api(
        method="GET", data={}, url_endpoint=endpoint, token=token
    )
    return response.json()["dataRepositories"]


def get_one(
    project_id: uuid.UUID,
    data_repository_id: uuid.UUID,
    token: str,
) -> DataRepository:
    endpoint = f"/projects/{str(project_id)}/data/{str(data_repository_id)}"
    response = client.send_request_to_mantik_api(
        method="GET", data={}, url_endpoint=endpoint, token=token
    )
    return DataRepository.from_json(response.json())
