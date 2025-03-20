import dataclasses
import typing as t
import uuid

import mantik.utils.mantik_api.client as client


@dataclasses.dataclass
class CodeRepository:
    code_repository_id: uuid.UUID
    code_repository_name: str
    uri: str
    connection_id: t.Optional[str]
    platform: str

    @classmethod
    def from_json(cls, json_str):
        return cls(
            code_repository_id=uuid.UUID(json_str["codeRepositoryId"]),
            code_repository_name=json_str["codeRepositoryName"],
            uri=json_str["uri"],
            connection_id=json_str["connectionId"],
            platform=json_str["platform"],
        )

    def to_json(self):
        return {
            "codeRepositoryId": str(self.code_repository_id),
            "codeRepositoryName": self.code_repository_name,
            "uri": self.uri,
            "connectionId": self.connection_id,
            "platform": self.platform,
        }


def get_one(
    code_repository_id: uuid.UUID,
    project_id: uuid.UUID,
    token: str,
) -> CodeRepository:
    """Retrieves a code repository entry from the Mantik API"""

    endpoint = f"/projects/{str(project_id)}/code/{str(code_repository_id)}"
    response = client.send_request_to_mantik_api(
        method="GET", data={}, url_endpoint=endpoint, token=token
    )
    return CodeRepository.from_json(response.json())
