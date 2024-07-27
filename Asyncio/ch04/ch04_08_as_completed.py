import asyncio
import platform

import aiohttp

from ch04.ch04_fetch_status import fetch_status
from util.async_timer import async_timed

"""
as_completed()
This method takes a list of awaitables and returns an iterator of futures.
We can then iterate over these futures, awaiting each one.
there is now no deterministic ordering of results, since we have no 
guarantees as to which requests will complete first.
"""


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        fetchers = [
            fetch_status(session, "https://www.example.com", 10),
            fetch_status(session, "https://www.example.com", 1),
            fetch_status(session, "https://www.example.com", 5),
        ]

        for finished_task in asyncio.as_completed(fetchers):
            print(await finished_task)


if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
