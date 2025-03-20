import dataclasses
import typing as t
import uuid


@dataclasses.dataclass(frozen=True)
class User:
    user_id: uuid.UUID
    name: str

    @classmethod
    def from_json(cls, data: t.Dict) -> "User":
        return cls(
            user_id=uuid.UUID(data["userId"]),
            name=data["name"],
        )
