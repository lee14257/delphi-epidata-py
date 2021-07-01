from typing import Iterable, Union
from .model import EpiRange, EpiRangeDict

ARG_TYPE = Union[int, str, EpiRange, EpiRangeDict]


def format_item(value: ARG_TYPE) -> str:
    """Cast values and/or range to a string."""
    if isinstance(value, dict) and "from" in value and "to" in value:
        return f"{value['from']}-{value['to']}"
    return str(value)


def format_list(values: Union[ARG_TYPE, Iterable[ARG_TYPE]]) -> str:
    """Turn a list/tuple of values/ranges into a comma-separated string."""
    list_values = values if isinstance(values, (list, tuple, set)) else [values]
    return ",".join([format_item(value) for value in list_values])
