import argparse

import pytest

import mantik.cli.utils


@pytest.mark.parametrize(
    ("string_list", "expected_dict"),
    [
        (
            [
                "n_components=3",
                "n_components2=2.7",
                "data='/opt/data/temperature_level_128'",
                "url==========",
            ],
            {
                "n_components": 3,
                "n_components2": 2.7,
                "data": "/opt/data/temperature_level_128",
                "url": "=========",
            },
        ),
    ],
)
def test_dict_from_list(string_list, expected_dict):
    assert expected_dict == mantik.cli.utils.dict_from_list(string_list)


@pytest.mark.parametrize(
    ("parameter_sting", "expected"),
    [
        ("n_components=3", ("n_components", 3)),
        ("n_components=2.7", ("n_components", 2.7)),
        (
            "data='/opt/data/temperature_level_128_daily_averages_2020.nc'",
            ("data", "/opt/data/temperature_level_128_daily_averages_2020.nc"),
        ),
        (
            'data="/opt/data/temperature_level_128_daily_averages_2020.nc"',
            ("data", "/opt/data/temperature_level_128_daily_averages_2020.nc"),
        ),
        (
            "data=/opt/data/temperature_level_128_daily_averages_2020.nc",
            ("data", "/opt/data/temperature_level_128_daily_averages_2020.nc"),
        ),
        ("url==========", ("url", "=========")),
    ],
)
def test_parse_parameter_from_string(parameter_sting, expected):
    assert expected == mantik.cli.utils._parse_parameter_from_string(
        parameter_sting
    )


@pytest.mark.parametrize(
    ("string", "expected"),
    [
        ("3", 3),
        ("2.7", 2.7),
        (
            "/opt/data/temperature_level_128_daily_averages_2020.nc",
            "/opt/data/temperature_level_128_daily_averages_2020.nc",
        ),
    ],
)
def test_parse_value(string, expected):
    assert expected == mantik.cli.utils._parse_value(string)


def test_parse_value_try_injection():
    injection = "_parse_parameter_from_string('a=2')"
    with pytest.raises(argparse.ArgumentTypeError) as parse_error:
        mantik.cli.utils._parse_value(injection)
    assert f"Unable to parse {injection}" in str(parse_error.value)
