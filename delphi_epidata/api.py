from json import loads
from typing import Dict, Generator, Iterable, List, Mapping, Optional, Union, cast
from requests import get, post, Response
from tenacity import retry, stop_after_attempt
from ._constants import HTTP_HEADERS, BASE_URL
from .model import EpiDataFormatType, EpiDataResponse, EpiDataCall


@retry(reraise=True, stop=stop_after_attempt(2))  # type: ignore
def _request_with_retry(url: str, params: Mapping[str, Union[str, int]]) -> Response:
    """Make request with a retry if an exception is thrown."""
    request = get(url, params, headers=HTTP_HEADERS)
    if request.status_code == 414:
        request = post(url, params, headers=HTTP_HEADERS)
    return request


class APICaller:
    """
    handler for calling the API
    """

    base_url: str

    def __init__(self, base_url: str = BASE_URL) -> None:
        self.base_url = base_url

    def _call(
        self, call: EpiDataCall, format_type: Optional[EpiDataFormatType] = None, fields: Optional[Iterable[str]] = None
    ) -> Response:
        url, params = call(self.base_url, format_type, fields)
        return _request_with_retry(url, params)

    def __call__(self, call: EpiDataCall, fields: Optional[Iterable[str]] = None) -> EpiDataResponse:
        """Request and parse epidata.

        We default to GET since it has better caching and logging
        capabilities, but fall back to POST if the request is too
        long and returns a 414.
        """
        try:
            response = self._call(call, fields=fields)
            return cast(EpiDataResponse, response.json())
        except Exception as e:  # pylint: disable=broad-except
            return {"result": 0, "message": f"error: {e}", "epidata": []}

    def json(self, call: EpiDataCall, fields: Optional[Iterable[str]] = None) -> List[Dict]:
        """Request and parse epidata in JSON format"""
        response = self._call(call, EpiDataFormatType.json, fields=fields)
        response.raise_for_status()
        return cast(List[Dict], response.json())

    def csv(self, call: EpiDataCall, fields: Optional[Iterable[str]] = None) -> str:
        """Request and parse epidata in CSV format"""
        response = self._call(call, EpiDataFormatType.csv, fields=fields)
        response.raise_for_status()
        return response.text

    def jsonl(self, call: EpiDataCall, fields: Optional[Iterable[str]] = None) -> Generator[Dict, None, Response]:
        """Request and streams epidata rows"""
        url, params = call(self.base_url, EpiDataFormatType.jsonl, fields)
        response = get(
            url,
            params,
            headers=HTTP_HEADERS,
            stream=True,
        )
        response.raise_for_status()
        for line in response.iter_lines():
            yield loads(line)
        return response
