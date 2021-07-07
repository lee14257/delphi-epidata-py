from urllib.parse import urlencode
from json import loads
from typing import (
    Dict,
    Generator,
    Generic,
    Iterable,
    List,
    Mapping,
    Optional,
    Tuple,
    Union,
    cast,
)
from requests import Response, Session
from pandas import DataFrame

from .model import EpiDataFormatType, EpiDataResponse, EpiRangeLike
from ._constants import BASE_URL
from ._utils import format_list, request_with_retry
from .endpoints import AEpiDataEndpoints, RESULT_TYPE


class AEpiDataRequest(AEpiDataEndpoints[RESULT_TYPE], Generic[RESULT_TYPE]):
    """
    base class for calling the API
    """

    def __init__(
        self,
        base_url: str = BASE_URL,
        fields: Optional[Iterable[str]] = None,
        session: Optional[Session] = None,
    ) -> None:
        super().__init__()
        self._base_url = base_url
        self._fields = fields
        self._session = session

    def request_arguments(
        self,
        endpoint: str,
        params: Mapping[str, Union[None, EpiRangeLike, Iterable[EpiRangeLike]]],
        format_type: Optional[EpiDataFormatType] = None,
    ) -> Tuple[str, Mapping[str, str]]:
        """
        format this call into a [URL, Params] tuple
        """
        all_params = dict(params)
        if format_type and format_type != EpiDataFormatType.classic:
            all_params["format"] = format_type
        if self._fields:
            all_params["fields"] = self._fields
        formatted_params = {k: format_list(v) for k, v in all_params.items() if v is not None}
        full_url = self._full_url(endpoint)
        return full_url, formatted_params

    def _full_url(self, endpoint: str) -> str:
        """
        combines the endpoint with the given base url
        """
        url = self._base_url
        if not url.endswith("/"):
            url += "/"
        url += endpoint
        return url

    def request_url(
        self,
        endpoint: str,
        params: Mapping[str, Union[None, EpiRangeLike, Iterable[EpiRangeLike]]],
        format_type: Optional[EpiDataFormatType] = None,
    ) -> str:
        """
        format this call into a full HTTP request url with encoded parameters
        """
        u, p = self.request_arguments(endpoint, params, format_type)
        query = urlencode(p)
        if query:
            return f"{u}?{query}"
        return u

    def _call(
        self,
        endpoint: str,
        params: Mapping[str, Union[None, EpiRangeLike, Iterable[EpiRangeLike]]],
        format_type: Optional[EpiDataFormatType] = None,
        stream: bool = False,
    ) -> Response:
        url, params = self.request_arguments(endpoint, params, format_type)
        return request_with_retry(url, params, self._session, stream)


class EpiDataClassic(AEpiDataRequest[EpiDataResponse]):
    """
    epidata fetcher in classic format
    """

    def _run(
        self, endpoint: str, params: Mapping[str, Union[None, EpiRangeLike, Iterable[EpiRangeLike]]]
    ) -> EpiDataResponse:
        try:
            response = self._call(endpoint, params)
            return cast(EpiDataResponse, response.json())
        except Exception as e:  # pylint: disable=broad-except
            return {"result": 0, "message": f"error: {e}", "epidata": []}


class EpiDataJSON(AEpiDataRequest[List[Dict]]):
    """
    epidata fetcher in classic format
    """

    def _run(
        self, endpoint: str, params: Mapping[str, Union[None, EpiRangeLike, Iterable[EpiRangeLike]]]
    ) -> List[Dict]:
        response = self._call(endpoint, params, EpiDataFormatType.json)
        response.raise_for_status()
        return cast(List[Dict], response.json())


class EpiDataCSV(AEpiDataRequest[str]):
    """
    epidata fetcher in CSV text format
    """

    def _run(self, endpoint: str, params: Mapping[str, Union[None, EpiRangeLike, Iterable[EpiRangeLike]]]) -> str:
        response = self._call(endpoint, params, EpiDataFormatType.csv)
        response.raise_for_status()
        return response.text


class EpiDataDataFrame(AEpiDataRequest[DataFrame]):
    """
    epidata fetcher in CSV text format
    """

    def _run(self, endpoint: str, params: Mapping[str, Union[None, EpiRangeLike, Iterable[EpiRangeLike]]]) -> DataFrame:
        response = self._call(endpoint, params, EpiDataFormatType.json)
        response.raise_for_status()
        out = cast(List[Dict], response.json())
        return DataFrame(out)


class EpiDataIterator(AEpiDataRequest[Generator[Dict, None, Response]]):
    """
    epidata fetcher as Iterator
    """

    def _run(
        self, endpoint: str, params: Mapping[str, Union[None, EpiRangeLike, Iterable[EpiRangeLike]]]
    ) -> Generator[Dict, None, Response]:
        response = self._call(endpoint, params, EpiDataFormatType.jsonl, stream=True)
        response.raise_for_status()
        for line in response.iter_lines():
            yield loads(line)
        return response
