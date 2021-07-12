from datetime import date
from delphi_epidata.requests import Epidata, EpiRange

apicall = Epidata.covidcast("fb-survey", "smoothed_cli", "day", "nation", EpiRange(20210405, 20210410), "us")

print(apicall)

classic = apicall.classic()
print(classic)

r = apicall.csv()
print(r[0:100])

data = apicall.json()
print(data[0])

df = apicall.df()
print(df.columns)
print(df.dtypes)

for row in apicall.iter():
    print(row)

StagingEpidata = Epidata.with_base_url("https://staging.delphi.cmu.edu/epidata/")

df = StagingEpidata.covidcast(
    "fb-survey", "smoothed_cli", "day", "nation", EpiRange(date(2021, 4, 5), date(2021, 4, 10)), "*"
).df()
print(df.shape)
