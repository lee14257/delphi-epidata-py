from typing import Dict, List, Tuple, cast
import asyncio
from aiohttp import TCPConnector, ClientSession

from .model import EpiDataResponse, EpidataCall
from ._constants import BASE_URL, HTTP_HEADERS


async def _async_get(base_url: str, call: EpidataCall, session: ClientSession) -> Tuple[Dict, EpidataCall]:
    """Helper function to make Epidata GET requests."""
    async with session.get(base_url + call.endpoint, params=call.formatted_params) as response:
        response.raise_for_status()
    return await response.json(), call


class AsyncAPICaller:
    """
    async version for multiple data
    """

    base_url: str
    _queue: List[EpidataCall]

    def __init__(self, base_url: str = BASE_URL) -> None:
        self.base_url = base_url
        self._queue = []

    def push(self, call: EpidataCall) -> None:
        self._queue.append(call)

    def __call__(self, batch_size: int = 50) -> List[Tuple[EpiDataResponse, EpidataCall]]:
        """Make asynchronous Epidata calls for a list of parameters."""
        q = list(self._queue)
        self._queue.clear()

        async def async_make_calls() -> List[Tuple[EpiDataResponse, EpidataCall]]:
            """Helper function to asynchronously make and aggregate Epidata GET requests."""
            tasks: List[asyncio.Future] = []
            connector = TCPConnector(limit=batch_size)
            async with ClientSession(connector=connector, headers=HTTP_HEADERS) as session:
                for call in q:
                    task = asyncio.ensure_future(_async_get(self.base_url, call, session))
                    tasks.append(task)
            responses = await asyncio.gather(*tasks)
            return cast(List[Tuple[EpiDataResponse, EpidataCall]], list(responses))

        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(async_make_calls())
        return loop.run_until_complete(future)
