import dataclasses
import typing as t

import mantik.config._base as _base
import mantik.config._utils as _utils


@dataclasses.dataclass
class SSHRemoteComputeSystem(_base.ConfigObject):
    hostname: str
    port: t.Optional[str]

    @classmethod
    def _from_dict(cls, config: t.Dict) -> "SSHRemoteComputeSystem":
        hostname = _utils.get_required_config_value(
            name="Hostname",
            value_type=str,
            config=config,
        )
        port = _utils.get_optional_config_value(
            name="Port",
            value_type=str,
            config=config,
        )

        return cls(hostname=hostname, port=port)

    def _to_dict(self) -> t.Dict:
        return {
            "Hostname": self.hostname,
            "Port": self.port,
        }
