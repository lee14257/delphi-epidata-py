from delphi_epidata import covidcast_meta

apicall = covidcast_meta()
classic = apicall.classic()

r = apicall.csv()
print(r[0:100])

data = apicall.json()
print(data[0])

for i, row in enumerate(apicall.iter()):
    print(row)
    if i > 5:
        break
