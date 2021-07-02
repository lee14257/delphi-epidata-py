from json import loads
from typing import AsyncGenerator, Callable, Coroutine, Dict, Iterable, List, Optional, cast
import asyncio
from aiohttp import TCPConnector, ClientSession, ClientResponse

from .model import EpiDataFormatType, EpiDataResponse, EpiDataCall
from ._constants import BASE_URL, HTTP_HEADERS


class AsyncAPICaller:
    """
    async version for multiple data
    """

    base_url: str

    def __init__(self, session: ClientSession, base_url: str = BASE_URL) -> None:
        self.base_url = base_url
        self.session = session

    @staticmethod
    async def create(base_url: str = BASE_URL, batch_size: int = 50) -> "AsyncAPICaller":
        connector = TCPConnector(limit=batch_size)
        async with ClientSession(connector=connector, headers=HTTP_HEADERS) as session:
            return AsyncAPICaller(session, base_url)

    async def _call(
        self,
        call: EpiDataCall,
        format_type: Optional[EpiDataFormatType] = None,
        fields: Optional[Iterable[str]] = None,
    ) -> ClientResponse:
        url, params = call(self.base_url, format_type, fields)
        async with self.session.get(url, params=params) as response:
            return response

    async def __call__(self, call: EpiDataCall, fields: Optional[Iterable[str]] = None) -> EpiDataResponse:
        """Request and parse epidata."""
        try:
            response = await self._call(call, fields=fields)
            return cast(EpiDataResponse, await response.json())
        except Exception as e:  # pylint: disable=broad-except
            return {"result": 0, "message": f"error: {e}", "epidata": []}

    async def json(self, call: EpiDataCall, fields: Optional[Iterable[str]] = None) -> List[Dict]:
        """Request and parse epidata in JSON format"""
        response = await self._call(call, EpiDataFormatType.json, fields=fields)
        response.raise_for_status()
        return cast(List[Dict], await response.json())

    async def csv(self, call: EpiDataCall, fields: Optional[Iterable[str]] = None) -> str:
        """Request and parse epidata in CSV format"""
        response = await self._call(call, EpiDataFormatType.csv, fields=fields)
        response.raise_for_status()
        return await response.text()

    async def jsonl(self, call: EpiDataCall, fields: Optional[Iterable[str]] = None) -> AsyncGenerator[Dict, None]:
        """Request and streams epidata rows"""
        url, params = call(self.base_url, EpiDataFormatType.jsonl, fields)
        async with self.session.get(url, params=params, stream=True) as response:
            response.raise_for_status()
            async for line in response.content:
                yield loads(line)

    @staticmethod
    def _batch_call(
        call_api: Callable[["AsyncAPICaller", EpiDataCall], Coroutine],
        calls: Iterable[EpiDataCall],
        batch_size: int = 50,
        base_url: str = BASE_URL,
    ) -> List:
        loop = asyncio.get_event_loop()

        async def impl() -> List:
            tasks: List[asyncio.Future] = []
            connector = TCPConnector(limit=batch_size)
            async with ClientSession(connector=connector, headers=HTTP_HEADERS) as session:
                api_caller = AsyncAPICaller(session, base_url)
                for call in calls:
                    co_routine = call_api(api_caller, call)
                    task = asyncio.ensure_future(co_routine)
                    tasks.append(task)
                return list(await asyncio.gather(*tasks))

        future = asyncio.ensure_future(impl())
        return loop.run_until_complete(future)

    @staticmethod
    def batch_call(
        calls: Iterable[EpiDataCall],
        fields: Optional[Iterable[str]] = None,
        batch_size: int = 50,
        base_url: str = BASE_URL,
    ) -> List[EpiDataResponse]:
        """
        runs the given calls in a batch asynchronously and return their responses
        """

        def call_api(caller: "AsyncAPICaller", call: EpiDataCall) -> Coroutine:
            return caller(call, fields)

        return AsyncAPICaller._batch_call(call_api, calls, batch_size, base_url)

    @staticmethod
    def batch_json(
        calls: Iterable[EpiDataCall],
        fields: Optional[Iterable[str]] = None,
        batch_size: int = 50,
        base_url: str = BASE_URL,
    ) -> List[List[Dict]]:
        """
        runs the given calls in a batch asynchronously and return their responses
        """

        def call_api(caller: "AsyncAPICaller", call: EpiDataCall) -> Coroutine:
            return caller.json(call, fields)

        return AsyncAPICaller._batch_call(call_api, calls, batch_size, base_url)

    @staticmethod
    def batch_csv(
        calls: Iterable[EpiDataCall],
        fields: Optional[Iterable[str]] = None,
        batch_size: int = 50,
        base_url: str = BASE_URL,
    ) -> List[str]:
        """
        runs the given calls in a batch asynchronously and return their responses
        """

        def call_api(caller: "AsyncAPICaller", call: EpiDataCall) -> Coroutine:
            return caller.csv(call, fields)

        return AsyncAPICaller._batch_call(call_api, calls, batch_size, base_url)
