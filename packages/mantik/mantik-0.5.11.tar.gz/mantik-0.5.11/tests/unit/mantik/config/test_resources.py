import pytest

import mantik.config as config


class TestResources:
    def test_to_job_script(self):
        expected = (
            "#SBATCH --partition=batch\n"
            "#SBATCH --time=0-01:00:00\n"
            "#SBATCH --nodes=1\n"
            "#SBATCH --ntasks=1\n"
            "#SBATCH --ntasks-per-node=1\n"
            "#SBATCH --gpus-per-node=1\n"
            "#SBATCH --mem=1\n"
            "#SBATCH --reservation=test-reservation\n"
            "#SBATCH --constraint=gpu\n"
            "#SBATCH --qos=test-qos"
        )
        resources = config.resources.Resources(
            queue="batch",
            node_constraints="gpu",
            runtime="1h",
            nodes=1,
            total_cpus=1,
            cpus_per_node=1,
            gpus_per_node=1,
            memory_per_node="1",
            reservation="test-reservation",
            qos="test-qos",
        )
        result = resources.to_slurm_batch_script()
        assert result == expected

    @pytest.mark.parametrize(
        ("time_str", "expected"),
        [
            ("1s", "0-00:00:01"),
            ("30s", "0-00:00:30"),
            ("60s", "0-00:01:00"),
            ("1m", "0-00:01:00"),
            ("30m", "0-00:30:00"),
            ("60m", "0-01:00:00"),
            ("1h", "0-01:00:00"),
            ("12h", "0-12:00:00"),
            ("24h", "1-00:00:00"),
            ("1d", "1-00:00:00"),
            ("2d", "2-00:00:00"),
        ],
    )
    def test_convert_to_slurm_time_format(self, time_str: str, expected):
        result = config.resources._convert_to_slurm_time_format(time_str)

        assert result == expected

    @pytest.mark.parametrize(
        ("time_str", "expected"),
        [
            (
                "1",
                "Unknown runtime unit '1'. Supported time units: s, m, h, d.",
            ),
            (
                "1h30m",
                (
                    "Invalid runtime value. "
                    "Only single unit allowed (30m, 12h, 1d, etc.)"
                ),
            ),
        ],
    )
    def test_convert_to_slurm_time_format_raises(
        self, expect_raise_if_exception, time_str: str, expected
    ):
        with expect_raise_if_exception(ValueError()) as e:
            config.resources._convert_to_slurm_time_format(time_str)

        assert str(e.value) == expected
