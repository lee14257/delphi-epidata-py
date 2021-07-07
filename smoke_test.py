from delphi_epidata.requests import Epidata

apicall = Epidata.covidcast("fb-survey", "smoothed_cli", "day", "nation", Epidata.range(20210405, 20210410), "us")

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
