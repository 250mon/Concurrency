import asyncio
import platform

import aiohttp

from ch04.ch04_fetch_status import fetch_status
from util.async_timer import async_timed


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        fetchers = [
            fetch_status(session, "https://www.example.com", 10),
            fetch_status(session, "https://www.example.com", 1),
            fetch_status(session, "https://www.example.com", 5),
        ]

        for finished_task in asyncio.as_completed(fetchers, timeout=2):
            try:
                result = await finished_task
                print(result)
            except asyncio.TimeoutError:
                print("We got a timeout error!")

        for task in asyncio.tasks.all_tasks():
            print(task)


if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
