from typing import AsyncGenerator, Callable, Coroutine, Dict, Iterable, List, Mapping, Optional, Union, cast
from json import loads

from asyncio import get_event_loop, gather
from aiohttp import TCPConnector, ClientSession, ClientResponse
from pandas import DataFrame

from ._model import EpiRangeLike, AEpiDataCall, EpiDataFormatType, EpiDataResponse
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

    def __init__(
        self,
        base_url: str,
        session: Optional[ClientSession],
        endpoint: str,
        params: Mapping[str, Union[None, EpiRangeLike, Iterable[EpiRangeLike]]],
    ) -> None:
        super().__init__(base_url, endpoint, params)
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
            return cast(EpiDataResponse, await response.json())
        except Exception as e:  # pylint: disable=broad-except
            return {"result": 0, "message": f"error: {e}", "epidata": []}

    async def __call__(self, fields: Optional[Iterable[str]] = None) -> EpiDataResponse:
        """Request and parse epidata in CLASSIC message format."""
        return await self.classic(fields)

    async def json(self, fields: Optional[Iterable[str]] = None) -> List[Dict]:
        """Request and parse epidata in JSON format"""
        response = await self._call(EpiDataFormatType.json, fields)
        response.raise_for_status()
        return cast(List[Dict], await response.json())

    async def df(self, fields: Optional[Iterable[str]] = None) -> DataFrame:
        """Request and parse epidata as a pandas data frame"""
        r = await self.json(fields)
        return DataFrame(r)

    async def csv(self, fields: Optional[Iterable[str]] = None) -> str:
        """Request and parse epidata in CSV format"""
        response = await self._call(EpiDataFormatType.csv, fields)
        response.raise_for_status()
        return await response.text()

    async def iter(self, fields: Optional[Iterable[str]] = None) -> AsyncGenerator[Dict, None]:
        """Request and streams epidata rows"""
        response = await self._call(EpiDataFormatType.jsonl, fields)
        response.raise_for_status()
        async for line in response.content:
            yield loads(line)

    async def __(self) -> AsyncGenerator[Dict, None]:
        return self.iter()


class EpiDataAsyncRequest(AEpiDataEndpoints[EpiDataAsyncCall]):
    """
    sync epidata call class
    """

    def __init__(self, base_url: str = BASE_URL, session: Optional[ClientSession] = None) -> None:
        super().__init__()
        self._base_url = base_url
        self._session = session

    def with_base_url(self, base_url: str) -> "EpiDataAsyncRequest":
        return EpiDataAsyncRequest(base_url, self._session)

    def with_session(self, session: ClientSession) -> "EpiDataAsyncRequest":
        return EpiDataAsyncRequest(self._base_url, session)

    def _create_call(
        self, endpoint: str, params: Mapping[str, Union[None, EpiRangeLike, Iterable[EpiRangeLike]]]
    ) -> EpiDataAsyncCall:
        return EpiDataAsyncCall(self._base_url, self._session, endpoint, params)


def _batch_call(
    call_api: Callable[[EpiDataAsyncCall, ClientSession], Coroutine],
    calls: Iterable[EpiDataAsyncCall],
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


def batch_call(
    calls: Iterable[EpiDataAsyncCall],
    fields: Optional[Iterable[str]] = None,
    batch_size: int = 50,
) -> List[EpiDataResponse]:
    """
    runs the given calls in a batch asynchronously and return their responses
    """

    def call_api(call: EpiDataAsyncCall, session: ClientSession) -> Coroutine:
        return call.with_session(session).classic(fields)

    return _batch_call(call_api, calls, batch_size)


def batch_json(
    calls: Iterable[EpiDataAsyncCall],
    fields: Optional[Iterable[str]] = None,
    batch_size: int = 50,
) -> List[List[Dict]]:
    """
    runs the given calls in a batch asynchronously and return their responses
    """

    def call_api(call: EpiDataAsyncCall, session: ClientSession) -> Coroutine:
        return call.with_session(session).json(fields)

    return _batch_call(call_api, calls, batch_size)


def batch_csv(
    calls: Iterable[EpiDataAsyncCall],
    fields: Optional[Iterable[str]] = None,
    batch_size: int = 50,
) -> List[str]:
    """
    runs the given calls in a batch asynchronously and return their responses
    """

    def call_api(call: EpiDataAsyncCall, session: ClientSession) -> Coroutine:
        return call.with_session(session).csv(fields)

    return _batch_call(call_api, calls, batch_size)


Epidata = EpiDataAsyncRequest()
