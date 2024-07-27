import asyncio
import logging
import platform

import aiohttp

from ch04.ch04_fetch_status import fetch_status
from util.async_timer import async_timed


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        good_request = fetch_status(session, "https://www.example.com")
        bad_request = fetch_status(session, "python://bad")

        fetchers = [asyncio.create_task(good_request), asyncio.create_task(bad_request)]

        done, pending = await asyncio.wait(fetchers)

        print(f"Done task count: {len(done)}")
        print(f"Pending task count: {len(pending)}")

        for done_task in done:
            # result = await done_task will throw an exception
            if done_task.exception() is None:
                print(done_task.result())
            else:
                logging.error(
                    "Request got an exception", exc_info=done_task.exception()
                )


if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())

