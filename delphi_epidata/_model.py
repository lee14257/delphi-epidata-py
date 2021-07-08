from dataclasses import dataclass
from enum import Enum
from datetime import date
from urllib.parse import urlencode
from typing import Iterable, List, Mapping, Optional, Tuple, TypedDict, Union

EpiRangeDict = TypedDict("EpiRangeDict", {"from": int, "to": int})
EpiRangeLike = Union[int, str, "EpiRange", EpiRangeDict, date]


def format_date(d: Union[int, str, date]) -> str:
    if isinstance(d, date):
        # YYYYMMDD
        return d.strftime("%Y%m%d")
    return str(d)


def format_item(value: EpiRangeLike) -> str:
    """Cast values and/or range to a string."""
    if isinstance(value, date):
        return format_date(value)
    if isinstance(value, Enum):
        return str(value.value)
    if isinstance(value, EpiRange):
        return str(value)
    if isinstance(value, dict) and "from" in value and "to" in value:
        return f"{format_item(value['from'])}-{format_item(value['to'])}"
    return str(value)


def format_list(values: Union[EpiRangeLike, Iterable[EpiRangeLike]]) -> str:
    """Turn a list/tuple of values/ranges into a comma-separated string."""
    list_values = values if isinstance(values, (list, tuple, set)) else [values]
    return ",".join([format_item(value) for value in list_values])


@dataclass(repr=False)
class EpiRange:
    """
    Range object for dates/epiweeks
    """

    start: Union[int, date, str]
    end: Union[int, date, str]

    def __post_init__(self) -> None:
        # swap if wrong order
        # complicated construct for typing inference
        if (isinstance(self.end, date) and isinstance(self.start, date) and self.end < self.start) or (
            (isinstance(self.end, int) and isinstance(self.start, int) and self.end < self.start)
            or (isinstance(self.end, str) and isinstance(self.start, str) and self.end < self.start)
        ):
            self.start, self.end = self.end, self.start

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"{format_date(self.start)}-{format_date(self.end)}"


EpiDataResponse = TypedDict("EpiDataResponse", {"result": int, "message": str, "epidata": List})


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

    def _formatted_paramters(
        self, format_type: Optional[EpiDataFormatType] = None, fields: Optional[Iterable[str]] = None
    ) -> Mapping[str, str]:
        """
        format this call into a [URL, Params] tuple
        """
        all_params = dict(self._params)
        if format_type and format_type != EpiDataFormatType.classic:
            all_params["format"] = format_type
        if fields:
            all_params["fields"] = fields
        return {k: format_list(v) for k, v in all_params.items() if v is not None}

    def request_arguments(
        self, format_type: Optional[EpiDataFormatType] = None, fields: Optional[Iterable[str]] = None
    ) -> Tuple[str, Mapping[str, str]]:
        """
        format this call into a [URL, Params] tuple
        """
        formatted_params = self._formatted_paramters(format_type, fields)
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

    def __repr__(self) -> str:
        return f"EpiDataCall(endpoint={self._endpoint}, params={self._formatted_paramters()})"

    def __str__(self) -> str:
        return self.request_url()
