import dataclasses
import typing as t

import mantik.config._base as _base
import mantik.config._utils as _utils


@dataclasses.dataclass
class Firecrest(_base.ConfigObject):
    api_url: str
    token_url: str
    machine: str

    @classmethod
    def _from_dict(cls, config: t.Dict) -> "Firecrest":
        api_url = _utils.get_required_config_value(
            name="ApiUrl",
            value_type=str,
            config=config,
        )
        token_url = _utils.get_required_config_value(
            name="TokenUrl",
            value_type=str,
            config=config,
        )
        machine = _utils.get_required_config_value(
            name="Machine",
            value_type=str,
            config=config,
        )
        return cls(api_url=api_url, token_url=token_url, machine=machine)

    def _to_dict(self) -> t.Dict:
        return {
            "ApiUrl": self.api_url,
            "TokenUrl": self.token_url,
            "Machine": self.machine,
        }
