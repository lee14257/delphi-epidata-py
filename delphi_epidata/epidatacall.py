from dataclasses import dataclass
from urllib.parse import urlencode
from json import loads
from typing import (
    AsyncGenerator,
    Dict,
    Generator,
    Iterable,
    List,
    Mapping,
    Optional,
    Tuple,
    Union,
    cast,
)
from requests import Response, Session
from aiohttp import ClientSession, ClientResponse

from .model import EpiDataFormatType, EpiDataResponse, EpiRangeLike
from ._constants import BASE_URL
from ._utils import format_list, request_with_retry, async_request


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

    def _full_url(self, base_url: str) -> str:
        """ """
        return f"{base_url}{self.endpoint}/"

    def request_arguments(
        self, base_url: str, format_type: Optional[EpiDataFormatType] = None, fields: Optional[Iterable[str]] = None
    ) -> Tuple[str, Mapping[str, str]]:
        """
        format this call into a [URL, Params] tuple
        """
        all_params = dict(self.params)
        if format_type and format_type != EpiDataFormatType.classic:
            all_params["format"] = format_type
        if fields:
            all_params["fields"] = fields
        formatted_params = {k: format_list(v) for k, v in all_params.items() if v is not None}
        full_url = self._full_url(base_url)
        return full_url, formatted_params

    def request_url(
        self, base_url: str, format_type: Optional[EpiDataFormatType] = None, fields: Optional[Iterable[str]] = None
    ) -> str:
        """
        format this call into a full HTTP request url with encoded parameters
        """
        u, p = self.request_arguments(base_url, format_type, fields)
        query = urlencode(p)
        if query:
            return f"{u}?{query}"
        return u

    def _call(
        self,
        base_url: str,
        format_type: Optional[EpiDataFormatType] = None,
        fields: Optional[Iterable[str]] = None,
        session: Optional[Session] = None,
        stream: bool = False,
    ) -> Response:
        url, params = self.request_arguments(base_url, format_type, fields)
        return request_with_retry(url, params, session, stream)

    def classic(
        self, fields: Optional[Iterable[str]] = None, base_url: str = BASE_URL, session: Optional[Session] = None
    ) -> EpiDataResponse:
        """Request and parse epidata.

        We default to GET since it has better caching and logging
        capabilities, but fall back to POST if the request is too
        long and returns a 414.
        """
        try:
            response = self._call(base_url, None, fields, session)
            return cast(EpiDataResponse, response.json())
        except Exception as e:  # pylint: disable=broad-except
            return {"result": 0, "message": f"error: {e}", "epidata": []}

    def __call__(
        self, fields: Optional[Iterable[str]] = None, base_url: str = BASE_URL, session: Optional[Session] = None
    ) -> EpiDataResponse:
        return self.classic(fields, base_url, session)

    def json(
        self, fields: Optional[Iterable[str]] = None, base_url: str = BASE_URL, session: Optional[Session] = None
    ) -> List[Dict]:
        """Request and parse epidata in JSON format"""
        response = self._call(base_url, EpiDataFormatType.json, fields, session)
        response.raise_for_status()
        return cast(List[Dict], response.json())

    def csv(
        self, fields: Optional[Iterable[str]] = None, base_url: str = BASE_URL, session: Optional[Session] = None
    ) -> str:
        """Request and parse epidata in CSV format"""
        response = self._call(base_url, EpiDataFormatType.csv, fields, session)
        response.raise_for_status()
        return response.text

    def jsonl(
        self, fields: Optional[Iterable[str]] = None, base_url: str = BASE_URL, session: Optional[Session] = None
    ) -> Generator[Dict, None, Response]:
        """Request and streams epidata rows"""
        response = self._call(base_url, EpiDataFormatType.jsonl, fields, session, stream=True)
        response.raise_for_status()
        for line in response.iter_lines():
            yield loads(line)
        return response

    async def _async_call(
        self,
        base_url: str,
        format_type: Optional[EpiDataFormatType] = None,
        fields: Optional[Iterable[str]] = None,
        session: Optional[ClientSession] = None,
    ) -> ClientResponse:
        url, params = self.request_arguments(base_url, format_type, fields)
        return await async_request(url, params, session)

    async def async_classic(
        self, fields: Optional[Iterable[str]] = None, base_url: str = BASE_URL, session: Optional[ClientSession] = None
    ) -> EpiDataResponse:
        """Request and parse epidata."""
        try:
            response = await self._async_call(base_url, None, fields, session)
            return cast(EpiDataResponse, await response.json())
        except Exception as e:  # pylint: disable=broad-except
            return {"result": 0, "message": f"error: {e}", "epidata": []}

    async def async_call(
        self, fields: Optional[Iterable[str]] = None, base_url: str = BASE_URL, session: Optional[ClientSession] = None
    ) -> EpiDataResponse:
        return await self.async_classic(fields, base_url, session)

    async def async_json(
        self, fields: Optional[Iterable[str]] = None, base_url: str = BASE_URL, session: Optional[ClientSession] = None
    ) -> List[Dict]:
        """Request and parse epidata in JSON format"""
        response = await self._async_call(base_url, EpiDataFormatType.json, fields, session)
        response.raise_for_status()
        return cast(List[Dict], await response.json())

    async def async_csv(
        self, fields: Optional[Iterable[str]] = None, base_url: str = BASE_URL, session: Optional[ClientSession] = None
    ) -> str:
        """Request and parse epidata in CSV format"""
        response = await self._async_call(base_url, EpiDataFormatType.csv, fields, session)
        response.raise_for_status()
        return await response.text()

    async def async_jsonl(
        self, fields: Optional[Iterable[str]] = None, base_url: str = BASE_URL, session: Optional[ClientSession] = None
    ) -> AsyncGenerator[Dict, None]:
        """Request and streams epidata rows"""
        response = await self._async_call(base_url, EpiDataFormatType.jsonl, fields, session)
        response.raise_for_status()
        async for line in response.content:
            yield loads(line)
