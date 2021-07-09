from datetime import date
from typing import Final, Generator, cast, Iterable, Mapping, Optional, Union, List, Dict
from json import loads

from requests import Response, Session
from tenacity import retry, stop_after_attempt
from pandas import DataFrame

from ._model import EpiRangeLike, AEpiDataCall, EpiDataFormatType, EpiDataResponse, EpiRange
from ._endpoints import AEpiDataEndpoints
from ._constants import HTTP_HEADERS, BASE_URL


@retry(reraise=True, stop=stop_after_attempt(2))
def _request_with_retry(
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


class EpiDataCall(AEpiDataCall):
    """
    epidata call representation
    """

    _session: Final[Optional[Session]]

    def __init__(
        self,
        base_url: str,
        session: Optional[Session],
        endpoint: str,
        params: Mapping[str, Union[None, EpiRangeLike, Iterable[EpiRangeLike]]],
    ) -> None:
        super().__init__(base_url, endpoint, params)
        self._session = session

    def with_base_url(self, base_url: str) -> "EpiDataCall":
        return EpiDataCall(base_url, self._session, self._endpoint, self._params)

    def with_session(self, session: Session) -> "EpiDataCall":
        return EpiDataCall(self._base_url, session, self._endpoint, self._params)

    def _call(
        self,
        format_type: Optional[EpiDataFormatType] = None,
        fields: Optional[Iterable[str]] = None,
        stream: bool = False,
    ) -> Response:
        url, params = self.request_arguments(format_type, fields)
        return _request_with_retry(url, params, self._session, stream)

    def classic(self, fields: Optional[Iterable[str]] = None) -> EpiDataResponse:
        """Request and parse epidata in CLASSIC message format."""
        try:
            response = self._call(None, fields)
            return cast(EpiDataResponse, response.json())
        except Exception as e:  # pylint: disable=broad-except
            return {"result": 0, "message": f"error: {e}", "epidata": []}

    def __call__(self, fields: Optional[Iterable[str]] = None) -> EpiDataResponse:
        """Request and parse epidata in CLASSIC message format."""
        return self.classic(fields)

    def json(self, fields: Optional[Iterable[str]] = None) -> List[Dict[str, Union[str, int, float, date]]]:
        """Request and parse epidata in JSON format"""
        response = self._call(EpiDataFormatType.json, fields)
        response.raise_for_status()
        return cast(List[Dict[str, Union[str, int, float, date]]], response.json())

    def df(self, fields: Optional[Iterable[str]] = None) -> DataFrame:
        """Request and parse epidata as a pandas data frame"""
        r = self.json(fields)
        return DataFrame(r)

    def csv(self, fields: Optional[Iterable[str]] = None) -> str:
        """Request and parse epidata in CSV format"""
        response = self._call(EpiDataFormatType.csv, fields)
        response.raise_for_status()
        return response.text

    def iter(
        self, fields: Optional[Iterable[str]] = None
    ) -> Generator[Dict[str, Union[str, int, float, date]], None, Response]:
        """Request and streams epidata rows"""
        response = self._call(EpiDataFormatType.jsonl, fields, stream=True)
        response.raise_for_status()
        for line in response.iter_lines():
            yield loads(line)
        return response

    def __iter__(self) -> Generator[Dict[str, Union[str, int, float, date]], None, Response]:
        return self.iter()


class EpiDataContext(AEpiDataEndpoints[EpiDataCall]):
    """
    sync epidata call class
    """

    _base_url: Final[str]
    _session: Final[Optional[Session]]

    def __init__(self, base_url: str = BASE_URL, session: Optional[Session] = None) -> None:
        super().__init__()
        self._base_url = base_url
        self._session = session

    def with_base_url(self, base_url: str) -> "EpiDataContext":
        return EpiDataContext(base_url, self._session)

    def with_session(self, session: Session) -> "EpiDataContext":
        return EpiDataContext(self._base_url, session)

    def _create_call(
        self,
        endpoint: str,
        params: Mapping[str, Union[None, EpiRangeLike, Iterable[EpiRangeLike]]],
    ) -> EpiDataCall:
        return EpiDataCall(self._base_url, self._session, endpoint, params)


Epidata = EpiDataContext()


__all__ = ["Epidata", "EpiDataCall", "EpiDataContext", "EpiRange"]
