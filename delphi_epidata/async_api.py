from typing import Dict, List, Mapping, Tuple, Union
import asyncio
from aiohttp import TCPConnector, ClientSession

from ._constants import BASE_URL, HTTP_HEADERS


async def _async_get(
    url: str, params: Mapping[str, Union[str, int]], session: ClientSession
) -> Tuple[Dict, str, Mapping[str, Union[str, int]]]:
    """Helper function to make Epidata GET requests."""
    async with session.get(url, params=params) as response:
        response.raise_for_status()
    return await response.json(), url, params


class AsyncAPICaller:
    """
    async version that queue
    """

    base_url: str
    _queue: List[Tuple[str, Mapping[str, Union[str, int]]]]

    def __init__(self, base_url: str = BASE_URL) -> None:
        self.base_url = base_url
        self._queue = []

    def push(self, endpoint: str, params: Mapping[str, Union[str, int]]) -> None:
        self._queue.append((endpoint, params))

    def run_queue(self, batch_size: int = 50) -> List[Tuple[Dict, str, Mapping[str, Union[str, int]]]]:
        """Make asynchronous Epidata calls for a list of parameters."""
        q = list(self._queue)
        self._queue.clear()

        async def async_make_calls() -> List[Tuple[Dict, str, Mapping[str, Union[str, int]]]]:
            """Helper function to asynchronously make and aggregate Epidata GET requests."""
            tasks: List[asyncio.Future[Tuple[Dict, str, Mapping[str, Union[str, int]]]]] = []
            connector = TCPConnector(limit=batch_size)
            async with ClientSession(connector=connector, headers=HTTP_HEADERS) as session:
                for endpoint, params in q:
                    url = self.base_url + endpoint
                    task = asyncio.ensure_future(_async_get(url, params, session))
                    tasks.append(task)
            responses = await asyncio.gather(*tasks)
            return list(responses)

        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(async_make_calls())
        return loop.run_until_complete(future)
