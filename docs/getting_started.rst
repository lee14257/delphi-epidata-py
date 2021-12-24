.. _getting-started:

Getting Started
===============

Overview
--------------

This package provides access to data from various Epidata API endpoints including COVIDcast, 
which provides numerous COVID-related data streams, updated daily. 

Epidata Endpoints Overview
--------------

**COVID-19 Data**

- `covidcast <https://cmu-delphi.github.io/delphi-epidata/api/covidcast.html>`_
      Delphi’s COVID-19 surveillance streams.
- `covidcast_meta <https://cmu-delphi.github.io/delphi-epidata/api/covidcast_meta.html>`_
      Metadata for Delphi’s COVID-19 surveillance streams.
- `covid_hosp <https://cmu-delphi.github.io/delphi-epidata/api/covid_hosp.html>`_
      COVID-19 Reported Patient Impact and Hospital Capacity.
- `covid_hosp_facility <https://cmu-delphi.github.io/delphi-epidata/api/covid_hosp_facility.html>`_
      COVID-19 Reported Patient Impact and Hospital Capacity - Facility Lookup
- `covid_hosp_facility_lookup <https://cmu-delphi.github.io/delphi-epidata/api/covid_hosp_facility.html>`_
      COVID-19 Reported Patient Impact and Hospital Capacity by Facility
- `covid_hosp_state_timeseries <https://cmu-delphi.github.io/delphi-epidata/api/covid_hosp.html>`_
      COVID-19 Reported Patient Impact and Hospital Capacity by State Timeseries



**Influenza Data**

- `afhsb <https://cmu-delphi.github.io/delphi-epidata/api/afhsb.html>`_
      TODO
- `cdc <https://cmu-delphi.github.io/delphi-epidata/api/cdc.html>`_
      CDC Page Hits   
- `delphi <https://cmu-delphi.github.io/delphi-epidata/api/delphi.html>`_
      Delphi’s Forecast 
- `ecdc_ili <https://cmu-delphi.github.io/delphi-epidata/api/ecdc_ili.html>`_
      ECDC ILI data from the ECDC website.
- `flusurv <https://cmu-delphi.github.io/delphi-epidata/api/flusurv.html>`_
      FluSurv-NET data (flu hospitaliation rates) from CDC.
- `fluview <https://cmu-delphi.github.io/delphi-epidata/api/fluview.html>`_
      Influenza-like illness (ILI) from U.S. Outpatient Influenza-like Illness Surveillance Network (ILINet).
- `fluview_meta <https://cmu-delphi.github.io/delphi-epidata/api/fluview_meta.html>`_
      Summary data about fluview.
- `fluview_clinical <https://cmu-delphi.github.io/delphi-epidata/api/fluview_clinical.html>`_
      FluView Clinical
- `gft <https://cmu-delphi.github.io/delphi-epidata/api/gft.html>`_
      Estimate of influenza activity based on volume of certain search queries. Google has discontinued Flu Trends, and this is now a static endpoint.
- `ght <https://cmu-delphi.github.io/delphi-epidata/api/ght.html>`_
      Google Health Trends data. Estimate of influenza activity based on volume of certain search queries.
- `kcdc_ili <https://cmu-delphi.github.io/delphi-epidata/api/kcdc_ili.html>`_
      KCDC ILI data from KCDC website.
- `meta <https://cmu-delphi.github.io/delphi-epidata/api/meta.html>`_
      Metadata for fluview, twitter, wiki, and delphi.
- `meta_afhsb <https://cmu-delphi.github.io/delphi-epidata/api/meta_afhsb.html>`_
      AFHSB Metadata
- `nidss_flu <https://cmu-delphi.github.io/delphi-epidata/api/nidss_flu.html>`_
      Outpatient ILI from Taiwan’s National Infectious Disease Statistics System (NIDSS).
- `nowcast <https://cmu-delphi.github.io/delphi-epidata/api/nowcast.html>`_
      A nowcast of U.S. national, regional, and state-level (weighted) percent ILI, available seven days (regionally) or five days (state-level) before the first ILINet report for the corresponding week.
- `quidel <https://cmu-delphi.github.io/delphi-epidata/api/quidel.html>`_
      Data provided by Quidel Corp., which contains flu lab test results.
- `sensors <https://cmu-delphi.github.io/delphi-epidata/api/sensors.html>`_
      Delphi’s Digital Surveillance Sensors
- `twitter <https://cmu-delphi.github.io/delphi-epidata/api/twitter.html>`_
      Estimate of influenza activity based on analysis of language used in tweets from HealthTweets.
- `wiki <https://cmu-delphi.github.io/delphi-epidata/api/wiki.html>`_
      Wikipedia Access Logs. Number of page visits for selected English, Influenza-related wikipedia articles.


**Dengue Data**

- `dengue_nowcast <https://cmu-delphi.github.io/delphi-epidata/api/dengue_nowcast.html>`_
      Delphi’s Dengue Nowcast data
- `dengue_sensors <https://cmu-delphi.github.io/delphi-epidata/api/dengue_sensors.html>`_
      Delphi’s Dengue Digital Surveillance Sensors
- `nidss_dengue <https://cmu-delphi.github.io/delphi-epidata/api/nidss_dengue.html>`_
      Counts of confirmed dengue cases from Taiwan’s NIDSS.
