import asyncio
import platform

import aiohttp

from ch04.ch04_fetch_status import fetch_status
from util.async_timer import async_timed

"""
wait
this method returns two sets: a set of tasks that are finished with either
a result or an exception, and a set of tasks that are still running.
This function also allows us to specify a timeout that behaves differently 
from how other API methods operate; it does not throw exceptions.
"""


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        fetchers = [
            asyncio.create_task(fetch_status(session, "https://www.example.com")),
            asyncio.create_task(fetch_status(session, "https://www.example.com")),
        ]
        done, pending = await asyncio.wait(fetchers)

        print(f"Done task count: {len(done)}")
        print(f"Pending task count: {len(pending)}")

        for done_task in done:
            result = await done_task
            print(result)


if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
