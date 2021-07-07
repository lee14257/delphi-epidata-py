from asyncio import get_event_loop
from delphi_epidata.model import EpiRange
from delphi_epidata import covidcast


async def main() -> None:
    apicall = covidcast("fb-survey", "smoothed_cli", "day", "nation", EpiRange(20210405, 20210410), "us")
    classic = await apicall.async_classic()
    print(classic)

    r = await apicall.async_csv()
    print(r[0:100])

    data = await apicall.async_json()
    print(data[0])

    async for row in apicall.async_iter():
        print(row)


loop = get_event_loop()
loop.run_until_complete(main())
