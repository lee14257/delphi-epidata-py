from typing import Iterable, Optional, Union
from .model import EpiDataCall, EpiRangeParam, InvalidArgumentException, StringParam, IntParam


def fluview(
    regions: StringParam,
    epiweeks: EpiRangeParam,
    issues: Optional[EpiRangeParam] = None,
    lag: Optional[int] = None,
    auth: Optional[str] = None,
) -> EpiDataCall:
    if regions is None or epiweeks is None:
        raise InvalidArgumentException("`regions` and `epiweeks` are both required")
    if issues is not None and lag is not None:
        raise InvalidArgumentException("`issues` and `lag` are mutually exclusive")
    return EpiDataCall("fluview", dict(regions=regions, epiweeks=epiweeks, issues=issues, lag=lag, auth=auth))


def fluview_meta() -> EpiDataCall:
    return EpiDataCall("fluview_meta", {})


def fluview_clinical(
    regions: StringParam, epiweeks: EpiRangeParam, issues: Optional[EpiRangeParam] = None, lag: Optional[int] = None
) -> EpiDataCall:
    """Fetch FluView clinical data."""

    if regions is None or epiweeks is None:
        raise InvalidArgumentException("`regions` and `epiweeks` are both required")
    if issues is not None and lag is not None:
        raise InvalidArgumentException("`issues` and `lag` are mutually exclusive")
    return EpiDataCall("fluview_clinical", dict(regions=regions, epiweeks=epiweeks, issues=issues, lag=lag))


def flusurv(
    locations: StringParam, epiweeks: EpiRangeParam, issues: Optional[EpiRangeParam] = None, lag: Optional[int] = None
) -> EpiDataCall:
    """Fetch FluSurv data."""

    if locations is None or epiweeks is None:
        raise InvalidArgumentException("`locations` and `epiweeks` are both required")
    if issues is not None and lag is not None:
        raise InvalidArgumentException("`issues` and `lag` are mutually exclusive")
    return EpiDataCall("flusurv", dict(locations=locations, epiweeks=epiweeks, issues=issues, lag=lag))


def paho_dengue(
    regions: StringParam, epiweeks: EpiRangeParam, issues: Optional[EpiRangeParam] = None, lag: Optional[int] = None
) -> EpiDataCall:
    """Fetch PAHO Dengue data."""

    if regions is None or epiweeks is None:
        raise InvalidArgumentException("`regions` and `epiweeks` are both required")
    if issues is not None and lag is not None:
        raise InvalidArgumentException("`issues` and `lag` are mutually exclusive")
    return EpiDataCall("paho_dengue", dict(regions=regions, epiweeks=epiweeks, issues=issues, lag=lag))


def ecdc_ili(
    regions: StringParam, epiweeks: EpiRangeParam, issues: Optional[EpiRangeParam] = None, lag: Optional[int] = None
) -> EpiDataCall:
    """Fetch ECDC ILI data."""
    if regions is None or epiweeks is None:
        raise InvalidArgumentException("`regions` and `epiweeks` are both required")
    if issues is not None and lag is not None:
        raise InvalidArgumentException("`issues` and `lag` are mutually exclusive")
    return EpiDataCall("ecdc_ili", dict(regions=regions, epiweeks=epiweeks, issues=issues, lag=lag))


def kcdc_ili(
    regions: StringParam, epiweeks: EpiRangeParam, issues: Optional[EpiRangeParam] = None, lag: Optional[int] = None
) -> EpiDataCall:
    """Fetch KCDC ILI data."""
    if regions is None or epiweeks is None:
        raise InvalidArgumentException("`regions` and `epiweeks` are both required")
    if issues is not None and lag is not None:
        raise InvalidArgumentException("`issues` and `lag` are mutually exclusive")
    return EpiDataCall("kcdc_ili", dict(regions=regions, epiweeks=epiweeks, issues=issues, lag=lag))


def gft(locations: StringParam, epiweeks: EpiRangeParam) -> EpiDataCall:
    """Fetch Google Flu Trends data."""
    if locations is None or epiweeks is None:
        raise InvalidArgumentException("`locations` and `epiweeks` are both required")
    return EpiDataCall("gft", dict(locations=locations, epiweeks=epiweeks))


