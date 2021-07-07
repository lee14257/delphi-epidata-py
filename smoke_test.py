from delphi_epidata.model import EpiRange
from delphi_epidata import EpiDataClassic, EpiDataCSV, EpiDataDataFrame, EpiDataIterator, EpiDataJSON

classic = EpiDataClassic().covidcast("fb-survey", "smoothed_cli", "day", "nation", EpiRange(20210405, 20210410), "us")
print(classic)

r = EpiDataCSV().covidcast("fb-survey", "smoothed_cli", "day", "nation", EpiRange(20210405, 20210410), "us")
print(r[0:100])

data = EpiDataJSON().covidcast("fb-survey", "smoothed_cli", "day", "nation", EpiRange(20210405, 20210410), "us")
print(data[0])

df = EpiDataDataFrame().covidcast("fb-survey", "smoothed_cli", "day", "nation", EpiRange(20210405, 20210410), "us")
print(df.columns)

for row in EpiDataIterator().covidcast(
    "fb-survey", "smoothed_cli", "day", "nation", EpiRange(20210405, 20210410), "us"
):
    print(row)
