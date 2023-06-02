import asyncio
import aiohttp
from aiohttp import ClientSession
from util import async_timed
import platform
from ch04_fetch_status import fetch_status


"""
asyncio.gather()
This function takes in a sequence of awaitables and lets us run
them concurrently, all in one line of code.
If any of the awaitables we pass in is a coroutine, gather will 
automatically wrap it in a task to ensure that it runs concurrently.
Thi means that we don't have to wrap everything with 
asyncio.create_task separately as we used.

It returns an awaitable. When we use it in an await expression,
it will pause until all awaitables that we passed into it are
complete. Once everything we passed in finishes, it will return
a list of the completed results

"""
@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        urls = ['https://example.com' for _ in range(1000)]
        requests = [fetch_status(session, url) for url in urls]
        status_codes = await asyncio.gather(*requests)
        print(status_codes)

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())