- `paho_dengue <https://cmu-delphi.github.io/delphi-epidata/api/paho_dengue.html>`_
      PAHO Dengue

**Norovirus Data**

- `meta_norostat <https://cmu-delphi.github.io/delphi-epidata/api/meta_norostat.html>`_
      NoroSTAT Metadata
- `norostat <https://cmu-delphi.github.io/delphi-epidata/api/norostat.html>`_
      Suspected and confirmed norovirus outbreaks reported by state health departments to the CDC.



Basic examples
--------------

To obtain all available sources of epidemiological data, we can use the following command:

>>> from delphi_epidata.request import CovidcastEpidata, EpiRange
>>> epidata = CovidcastEpidata()
>>> print(list(epidata.source_names))
['chng-cli', 'chng-covid', 'covid-act-now', 'doctor-visits', 'fb-survey', 'google-symptoms', 'hhs', 'hospital-admissions', 'indicator-combination-cases-deaths', 'jhu-csse', 'quidel-covid-ag', 'safegraph-weekly', 'usa-facts', 'ght', 'google-survey', 'indicator-combination-nmf', 'quidel-flu', 'safegraph-daily', 'nchs-mortality']


To obtain smoothed estimates of COVID-like illness from our symptom survey,
distributed through Facebook (`fb-survey`), for every county in the United States between
2020-05-01 and 2020-05-07:

>>> from delphi_epidata.request import EpiRange
>>> apicall = epidata[("fb-survey", "smoothed_cli")].call(    
...     'county', "*", EpiRange(20200501, 20200507),
... )
EpiDataCall(endpoint=covidcast, params={'data_source': 'fb-survey', 'signals': 'smoothed_cli', 'time_type': 'day', 'time_values': '20200501-20200507', 'geo_type': 'county', 'geo_values': '*'})
>>> data = apicall.df()
>>> data.head()
      source        signal geo_type geo_value time_type time_value      issue  lag     value    stderr  sample_size  direction  missing_value   missing_stderr  missing_sample_size
0  fb-survey  smoothed_cli   county     01000       day 2020-05-01 2020-09-03  125  0.825410  0.136003         1722        NaN              0                0                    0
1  fb-survey  smoothed_cli   county     01001       day 2020-05-01 2020-09-03  125  1.299425  0.967136          115        NaN              0                0                    0   
2  fb-survey  smoothed_cli   county     01003       day 2020-05-01 2020-09-03  125  0.696597  0.324753          584        NaN              0                0                    0   
3  fb-survey  smoothed_cli   county     01015       day 2020-05-01 2020-09-03  125  0.428271  0.548566          122        NaN              0                0                    0   
4  fb-survey  smoothed_cli   county     01031       day 2020-05-01 2020-09-03  125  0.025579  0.360827          114        NaN              0                0                    0   


Each row represents one observation in one county on one day. The county FIPS
code is given in the ``geo_value`` column, the date in the ``time_value``
column. Here ``value`` is the requested signal---in this case, the smoothed
estimate of the percentage of people with COVID-like illness, based on the
symptom surveys. ``stderr`` is its standard error. The ``issue`` column
indicates when this data was reported; in this case, the survey estimates for
May 1st were updated on September 3rd based on new data, giving a ``lag`` of 125 days.
See the `Delphi Epidata API <https://cmu-delphi.github.io/delphi-epidata/api/README.html#epidata-api-other-diseases>`_ documentation for details on all fields of the returned data frame.

The API documentation lists each available signal and provides technical details
on how it is estimated and how its standard error is calculated. In this case,
for example, the `symptom surveys documentation page
<https://cmu-delphi.github.io/delphi-epidata/api/covidcast-signals/fb-survey.html>`_
explains the definition of "COVID-like illness", links to the exact survey text,
and describes the mathematical derivation of the estimates.

Using the ``geo_values`` argument, we can request data for a specific geography,
such as the state of Pennsylvania for the month of September 2021:

>>> pa_data = epidata[("fb-survey", "smoothed_cli")].call(    
...         'state', "pa", EpiRange(20210901, 20210930)
...     ).df()
>>> pa_data.head()
      source        signal geo_type geo_value time_type time_value      issue  lag     value    stderr  sample_size  direction  missing_value  missing_stderr  missing_sample_size
0  fb-survey  smoothed_cli    state        pa       day 2021-09-01 2021-09-06    5  0.928210  0.088187         9390        NaN              0               0                    0
1  fb-survey  smoothed_cli    state        pa       day 2021-09-02 2021-09-07    5  0.894603  0.087308         9275        NaN              0               0                    0
2  fb-survey  smoothed_cli    state        pa       day 2021-09-03 2021-09-08    5  0.922847  0.088324         9179        NaN              0               0                    0
3  fb-survey  smoothed_cli    state        pa       day 2021-09-04 2021-09-09    5  0.984799  0.092566         9069        NaN              0               0                    0
4  fb-survey  smoothed_cli    state        pa       day 2021-09-05 2021-09-10    5  1.010306  0.093357         9016        NaN              0               0                    0

We can request multiple states by providing a list, such as ``["pa", "ny",
"mo"]``.