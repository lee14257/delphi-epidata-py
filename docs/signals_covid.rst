Fetching Data
=============

Signals
-------





                  
Metadata
--------

Many data sources and signals are available, so one can also obtain a data frame
of all signals and their associated metadata

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

