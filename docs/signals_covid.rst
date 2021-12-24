Fetching Data
=============

Signals
-------

This package provides a key function to obtain any signal of interest and parse it in 4 different formats. 
Detailed examples are provided in the :ref:`usage examples <getting-started>`.

A signal is obtained by requesting an API call to an Epidata endpoint with defined parameters. 
An EpiDataCall object is first obtained using the functions from the Endpoint fetcher class below. 
This object will contain the appropriate  endpoint URL and the parameters required to make the API request. 


.. autoclass:: delphi_epidata.request.AEpiDataEndpoints()
    :members:


Output Data
--------

An EpiDataCall object can be used to make an API request and parse the resulting signal in 
4 different formats (Classic, JSON, CSV, and Pandas DataFrame)

.. autofunction:: delphi_epidata.request.EpiDataCall.classic

.. autofunction:: delphi_epidata.request.EpiDataCall.json

.. autofunction:: delphi_epidata.request.EpiDataCall.csv

.. autofunction:: delphi_epidata.request.EpiDataCall.df


COVIDcast Metadata
--------

Many data sources and signals are available, so one can also obtain a data frame
of all signals and their associated metadata:

>>> from delphi_epidata.request import CovidcastEpidata
>>> covid_ds = CovidcastEpidata()
>>> df_source = covid_ds.source_df
>>> df_signal = covid_ds.signal_df

Calling ``CovidcastEpidata`` function will return a class object ``CovidcastDataSources``, 
which has the property ``source_df`` and ``signal_df``, two data frames containing 
the information of all available sources and signals.
More details of the two data frames are listed below.

.. autoclass:: delphi_epidata.request.CovidcastDataSources()
    :members:

More metadata statistics can also be obtained as follows:

>>> from delphi_epidata.request import Epidata
>>> df = Epidata.covidcast_meta().df()

.. autofunction:: delphi_epidata.request.Epidata.covidcast_meta()