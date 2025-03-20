import typing as t


def iterable_to_string(any_list: t.Iterable) -> str:
    return ", ".join(f"{element!r}" for element in any_list)
