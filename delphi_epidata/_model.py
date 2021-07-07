from dataclasses import dataclass
from enum import Enum
from urllib.parse import urlencode
from typing import Iterable, List, Mapping, Optional, Tuple, TypedDict, Union


@dataclass(repr=False)
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

    def __repr__(self) -> str:
        return str(self)

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


def format_item(value: EpiRangeLike) -> str:
    """Cast values and/or range to a string."""
    if isinstance(value, Enum):
        return str(value.value)
    if isinstance(value, EpiRange):
        return str(value)
    if isinstance(value, dict) and "from" in value and "to" in value:
        return f"{value['from']}-{value['to']}"
    return str(value)


def format_list(values: Union[EpiRangeLike, Iterable[EpiRangeLike]]) -> str:
    """Turn a list/tuple of values/ranges into a comma-separated string."""
    list_values = values if isinstance(values, (list, tuple, set)) else [values]
    return ",".join([format_item(value) for value in list_values])


class AEpiDataCall:
    """
    base epidata call class
    """

    def __init__(
        self,
        base_url: str,
        endpoint: str,
        params: Mapping[str, Union[None, EpiRangeLike, Iterable[EpiRangeLike]]],
    ) -> None:
        self._base_url = base_url
        self._endpoint = endpoint
        self._params = params

    def request_arguments(
        self, format_type: Optional[EpiDataFormatType] = None, fields: Optional[Iterable[str]] = None
    ) -> Tuple[str, Mapping[str, str]]:
        """
        format this call into a [URL, Params] tuple
        """
        all_params = dict(self._params)
        if format_type and format_type != EpiDataFormatType.classic:
            all_params["format"] = format_type
        if fields:
            all_params["fields"] = fields
        formatted_params = {k: format_list(v) for k, v in all_params.items() if v is not None}
        full_url = self._full_url()
        return full_url, formatted_params

    def _full_url(self) -> str:
        """
        combines the endpoint with the given base url
        """
        url = self._base_url
        if not url.endswith("/"):
            url += "/"
        url += self._endpoint
        return url

    def request_url(
        self,
        format_type: Optional[EpiDataFormatType] = None,
        fields: Optional[Iterable[str]] = None,
    ) -> str:
        """
        format this call into a full HTTP request url with encoded parameters
        """
        u, p = self.request_arguments(format_type, fields)
        query = urlencode(p)
        if query:
            return f"{u}?{query}"
        return u
