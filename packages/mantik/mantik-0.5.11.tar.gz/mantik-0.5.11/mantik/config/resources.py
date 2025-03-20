import dataclasses
import typing as t

import mantik.config._base as _base
import mantik.config._utils as _utils


@dataclasses.dataclass
class Resources(_base.ConfigObject):
    """The computing resources that will be requested ."""

    queue: str
    runtime: t.Optional[str] = None
    nodes: t.Optional[int] = None
    total_cpus: t.Optional[int] = None
    cpus_per_node: t.Optional[int] = None
    gpus_per_node: t.Optional[int] = None
    memory_per_node: t.Optional[str] = None
    reservation: t.Optional[str] = None
    node_constraints: t.Optional[str] = None
    qos: t.Optional[str] = None

    @classmethod
    def _from_dict(cls, config: t.Dict) -> "Resources":
        queue = _utils.get_required_config_value(
            name="Queue",
            value_type=str,
            config=config,
        )
        runtime = _utils.get_optional_config_value(
            name="Runtime",
            value_type=str,
            config=config,
        )
        nodes = _utils.get_optional_config_value(
            name="Nodes",
            value_type=int,
            config=config,
        )
        total_cpus = _utils.get_optional_config_value(
            name="TotalCPUs",
            value_type=int,
            config=config,
        )
        cpus_per_node = _utils.get_optional_config_value(
            name="CPUsPerNode",
            value_type=int,
            config=config,
        )
        gpus_per_node = _utils.get_optional_config_value(
            name="GPUsPerNode",
            value_type=int,
            config=config,
        )
        memory_per_node = _utils.get_optional_config_value(
            name="MemoryPerNode",
            value_type=str,
            config=config,
        )
        reservation = _utils.get_optional_config_value(
            name="Reservation",
            value_type=str,
            config=config,
        )
        node_constraints = _utils.get_optional_config_value(
            name="NodeConstraints",
            value_type=str,
            config=config,
        )
        qos = _utils.get_optional_config_value(
            name="QoS",
            value_type=str,
            config=config,
        )
        return cls(
            queue=queue,
            runtime=runtime,
            nodes=nodes,
            total_cpus=total_cpus,
            cpus_per_node=cpus_per_node,
            gpus_per_node=gpus_per_node,
            memory_per_node=memory_per_node,
            reservation=reservation,
            node_constraints=node_constraints,
            qos=qos,
        )

    def _to_dict(self) -> t.Dict:
        return {
            "Runtime": self.runtime,
            "Queue": self.queue,
            "Nodes": self.nodes,
            "TotalCPUs": self.total_cpus,
            "CPUsPerNode": self.cpus_per_node,
            "GPUS": self.gpus_per_node,
            "MemoryPerNode": self.memory_per_node,
            "Reservation": self.reservation,
            "NodeConstraints": self.node_constraints,
            "QoS": self.qos,
        }

    def to_slurm_batch_script(self):
        sbatch_options_list = [f"#SBATCH --partition={self.queue}"]
        if self.runtime is not None:
            sbatch_options_list.append(
                f"#SBATCH --time={_convert_to_slurm_time_format(self.runtime)}"
            )
        if self.nodes is not None:
            sbatch_options_list.append(f"#SBATCH --nodes={self.nodes}")
        if self.total_cpus is not None:
            sbatch_options_list.append(f"#SBATCH --ntasks={self.total_cpus}")
        if self.cpus_per_node is not None:
            sbatch_options_list.append(
                f"#SBATCH --ntasks-per-node={self.cpus_per_node}"
            )
        if self.gpus_per_node is not None:
            sbatch_options_list.append(
                f"#SBATCH --gpus-per-node={self.gpus_per_node}"
            )
        if self.memory_per_node is not None and int(self.memory_per_node) >= 0:
            sbatch_options_list.append(f"#SBATCH --mem={self.memory_per_node}")
        if self.reservation is not None:
            sbatch_options_list.append(
                f"#SBATCH --reservation={self.reservation}"
            )
        if self.node_constraints is not None:
            sbatch_options_list.append(
                f"#SBATCH --constraint={self.node_constraints}"
            )
        if self.qos is not None:
            sbatch_options_list.append(f"#SBATCH --qos={self.qos}")
        return "\n".join(sbatch_options_list)


def _convert_to_slurm_time_format(input_time: str) -> str:
    """Convert a given time string to the expected format of the `--time`
    option of Slurm.

    UNICORE allows to define time using strings with `d`, `h`, `m`, `s` units.
    Hence, we must convert them here to be consistent with UNICORE.

    """

    if input_time == "0":
        return input_time

    units = {"s": 1, "m": 60, "h": 3600, "d": 86400}

    number, unit = input_time[:-1], input_time[-1]

    # Ensure that given unit (last string character)
    # is a supported time unit.
    if unit not in units:
        time_units = ", ".join(units.keys())
        raise ValueError(
            f"Unknown runtime unit '{unit}'. "
            f"Supported time units: {time_units}."
        )

    # Verify given number.
    # It may be a combination of multiple time units,
    # which is not allowed (UNICORE doesn't support this).
    # E.g. 1h30m is not allowed.
    try:
        value = int(number)
    except ValueError as e:
        raise ValueError(
            "Invalid runtime value. "
            "Only single unit allowed (30m, 12h, 1d, etc.)"
        ) from e

    # Convert the input time to total seconds
    seconds = value * units.get(unit)

    # Convert seconds to target format
    days, remainder = divmod(seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    return f"{days}-{hours:02}:{minutes:02}:{seconds:02}"
