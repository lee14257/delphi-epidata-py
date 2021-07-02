from enum import Enum
from typing import Iterable, Mapping, Optional, Union

from aiohttp import ClientSession, ClientResponse
from requests import Response, Session
from tenacity import retry, stop_after_attempt

from .model import EpiRangeLike
from ._constants import HTTP_HEADERS


def format_item(value: EpiRangeLike) -> str:
    """Cast values and/or range to a string."""
    if isinstance(value, dict) and "from" in value and "to" in value:
        return f"{value['from']}-{value['to']}"
    if isinstance(value, Enum):
        return str(value.value)
    return str(value)


def format_list(values: Union[EpiRangeLike, Iterable[EpiRangeLike]]) -> str:
    """Turn a list/tuple of values/ranges into a comma-separated string."""
    list_values = values if isinstance(values, (list, tuple, set)) else [values]
    return ",".join([format_item(value) for value in list_values])


@retry(reraise=True, stop=stop_after_attempt(2))  # type: ignore
def request_with_retry(
    url: str, params: Mapping[str, str], session: Optional[Session] = None, stream: bool = False
) -> Response:
    """Make request with a retry if an exception is thrown."""

    def call_impl(s: Session) -> Response:
        res = s.get(url, params=params, headers=HTTP_HEADERS, stream=stream)
        if res.status_code == 414:
            return s.post(url, params=params, headers=HTTP_HEADERS, stream=stream)
        return res

    if session:
        return call_impl(session)

    with Session() as s:
        return call_impl(s)


async def async_request(url: str, params: Mapping[str, str], session: Optional[ClientSession] = None) -> ClientResponse:
    async def call_impl(s: ClientSession) -> ClientResponse:
        res = await s.get(url, params=params, headers=HTTP_HEADERS)
        if res.status == 414:
            return await s.post(url, params=params, headers=HTTP_HEADERS)
        return res

    if session:
        return await call_impl(session)

    async with ClientSession() as s:
        return await call_impl(s)
