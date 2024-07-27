import asyncio
import platform

import aiohttp

from ch04.ch04_fetch_status import fetch_status
from util.async_timer import async_timed

"""
return_exceptions=False
our gather call will also throw that exception when we await it. However,
even though one of our coroutines failed, our other coroutines are not 
canceled and will continue to run
"""


@async_timed()
async def main1():
    async with aiohttp.ClientSession() as session:
        urls = ["https://example.com", "python://example.com"]
        requests = [fetch_status(session, url) for url in urls]
        status_codes = await asyncio.gather(*requests)
        print(status_codes)


"""
return_exceptions=True
gather will return any exceptions as part of the result list it returns
when we await it. The call to gather will not throw any exceptions itself,
and we’ll be able handle all exceptions as we wish.
"""


@async_timed()
async def main2():
    async with aiohttp.ClientSession() as session:
        urls = ["https://example.com", "python://example.com"]
        requests = [fetch_status(session, url) for url in urls]
        results = await asyncio.gather(*requests, return_exceptions=True)

        exceptions = [res for res in results if isinstance(res, Exception)]
        successful_results = [res for res in results if not isinstance(res, Exception)]

        print(f"All results: {results}")
        print(f"Finished successfully: {successful_results}")
        print(f"Threw exceptions: {exceptions}")


if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
print("###### return_exceptions = True")
asyncio.run(main2())
print("\n\n\n")
print("###### return_exceptions = False")
asyncio.run(main1())
