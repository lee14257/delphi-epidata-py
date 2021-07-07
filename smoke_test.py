from delphi_epidata.model import EpiRange
from delphi_epidata import covidcast

apicall = covidcast("fb-survey", "smoothed_cli", "day", "nation", EpiRange(20210405, 20210410), "us")
classic = apicall.classic()
print(classic)

r = apicall.csv()
print(r[0:100])

data = apicall.json()
print(data[0])

df = apicall.df()
print(df.columns)

for row in apicall.iter():
    print(row)
