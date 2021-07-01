from dataclasses import dataclass
from typing import List, TypedDict


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
EpiResponse = TypedDict("EpiResponse", {"result": int, "message": str, "epidata": List})
