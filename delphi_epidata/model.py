from dataclasses import dataclass
from enum import Enum
from typing import Iterable, List, TypedDict, Union


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


class EpiDataFormatType(str, Enum):
    """
    possible formatting options for API calls
    """

    json = "json"
    classic = "classic"
    csv = "csv"
    jsonl = "jsonl"


class InvalidArgumentException(Exception):
    """
    exception
    """