def ght(auth: str, locations: StringParam, epiweeks: EpiRangeParam, query: str) -> EpiDataCall:
    """Fetch Google Health Trends data."""
    if auth is None or locations is None or epiweeks is None or query is None:
        raise InvalidArgumentException("`auth`, `locations`, `epiweeks`, and `query` are all required")
    return EpiDataCall("ght", dict(auth=auth, locations=locations, epiweeks=epiweeks, query=query))


def twitter(
    auth: str, locations: StringParam, dates: Optional[EpiRangeParam] = None, epiweeks: Optional[EpiRangeParam] = None
) -> EpiDataCall:
    """Fetch HealthTweets data."""

    if auth is None or locations is None:
        raise InvalidArgumentException("`auth` and `locations` are both required")
    if not (dates is None) ^ (epiweeks is None):
        raise InvalidArgumentException("exactly one of `dates` and `epiweeks` is required")
    return EpiDataCall("twitter", dict(auth=auth, locations=locations, dates=dates, epiweeks=epiweeks))


def wiki(
    articles: StringParam,
    dates: Optional[EpiRangeParam] = None,
    epiweeks: Optional[EpiRangeParam] = None,
    hours: Optional[IntParam] = None,
    language: str = "en",
) -> EpiDataCall:
    """Fetch Wikipedia access data."""

    if articles is None:
        raise InvalidArgumentException("`articles` is required")
    if not (dates is None) ^ (epiweeks is None):
        raise InvalidArgumentException("exactly one of `dates` and `epiweeks` is required")
    return EpiDataCall("wiki", dict(articles=articles, dates=dates, epiweeks=epiweeks, hours=hours, language=language))


def cdc(auth: str, epiweeks: EpiRangeParam, locations: StringParam) -> EpiDataCall:
    """Fetch CDC page hits."""

    if auth is None or epiweeks is None or locations is None:
        raise InvalidArgumentException("`auth`, `epiweeks`, and `locations` are all required")

    return EpiDataCall("cdc", dict(auth=auth, epiweeks=epiweeks, locations=locations))


def quidel(auth: str, epiweeks: EpiRangeParam, locations: StringParam) -> EpiDataCall:
    """Fetch Quidel data."""

    if auth is None or epiweeks is None or locations is None:
        raise InvalidArgumentException("`auth`, `epiweeks`, and `locations` are all required")

    return EpiDataCall("quidel", dict(auth=auth, epiweeks=epiweeks, locations=locations))


def norostat(auth: str, location: str, epiweeks: EpiRangeParam) -> EpiDataCall:
    """Fetch NoroSTAT data (point data, no min/max)."""

    if auth is None or location is None or epiweeks is None:
        raise InvalidArgumentException("`auth`, `location`, and `epiweeks` are all required")
    return EpiDataCall("norostat", dict(auth=auth, epiweeks=epiweeks, location=location))


def meta_norostat(auth: str) -> EpiDataCall:
    """Fetch NoroSTAT metadata."""

    if auth is None:
        raise InvalidArgumentException("`auth` is required")
    return EpiDataCall("meta_norostat", dict(auth=auth))


def afhsb(auth: str, locations: StringParam, epiweeks: EpiRangeParam, flu_types: StringParam) -> EpiDataCall:
    """Fetch AFHSB data (point data, no min/max)."""

    if auth is None or locations is None or epiweeks is None or flu_types is None:
        raise InvalidArgumentException("`auth`, `locations`, `epiweeks` and `flu_types` are all required")

    loc_exception = (
        "Location parameter  `{}` is invalid. Valid `location` parameters are: "
        "`hhs[1-10]`, `cen[1-9]`, 2-letter state code or 3-letter country code."
    )
    for location in locations:
        location = location.lower()
        if location.startswith("hhs") or location.startswith("cen"):
            prefix, postfix = location[:3], location[3:]
            if postfix.isnumeric():
                region_num = int(postfix)
                if region_num < 1 or region_num > 10 or (region_num == 10 and prefix == "cen"):
                    raise InvalidArgumentException(loc_exception.format(location))
            else:
                raise InvalidArgumentException(loc_exception.format(location))
        elif len(location) < 2 or len(location) > 3:
            raise InvalidArgumentException(loc_exception.format(location))

    flu_exception = (
        "Flu-type parameters `{}` is invalid. Valid flu-type parameters are: "
        "`flu1`, `flu2`, `flu3`, `ili`, `flu2-flu1`, `flu3-flu2`, `ili-flu3`."
    )
    valid_flu_types = ["flu1", "flu2", "flu3", "ili", "flu2-flu1", "flu3-flu2", "ili-flu3"]
    for flu_type in flu_types:
        if not flu_type in valid_flu_types:
            raise InvalidArgumentException(flu_exception.format(flu_type))

    return EpiDataCall("afhsb", dict(auth=auth, locations=locations, epiweeks=epiweeks, flu_types=flu_types))


