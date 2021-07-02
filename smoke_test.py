from delphi_epidata import covidcast_meta

classic = covidcast_meta().classic()

r = covidcast_meta().csv()
print(r[0:100])

data = covidcast_meta().json()
print(data[0])

for row in covidcast_meta().jsonl():
    print(row)
