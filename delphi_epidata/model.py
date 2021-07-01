from dataclasses import dataclass
from typing import Iterable, List, Mapping, TypedDict, Union


@dataclass
class EpiRange:
    """
    Range object for dates/epiweeks
    """

    start: int
    end: int

    def __post_init__(self) -> None:
        # swap if wrong order
        if self.end < self.start:
            self.start, self.end = self.end, self.start

    def __str__(self) -> str:
        return f"{self.start}-{self.end}"


EpiRangeDict = TypedDict("EpiRangeDict", {"from": int, "to": int})
EpiDataResponse = TypedDict("EpiDataResponse", {"result": int, "message": str, "epidata": List})

EpiRangeLike = Union[int, str, EpiRange, EpiRangeDict]

EpiRangeParam = Union[EpiRangeLike, Iterable[EpiRangeLike]]
StringParam = Union[str, Iterable[str]]
IntParam = Union[int, Iterable[int]]


def _format_item(value: EpiRangeLike) -> str:
    """Cast values and/or range to a string."""
    if isinstance(value, dict) and "from" in value and "to" in value:
        return f"{value['from']}-{value['to']}"
    return str(value)


def _format_list(values: Union[EpiRangeLike, Iterable[EpiRangeLike]]) -> str:
    """Turn a list/tuple of values/ranges into a comma-separated string."""
    list_values = values if isinstance(values, (list, tuple, set)) else [values]
    return ",".join([_format_item(value) for value in list_values])


@dataclass
class EpiDataCall:
    """
    epi data call definition
    """

    endpoint: str
    """
    endpoint to call
    """
    params: Mapping[str, Union[None, EpiRangeLike, Iterable[EpiRangeLike]]]
    """
    parameters for the call
    """

    @property
    def formatted_params(self) -> Mapping[str, str]:
        """
        format the parameters such that they can be transferred
        """
        return {k: _format_list(v) for k, v in self.params.items() if v is not None}


class InvalidArgumentException(Exception):
    """
    exception
    """

    pass
