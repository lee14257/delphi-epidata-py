from abc import ABC, abstractmethod
from typing import Generic, Iterable, Mapping, Optional, TypeVar, Union
from ._model import EpiRangeLike, EpiRangeParam, InvalidArgumentException, StringParam, IntParam, EpiRange

CALL_TYPE = TypeVar("CALL_TYPE")


class AEpiDataEndpoints(ABC, Generic[CALL_TYPE]):
    """
    epidata endpoint list and fetcher
    """

    @staticmethod
    def range(from_: int, to: int) -> EpiRange:
        return EpiRange(from_, to)

    @abstractmethod
    def _create_call(
        self, endpoint: str, params: Mapping[str, Union[None, EpiRangeLike, Iterable[EpiRangeLike]]]
    ) -> CALL_TYPE:
        raise NotImplementedError()

    def fluview(
        self,
        regions: StringParam,
        epiweeks: EpiRangeParam,
        issues: Optional[EpiRangeParam] = None,
        lag: Optional[int] = None,
        auth: Optional[str] = None,
    ) -> CALL_TYPE:
        if regions is None or epiweeks is None:
            raise InvalidArgumentException("`regions` and `epiweeks` are both required")
        if issues is not None and lag is not None:
            raise InvalidArgumentException("`issues` and `lag` are mutually exclusive")
        return self._create_call(
            "fluview/", dict(regions=regions, epiweeks=epiweeks, issues=issues, lag=lag, auth=auth)
        )

    def fluview_meta(self) -> CALL_TYPE:
        return self._create_call("fluview_meta", {})

    def fluview_clinical(
        self,
        regions: StringParam,
        epiweeks: EpiRangeParam,
        issues: Optional[EpiRangeParam] = None,
        lag: Optional[int] = None,
    ) -> CALL_TYPE:
        """Fetch FluView clinical data."""

        if regions is None or epiweeks is None:
            raise InvalidArgumentException("`regions` and `epiweeks` are both required")
        if issues is not None and lag is not None:
            raise InvalidArgumentException("`issues` and `lag` are mutually exclusive")
        return self._create_call("fluview_clinical/", dict(regions=regions, epiweeks=epiweeks, issues=issues, lag=lag))

    def flusurv(
        self,
        locations: StringParam,
        epiweeks: EpiRangeParam,
        issues: Optional[EpiRangeParam] = None,
        lag: Optional[int] = None,
    ) -> CALL_TYPE:
        """Fetch FluSurv data."""

        if locations is None or epiweeks is None:
            raise InvalidArgumentException("`locations` and `epiweeks` are both required")
        if issues is not None and lag is not None:
            raise InvalidArgumentException("`issues` and `lag` are mutually exclusive")
        return self._create_call("flusurv/", dict(locations=locations, epiweeks=epiweeks, issues=issues, lag=lag))

    def paho_dengue(
        self,
        regions: StringParam,
        epiweeks: EpiRangeParam,
        issues: Optional[EpiRangeParam] = None,
        lag: Optional[int] = None,
    ) -> CALL_TYPE:
        """Fetch PAHO Dengue data."""

        if regions is None or epiweeks is None:
            raise InvalidArgumentException("`regions` and `epiweeks` are both required")
        if issues is not None and lag is not None:
            raise InvalidArgumentException("`issues` and `lag` are mutually exclusive")
        return self._create_call("paho_dengue/", dict(regions=regions, epiweeks=epiweeks, issues=issues, lag=lag))

    def ecdc_ili(
        self,
        regions: StringParam,
        epiweeks: EpiRangeParam,
        issues: Optional[EpiRangeParam] = None,
        lag: Optional[int] = None,
    ) -> CALL_TYPE:
        """Fetch ECDC ILI data."""
        if regions is None or epiweeks is None:
            raise InvalidArgumentException("`regions` and `epiweeks` are both required")
        if issues is not None and lag is not None:
            raise InvalidArgumentException("`issues` and `lag` are mutually exclusive")
        return self._create_call("ecdc_ili/", dict(regions=regions, epiweeks=epiweeks, issues=issues, lag=lag))

    def kcdc_ili(
        self,
        regions: StringParam,
        epiweeks: EpiRangeParam,
        issues: Optional[EpiRangeParam] = None,
        lag: Optional[int] = None,
    ) -> CALL_TYPE:
        """Fetch KCDC ILI data."""
        if regions is None or epiweeks is None:
            raise InvalidArgumentException("`regions` and `epiweeks` are both required")
        if issues is not None and lag is not None:
            raise InvalidArgumentException("`issues` and `lag` are mutually exclusive")
        return self._create_call("kcdc_ili/", dict(regions=regions, epiweeks=epiweeks, issues=issues, lag=lag))

    def gft(self, locations: StringParam, epiweeks: EpiRangeParam) -> CALL_TYPE:
        """Fetch Google Flu Trends data."""
        if locations is None or epiweeks is None:
            raise InvalidArgumentException("`locations` and `epiweeks` are both required")
        return self._create_call("gft/", dict(locations=locations, epiweeks=epiweeks))

    def ght(self, auth: str, locations: StringParam, epiweeks: EpiRangeParam, query: str) -> CALL_TYPE:
        """Fetch Google Health Trends data."""
        if auth is None or locations is None or epiweeks is None or query is None:
            raise InvalidArgumentException("`auth`, `locations`, `epiweeks`, and `query` are all required")
        return self._create_call("ght/", dict(auth=auth, locations=locations, epiweeks=epiweeks, query=query))

    def twitter(
        self,
        auth: str,
        locations: StringParam,
        dates: Optional[EpiRangeParam] = None,
        epiweeks: Optional[EpiRangeParam] = None,
    ) -> CALL_TYPE:
        """Fetch HealthTweets data."""

        if auth is None or locations is None:
            raise InvalidArgumentException("`auth` and `locations` are both required")
        if not (dates is None) ^ (epiweeks is None):
            raise InvalidArgumentException("exactly one of `dates` and `epiweeks` is required")
        return self._create_call("twitter/", dict(auth=auth, locations=locations, dates=dates, epiweeks=epiweeks))

    def wiki(
        self,
        articles: StringParam,
        dates: Optional[EpiRangeParam] = None,
        epiweeks: Optional[EpiRangeParam] = None,
        hours: Optional[IntParam] = None,
        language: str = "en",
    ) -> CALL_TYPE:
        """Fetch Wikipedia access data."""

        if articles is None:
            raise InvalidArgumentException("`articles` is required")
        if not (dates is None) ^ (epiweeks is None):
            raise InvalidArgumentException("exactly one of `dates` and `epiweeks` is required")
        return self._create_call(
            "wiki/", dict(articles=articles, dates=dates, epiweeks=epiweeks, hours=hours, language=language)
        )

    def cdc(self, auth: str, epiweeks: EpiRangeParam, locations: StringParam) -> CALL_TYPE:
        """Fetch CDC page hits."""

        if auth is None or epiweeks is None or locations is None:
            raise InvalidArgumentException("`auth`, `epiweeks`, and `locations` are all required")

        return self._create_call("cdc/", dict(auth=auth, epiweeks=epiweeks, locations=locations))

    def quidel(self, auth: str, epiweeks: EpiRangeParam, locations: StringParam) -> CALL_TYPE:
        """Fetch Quidel data."""

        if auth is None or epiweeks is None or locations is None:
            raise InvalidArgumentException("`auth`, `epiweeks`, and `locations` are all required")

        return self._create_call("quidel/", dict(auth=auth, epiweeks=epiweeks, locations=locations))

    def norostat(self, auth: str, location: str, epiweeks: EpiRangeParam) -> CALL_TYPE:
        """Fetch NoroSTAT data (point data, no min/max)."""

        if auth is None or location is None or epiweeks is None:
            raise InvalidArgumentException("`auth`, `location`, and `epiweeks` are all required")
        return self._create_call("norostat/", dict(auth=auth, epiweeks=epiweeks, location=location))

    def meta_norostat(self, auth: str) -> CALL_TYPE:
        """Fetch NoroSTAT metadata."""

        if auth is None:
            raise InvalidArgumentException("`auth` is required")
        return self._create_call("meta_norostat/", dict(auth=auth))

    def afhsb(self, auth: str, locations: StringParam, epiweeks: EpiRangeParam, flu_types: StringParam) -> CALL_TYPE:
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

        return self._create_call("afhsb/", dict(auth=auth, locations=locations, epiweeks=epiweeks, flu_types=flu_types))

    def meta_afhsb(self, auth: str) -> CALL_TYPE:
        """Fetch AFHSB metadata."""

        if auth is None:
            raise InvalidArgumentException("`auth` is required")

        return self._create_call("meta_afhsb/", dict(auth=auth))

    def nidss_flu(
        self,
        regions: StringParam,
        epiweeks: EpiRangeParam,
        issues: Optional[EpiRangeParam] = None,
        lag: Optional[int] = None,
    ) -> CALL_TYPE:
        """Fetch NIDSS flu data."""

        if regions is None or epiweeks is None:
            raise InvalidArgumentException("`regions` and `epiweeks` are both required")
        if issues is not None and lag is not None:
            raise InvalidArgumentException("`issues` and `lag` are mutually exclusive")

        return self._create_call("nidss_flu/", dict(regions=regions, epiweeks=epiweeks, issues=issues, lag=lag))

    def nidss_dengue(self, locations: StringParam, epiweeks: EpiRangeParam) -> CALL_TYPE:
        """Fetch NIDSS dengue data."""

        if locations is None or epiweeks is None:
            raise InvalidArgumentException("`locations` and `epiweeks` are both required")

        return self._create_call("nidss_dengue/", dict(locations=locations, epiweeks=epiweeks))

    def delphi(self, system: str, epiweek: Union[int, str]) -> CALL_TYPE:
        """Fetch Delphi's forecast."""

        if system is None or epiweek is None:
            raise InvalidArgumentException("`system` and `epiweek` are both required")
        return self._create_call("delphi/", dict(system=system, epiweek=epiweek))

    def sensors(self, auth: str, names: StringParam, locations: StringParam, epiweeks: EpiRangeParam) -> CALL_TYPE:
        """Fetch Delphi's digital surveillance sensors."""

        if auth is None or names is None or locations is None or epiweeks is None:
            raise InvalidArgumentException("`auth`, `names`, `locations`, and `epiweeks` are all required")
        return self._create_call("sensors/", dict(auth=auth, names=names, locations=locations, epiweeks=epiweeks))

    def dengue_sensors(
        self, auth: str, names: StringParam, locations: StringParam, epiweeks: EpiRangeParam
    ) -> CALL_TYPE:
        """Fetch Delphi's digital surveillance sensors."""

        if auth is None or names is None or locations is None or epiweeks is None:
            raise InvalidArgumentException("`auth`, `names`, `locations`, and `epiweeks` are all required")

        return self._create_call(
            "dengue_sensors/", dict(auth=auth, names=names, locations=locations, epiweeks=epiweeks)
        )

    def nowcast(self, locations: StringParam, epiweeks: EpiRangeParam) -> CALL_TYPE:
        """Fetch Delphi's wILI nowcast."""

        if locations is None or epiweeks is None:
            raise InvalidArgumentException("`locations` and `epiweeks` are both required")

        return self._create_call("nowcast/", dict(locations=locations, epiweeks=epiweeks))

    def dengue_nowcast(self, locations: StringParam, epiweeks: EpiRangeParam) -> CALL_TYPE:
        """Fetch Delphi's dengue nowcast."""

        if locations is None or epiweeks is None:
            raise InvalidArgumentException("`locations` and `epiweeks` are both required")
        return self._create_call("dengue_nowcast/", dict(locations=locations, epiweeks=epiweeks))

    def meta(self) -> CALL_TYPE:
        """Fetch API metadata."""
        return self._create_call("meta/", {})

    def covidcast(
        self,
        data_source: str,
        signals: StringParam,
        time_type: str,
        geo_type: str,
        time_values: EpiRangeParam,
        geo_values: Union[int, str, Iterable[Union[int, str]]],
        as_of: Union[None, str, int] = None,
        issues: Optional[EpiRangeParam] = None,
        lag: Optional[int] = None,
    ) -> CALL_TYPE:
        """Fetch Delphi's COVID-19 Surveillance Streams"""
        if any((v is None for v in (data_source, signals, time_type, geo_type, time_values, geo_values))):
            raise InvalidArgumentException(
                "`data_source`, `signals`, `time_type`, `geo_type`, `time_values`, and `geo_values` are all required"
            )
        if issues is not None and lag is not None:
            raise InvalidArgumentException("`issues` and `lag` are mutually exclusive")

        return self._create_call(
            "covidcast/",
            dict(
                data_source=data_source,
                signals=signals,
                time_type=time_type,
                geo_type=geo_type,
                time_values=time_values,
                as_of=as_of,
                issues=issues,
                lag=lag,
                geo_values=geo_values,
            ),
        )

    def covidcast_meta(self) -> CALL_TYPE:
        """Fetch Delphi's COVID-19 Surveillance Streams metadata"""
        return self._create_call("covidcast_meta/", {})

    def covid_hosp(
        self,
        states: StringParam,
        dates: EpiRangeParam,
        issues: Optional[EpiRangeParam] = None,
        as_of: Union[None, int, str] = None,
    ) -> CALL_TYPE:
        """Fetch COVID hospitalization data."""

        if states is None or dates is None:
            raise InvalidArgumentException("`states` and `dates` are both required")
        return self._create_call("covid_hosp/", dict(states=states, dates=dates, issues=issues, as_of=as_of))

    def covid_hosp_facility(
        self,
        hospital_pks: StringParam,
        collection_weeks: StringParam,
        publication_dates: Optional[EpiRangeParam] = None,
    ) -> CALL_TYPE:
        """Fetch COVID hospitalization data for specific facilities."""

        if hospital_pks is None or collection_weeks is None:
            raise InvalidArgumentException("`hospital_pks` and `collection_weeks` are both required")

        return self._create_call(
            "covid_hosp_facility/",
            dict(hospital_pks=hospital_pks, collection_weeks=collection_weeks, publication_dates=publication_dates),
        )

    def covid_hosp_facility_lookup(
        self,
        state: Optional[str] = None,
        ccn: Optional[str] = None,
        city: Optional[str] = None,
        zip: Optional[str] = None,  # pylint: disable=redefined-builtin
        fips_code: Optional[str] = None,
    ) -> CALL_TYPE:
        """Lookup COVID hospitalization facility identifiers."""

        if all((v is None for v in (state, ccn, city, zip, fips_code))):
            raise InvalidArgumentException("one of `state`, `ccn`, `city`, `zip`, or `fips_code` is required")

        return self._create_call(
            "covid_hosp_facility_lookup/",
            dict(state=state, ccn=ccn, city=city, zip=zip, fips_code=fips_code),
        )

    def covidcast_nowcast(
        self,
        data_source: str,
        signals: StringParam,
        sensor_names: StringParam,
        time_type: str,
        geo_type: str,
        time_values: EpiRangeParam,
        geo_values: StringParam,
        as_of: Union[None, int, str] = None,
        issues: Optional[EpiRangeParam] = None,
        lag: Optional[int] = None,
    ) -> CALL_TYPE:
        """Fetch Delphi's COVID-19 Nowcast sensors"""

        if any((v is None for v in (data_source, signals, time_type, geo_type, time_values, geo_values, sensor_names))):
            raise InvalidArgumentException(
                "`data_source`, `signals`, `sensor_names`, `time_type`, `geo_type`, `time_values`, and `geo_value`"
                + " are all required"
            )
        if issues is not None and lag is not None:
            raise InvalidArgumentException("`issues` and `lag` are mutually exclusive")

        return self._create_call(
            "covidcast_nowcast/",
            dict(
                data_source=data_source,
                signals=signals,
                sensor_names=sensor_names,
                time_type=time_type,
                geo_type=geo_type,
                time_values=time_values,
                as_of=as_of,
                issues=issues,
                lag=lag,
                geo_values=geo_values,
            ),
        )