def meta_afhsb(auth: str) -> EpiDataCall:
    """Fetch AFHSB metadata."""

    if auth is None:
        raise InvalidArgumentException("`auth` is required")

    return EpiDataCall("meta_afhsb", dict(auth=auth))


def nidss_flu(
    regions: StringParam, epiweeks: EpiRangeParam, issues: Optional[EpiRangeParam] = None, lag: Optional[int] = None
) -> EpiDataCall:
    """Fetch NIDSS flu data."""

    if regions is None or epiweeks is None:
        raise InvalidArgumentException("`regions` and `epiweeks` are both required")
    if issues is not None and lag is not None:
        raise InvalidArgumentException("`issues` and `lag` are mutually exclusive")

    return EpiDataCall("nidss_flu", dict(regions=regions, epiweeks=epiweeks, issues=issues, lag=lag))


def nidss_dengue(locations: StringParam, epiweeks: EpiRangeParam) -> EpiDataCall:
    """Fetch NIDSS dengue data."""

    if locations is None or epiweeks is None:
        raise InvalidArgumentException("`locations` and `epiweeks` are both required")

    return EpiDataCall("nidss_dengue", dict(locations=locations, epiweeks=epiweeks))


def delphi(system: str, epiweek: Union[int, str]) -> EpiDataCall:
    """Fetch Delphi's forecast."""

    if system is None or epiweek is None:
        raise InvalidArgumentException("`system` and `epiweek` are both required")
    return EpiDataCall("delphi", dict(system=system, epiweek=epiweek))


def sensors(auth: str, names: StringParam, locations: StringParam, epiweeks: EpiRangeParam) -> EpiDataCall:
    """Fetch Delphi's digital surveillance sensors."""

    if auth is None or names is None or locations is None or epiweeks is None:
        raise InvalidArgumentException("`auth`, `names`, `locations`, and `epiweeks` are all required")
    return EpiDataCall("sensors", dict(auth=auth, names=names, locations=locations, epiweeks=epiweeks))


def dengue_sensors(auth: str, names: StringParam, locations: StringParam, epiweeks: EpiRangeParam) -> EpiDataCall:
    """Fetch Delphi's digital surveillance sensors."""

    if auth is None or names is None or locations is None or epiweeks is None:
        raise InvalidArgumentException("`auth`, `names`, `locations`, and `epiweeks` are all required")

    return EpiDataCall("dengue_sensors", dict(auth=auth, names=names, locations=locations, epiweeks=epiweeks))


def nowcast(locations: StringParam, epiweeks: EpiRangeParam) -> EpiDataCall:
    """Fetch Delphi's wILI nowcast."""

    if locations is None or epiweeks is None:
        raise InvalidArgumentException("`locations` and `epiweeks` are both required")

    return EpiDataCall("nowcast", dict(locations=locations, epiweeks=epiweeks))


def dengue_nowcast(locations: StringParam, epiweeks: EpiRangeParam) -> EpiDataCall:
    """Fetch Delphi's dengue nowcast."""

    if locations is None or epiweeks is None:
        raise InvalidArgumentException("`locations` and `epiweeks` are both required")
    return EpiDataCall("dengue_nowcast", dict(locations=locations, epiweeks=epiweeks))


def meta() -> EpiDataCall:
    """Fetch API metadata."""
    return EpiDataCall("meta", {})


