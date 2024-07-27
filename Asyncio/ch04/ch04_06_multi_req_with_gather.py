import asyncio
import platform

import aiohttp

from ch04.ch04_fetch_status import fetch_status
from util.async_timer import async_timed

"""
asyncio.gather()
This function takes in a sequence of awaitables and lets us run them concurrently, all in one line of code.
If any of the awaitables we pass in is a coroutine, gather will automatically wrap it in a task to ensure
that it runs concurrently.
Thi means that we don't have to wrap everything with asyncio.create_task separately as we used.

It returns an awaitable. When we use it in an await expression, it will pause until all awaitables that we passed
into it are complete. Once everything we passed in finishes, it will return a list of the completed results


** gather has a few drawbacks. 
The first, which was already mentioned, is that it isn’t easy to cancel our tasks if one throws an exception
The second is that we must wait for all our coroutines to finish before we can process our results.

"""


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        urls = ["https://example.com" for _ in range(1000)]
        requests = [fetch_status(session, url) for url in urls]
        status_codes = await asyncio.gather(*requests)
        print(status_codes)


if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
