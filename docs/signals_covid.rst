Fetching Data
=============

Signals
-------

This package provides a key function to obtain any signal of interest as a
Pandas data frame. Detailed examples are provided in the :ref:`usage examples
<getting-started>`.



Sometimes you would like to work with multiple signals -- for example, to obtain
several signals at every location, as part of building models of features at
each location. For convenience, the package provides a function to produce a
single data frame containing multiple signals at each location.



                  
Metadata
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