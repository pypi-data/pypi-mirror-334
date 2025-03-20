import argparse
import ast
import typing as t

import mantik.authentication.auth


def dict_from_list(parameters: t.List[str]) -> t.Dict:
    return dict([_parse_parameter_from_string(p) for p in parameters])


def _parse_parameter_from_string(parameter: str) -> t.Tuple[str, t.Any]:
    key, value = parameter.split("=", 1)
    return key, _parse_value(value)


def _parse_value(value: t.Any) -> t.Any:
    try:
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        # If value is a string, `astr.literal_eval` raises ValueError
        # and in some cases a SyntaxError.
        try:
            return ast.literal_eval(f"'{value}'")
        except (ValueError, SyntaxError):
            raise argparse.ArgumentTypeError(f"Unable to parse {value}")


def access_token_from_env_vars() -> str:
    return mantik.authentication.auth.get_valid_access_token()
