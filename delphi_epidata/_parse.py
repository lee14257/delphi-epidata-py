from typing import Optional, cast

from typing import Union
from datetime import date, datetime
from epiweeks import Week


def parse_api_date(value: Union[str, int, float, None]) -> Optional[date]:
    if value is None:
        return value
    v = str(value)
    return datetime.strptime(v, "%Y%m%d").date()


def parse_api_week(value: Union[str, int, float, None]) -> Optional[date]:
    if value is None:
        return None
    return cast(date, Week.fromstring(str(value)).startdate())
