from typing import Mapping, Union, cast
from requests import get, post, Response
from tenacity import retry, stop_after_attempt
from ._constants import HTTP_HEADERS, BASE_URL
from .model import EpiResponse


@retry(reraise=True, stop=stop_after_attempt(2))  # type: ignore
def _request_with_retry(url: str, params: Mapping[str, Union[str, int]]) -> Response:
    """Make request with a retry if an exception is thrown."""
    req = get(url, params, headers=HTTP_HEADERS)
    if req.status_code == 414:
        req = post(url, params, headers=HTTP_HEADERS)
    return req


class APICaller:
    """
    handler for calling the API
    """

    base_url: str

    def __init__(self, base_url: str = BASE_URL) -> None:
        self.base_url = base_url

    def __call__(self, endpoint: str, params: Mapping[str, Union[str, int]]) -> EpiResponse:
        """Request and parse epidata.

        We default to GET since it has better caching and logging
        capabilities, but fall back to POST if the request is too
        long and returns a 414.
        """
        try:
            return cast(EpiResponse, _request_with_retry(self.base_url + endpoint, params).json())
        except Exception as e:  # pylint: disable=broad-except
            return {"result": 0, "message": f"error: {e}", "epidata": []}