def covidcast(
    data_source: str,
    signals: StringParam,
    time_type: str,
    geo_type: str,
    time_values: EpiRangeParam,
    geo_value: Union[int, str, Iterable[Union[int, str]]],
    as_of: Union[None, str, int] = None,
    issues: Optional[EpiRangeParam] = None,
    lag: Optional[int] = None,
) -> EpiDataCall:
    """Fetch Delphi's COVID-19 Surveillance Streams"""
    if any((v is None for v in (data_source, signals, time_type, geo_type, time_values, geo_value))):
        raise InvalidArgumentException(
            "`data_source`, `signals`, `time_type`, `geo_type`, `time_values`, and `geo_value` are all required"
        )
    if issues is not None and lag is not None:
        raise InvalidArgumentException("`issues` and `lag` are mutually exclusive")

    params = dict(
        data_source=data_source,
        signals=signals,
        time_type=time_type,
        geo_type=geo_type,
        time_values=time_values,
        as_of=as_of,
        issues=issues,
        lag=lag,
    )
    if isinstance(geo_value, (list, tuple)):
        params["geo_values"] = ",".join(geo_value)
    else:
        params["geo_value"] = geo_value

    return EpiDataCall("covidcast", params)


def covidcast_meta() -> EpiDataCall:
    """Fetch Delphi's COVID-19 Surveillance Streams metadata"""
    return EpiDataCall("covidcast_meta", {})


def covid_hosp(
    states: StringParam,
    dates: EpiRangeParam,
    issues: Optional[EpiRangeParam] = None,
    as_of: Union[None, int, str] = None,
) -> EpiDataCall:
    """Fetch COVID hospitalization data."""

    if states is None or dates is None:
        raise InvalidArgumentException("`states` and `dates` are both required")
    return EpiDataCall("covid_hosp", dict(states=states, dates=dates, issues=issues, as_of=as_of))


def covid_hosp_facility(
    hospital_pks: StringParam, collection_weeks: StringParam, publication_dates: Optional[EpiRangeParam] = None
) -> EpiDataCall:
    """Fetch COVID hospitalization data for specific facilities."""

    if hospital_pks is None or collection_weeks is None:
        raise InvalidArgumentException("`hospital_pks` and `collection_weeks` are both required")

    return EpiDataCall(
        "covid_hosp_facility",
        dict(hospital_pks=hospital_pks, collection_weeks=collection_weeks, publication_dates=publication_dates),
    )


def covid_hosp_facility_lookup(
    state: Optional[str] = None,
    ccn: Optional[str] = None,
    city: Optional[str] = None,
    zip: Optional[str] = None,  # pylint: disable=redefined-builtin
    fips_code: Optional[str] = None,
) -> EpiDataCall:
    """Lookup COVID hospitalization facility identifiers."""

    if all((v is None for v in (state, ccn, city, zip, fips_code))):
        raise InvalidArgumentException("one of `state`, `ccn`, `city`, `zip`, or `fips_code` is required")

    return EpiDataCall(
        "covid_hosp_facility_lookup",
        dict(state=state, ccn=ccn, city=city, zip=zip, fips_code=fips_code),
    )


def covidcast_nowcast(
    data_source: str,
    signals: StringParam,
    sensor_names: StringParam,
    time_type: str,
    geo_type: str,
    time_values: EpiRangeParam,
    geo_value: str,
    as_of: Union[None, int, str] = None,
    issues: Optional[EpiRangeParam] = None,
    lag: Optional[int] = None,
) -> EpiDataCall:
    """Fetch Delphi's COVID-19 Nowcast sensors"""

    if any((v is None for v in (data_source, signals, time_type, geo_type, time_values, geo_value, sensor_names))):
        raise InvalidArgumentException(
            "`data_source`, `signals`, `sensor_names`, `time_type`, `geo_type`, `time_values`, and `geo_value`"
            + " are all required"
        )
    if issues is not None and lag is not None:
        raise InvalidArgumentException("`issues` and `lag` are mutually exclusive")

    params = dict(
        data_source=data_source,
        signals=signals,
        sensor_names=sensor_names,
        time_type=time_type,
        geo_type=geo_type,
        time_values=time_values,
        as_of=as_of,
        issues=issues,
        lag=lag,
    )
    if isinstance(geo_value, (list, tuple)):
        params["geo_values"] = ",".join(geo_value)
    else:
        params["geo_value"] = geo_value

    return EpiDataCall("covidcast_nowcast", params)
