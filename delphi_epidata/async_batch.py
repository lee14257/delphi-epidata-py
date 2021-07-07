from typing import Callable, Coroutine, Dict, Iterable, List, Optional
from asyncio import get_event_loop, gather
from aiohttp import TCPConnector, ClientSession

from .model import EpiDataResponse
from .epidatacall import EpiDataCall
from ._constants import BASE_URL


def _batch_call(
    call_api: Callable[[EpiDataCall, ClientSession], Coroutine],
    calls: Iterable[EpiDataCall],
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
    calls: Iterable[EpiDataCall],
    fields: Optional[Iterable[str]] = None,
    batch_size: int = 50,
    base_url: str = BASE_URL,
) -> List[EpiDataResponse]:
    """
    runs the given calls in a batch asynchronously and return their responses
    """

    def call_api(call: EpiDataCall, session: ClientSession) -> Coroutine:
        return call.async_call(fields, base_url, session)

    return _batch_call(call_api, calls, batch_size)


def batch_json(
    calls: Iterable[EpiDataCall],
    fields: Optional[Iterable[str]] = None,
    batch_size: int = 50,
    base_url: str = BASE_URL,
) -> List[List[Dict]]:
    """
    runs the given calls in a batch asynchronously and return their responses
    """

    def call_api(call: EpiDataCall, session: ClientSession) -> Coroutine:
        return call.async_json(fields, base_url, session)

    return _batch_call(call_api, calls, batch_size)


def batch_csv(
    calls: Iterable[EpiDataCall],
    fields: Optional[Iterable[str]] = None,
    batch_size: int = 50,
    base_url: str = BASE_URL,
) -> List[str]:
    """
    runs the given calls in a batch asynchronously and return their responses
    """

    def call_api(call: EpiDataCall, session: ClientSession) -> Coroutine:
        return call.async_csv(fields, base_url, session)

    return _batch_call(call_api, calls, batch_size)
