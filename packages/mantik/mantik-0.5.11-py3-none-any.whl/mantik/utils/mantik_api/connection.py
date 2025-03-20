import dataclasses
import typing as t
import uuid

import mantik.utils.mantik_api.client as client
import mantik.utils.mantik_api.user as _user


@dataclasses.dataclass(frozen=True)
class Connection:
    """
    Model for the Connection credentials delivered by Mantik API.

    Attributes
    ----------
    name: the name of the Connection
    username: the username of the Connection credentials
    password: the password of the Connection credentials
    """

    connection_id: uuid.UUID
    user: _user.User
    connection_name: str
    connection_provider: str
    auth_method: str
    login_name: t.Optional[str] = None
    password: t.Optional[str] = None
    token: t.Optional[str] = None

    @classmethod
    def from_json(cls, data: t.Dict) -> "Connection":
        return cls(
            connection_id=uuid.UUID(data["connectionId"]),
            user=_user.User.from_json(data["user"]),
            connection_name=data["connectionName"],
            connection_provider=data["connectionProvider"],
            auth_method=data["authMethod"],
            login_name=data.get("loginName"),
            password=data.get("password"),
            token=data.get("token"),
        )


def get(
    user_id: uuid.UUID,
    connection_id: uuid.UUID,
    token: str,
) -> Connection:
    endpoint = f"/users/{user_id}/settings/connections/{connection_id}"
    response = client.send_request_to_mantik_api(
        method="GET", data={}, url_endpoint=endpoint, token=token
    ).json()

    return Connection.from_json(response)
