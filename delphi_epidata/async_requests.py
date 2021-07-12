from datetime import date
from typing import (
    AsyncGenerator,
    Callable,
    Coroutine,
    Dict,
    Final,
    Iterable,
    List,
    Mapping,
    Optional,
    Sequence,
    Union,
    cast,
)
from json import loads

from asyncio import get_event_loop, gather
from aiohttp import TCPConnector, ClientSession, ClientResponse
from pandas import DataFrame

from ._model import EpiRangeLike, AEpiDataCall, EpiDataFormatType, EpiDataResponse, EpiRange, EpidataFieldInfo
from ._endpoints import AEpiDataEndpoints
from ._constants import HTTP_HEADERS, BASE_URL


async def _async_request(
    url: str, params: Mapping[str, str], session: Optional[ClientSession] = None
) -> ClientResponse:
    async def call_impl(s: ClientSession) -> ClientResponse:
        res = await s.get(url, params=params, headers=HTTP_HEADERS)
        if res.status == 414:
            return await s.post(url, params=params, headers=HTTP_HEADERS)
        return res

    if session:
        return await call_impl(session)

    async with ClientSession() as s:
        return await call_impl(s)


class EpiDataAsyncCall(AEpiDataCall):
    """
    async version of an epidata call
    """

    _session: Final[Optional[ClientSession]]

    def __init__(
        self,
        base_url: str,
        session: Optional[ClientSession],
        endpoint: str,
        params: Mapping[str, Union[None, EpiRangeLike, Iterable[EpiRangeLike]]],
        meta: Optional[Sequence[EpidataFieldInfo]] = None,
    ) -> None:
        super().__init__(base_url, endpoint, params, meta)
        self._session = session

    def with_base_url(self, base_url: str) -> "EpiDataAsyncCall":
        return EpiDataAsyncCall(base_url, self._session, self._endpoint, self._params)

    def with_session(self, session: ClientSession) -> "EpiDataAsyncCall":
        return EpiDataAsyncCall(self._base_url, session, self._endpoint, self._params)

    async def _call(
        self,
        format_type: Optional[EpiDataFormatType] = None,
        fields: Optional[Iterable[str]] = None,
    ) -> ClientResponse:
        url, params = self.request_arguments(format_type, fields)
        return await _async_request(url, params, self._session)

    async def classic(self, fields: Optional[Iterable[str]] = None) -> EpiDataResponse:
        """Request and parse epidata in CLASSIC message format."""
        try:
            response = await self._call(None, fields)
            r = cast(EpiDataResponse, await response.json())
            epidata = r.get("epidata")
            if epidata and isinstance(epidata, list) and len(epidata) > 0 and isinstance(epidata[0], dict):
                r["epidata"] = [self._parse_row(row) for row in epidata]
            return r
        except Exception as e:  # pylint: disable=broad-except
            return {"result": 0, "message": f"error: {e}", "epidata": []}

    async def __call__(self, fields: Optional[Iterable[str]] = None) -> EpiDataResponse:
        """Request and parse epidata in CLASSIC message format."""
        return await self.classic(fields)

    async def json(
        self, fields: Optional[Iterable[str]] = None
    ) -> List[Mapping[str, Union[str, int, float, date, None]]]:
        """Request and parse epidata in JSON format"""
        response = await self._call(EpiDataFormatType.json, fields)
        response.raise_for_status()
        return [
            self._parse_row(row)
            for row in cast(List[Mapping[str, Union[str, int, float, None]]], await response.json())
        ]

    async def df(self, fields: Optional[Iterable[str]] = None) -> DataFrame:
        """Request and parse epidata as a pandas data frame"""
        r = await self.json(fields)
        return self._as_df(r)

    async def csv(self, fields: Optional[Iterable[str]] = None) -> str:
        """Request and parse epidata in CSV format"""
        response = await self._call(EpiDataFormatType.csv, fields)
        response.raise_for_status()
        return await response.text()

    async def iter(
        self, fields: Optional[Iterable[str]] = None
    ) -> AsyncGenerator[Mapping[str, Union[str, int, float, date, None]], None]:
        """Request and streams epidata rows"""
        response = await self._call(EpiDataFormatType.jsonl, fields)
        response.raise_for_status()
        async for line in response.content:
            yield self._parse_row(loads(line))

    async def __(self) -> AsyncGenerator[Mapping[str, Union[str, int, float, date, None]], None]:
        return self.iter()


class EpiDataAsyncContext(AEpiDataEndpoints[EpiDataAsyncCall]):
    """
    sync epidata call class
    """

    _base_url: Final[str]
    _session: Final[Optional[ClientSession]]

    def __init__(self, base_url: str = BASE_URL, session: Optional[ClientSession] = None) -> None:
        super().__init__()
        self._base_url = base_url
        self._session = session

    def with_base_url(self, base_url: str) -> "EpiDataAsyncContext":
        return EpiDataAsyncContext(base_url, self._session)

    def with_session(self, session: ClientSession) -> "EpiDataAsyncContext":
        return EpiDataAsyncContext(self._base_url, session)

    def _create_call(
        self,
        endpoint: str,
        params: Mapping[str, Union[None, EpiRangeLike, Iterable[EpiRangeLike]]],
        meta: Optional[Sequence[EpidataFieldInfo]] = None,
    ) -> EpiDataAsyncCall:
        return EpiDataAsyncCall(self._base_url, self._session, endpoint, params, meta)

    @staticmethod
    def all(
        calls: Iterable[EpiDataAsyncCall],
        call_api: Callable[[EpiDataAsyncCall, ClientSession], Coroutine],
        batch_size: int = 50,
    ) -> List:
        loop = get_event_loop()

        async def impl() -> List:
            tasks: List[Coroutine] = []
            connector = TCPConnector(limit=batch_size)
            async with ClientSession(connector=connector) as session:
                for call in calls:
                    co_routine = call_api(call, session)
                    tasks.append(co_routine)
                return list(await gather(*tasks))

        future = impl()
        return loop.run_until_complete(future)

    def all_classic(
        self,
        calls: Iterable[EpiDataAsyncCall],
        fields: Optional[Iterable[str]] = None,
        batch_size: int = 50,
    ) -> List[EpiDataResponse]:
        """
        runs the given calls in a batch asynchronously and return their responses
        """

        def call_api(call: EpiDataAsyncCall, session: ClientSession) -> Coroutine:
            return call.with_session(session).classic(fields)

        return self.all(calls, call_api, batch_size)

    def all_json(
        self,
        calls: Iterable[EpiDataAsyncCall],
        fields: Optional[Iterable[str]] = None,
        batch_size: int = 50,
    ) -> List[List[Dict]]:
        """
        runs the given calls in a batch asynchronously and return their responses
        """

        def call_api(call: EpiDataAsyncCall, session: ClientSession) -> Coroutine:
            return call.with_session(session).json(fields)

        return self.all(calls, call_api, batch_size)

    def all_csv(
        self,
        calls: Iterable[EpiDataAsyncCall],
        fields: Optional[Iterable[str]] = None,
        batch_size: int = 50,
    ) -> List[str]:
        """
        runs the given calls in a batch asynchronously and return their responses
        """

        def call_api(call: EpiDataAsyncCall, session: ClientSession) -> Coroutine:
            return call.with_session(session).csv(fields)

        return self.all(calls, call_api, batch_size)


Epidata = EpiDataAsyncContext()


__all__ = ["Epidata", "EpiDataAsyncCall", "EpiDataAsyncContext", "EpiRange"]
