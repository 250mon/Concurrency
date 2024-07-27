import asyncio
import logging
import platform

import aiohttp

from ch04.ch04_fetch_status import fetch_status
from util.async_timer import async_timed

"""
The drawbacks of ALL_COMPLETED are like the drawbacks we saw with gather. We
could have any number of exceptions while we wait for other coroutines to complete,
which we won’t see until all tasks complete. This could be an issue if, because
of one exception, we’d like to cancel other running requests

To support these use cases, wait supports the FIRST_EXCEPTION option. When we
use this option, we’ll get two different behaviors, depending on whether any of our
tasks throw exceptions.

1. No exceptions
the same as ALL_COMPLETED

2. One or more exceptions 
wait will immediately return once the exceptions is thrown.
The done set will have any coroutines that finished successfully alongside
any coroutines with exceptions. The done set is, at minimum, guaranteed to have one
failed task in this case but may have successfully completed tasks. The pending set
may be empty, but it may also have tasks that are still running. We can then use this
pending set to manage the currently running tasks as we desire.
"""


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        fetchers = [
            asyncio.create_task(fetch_status(session, "python://bad.com")),
            asyncio.create_task(
                fetch_status(session, "https://www.example.com", delay=3)
            ),
            asyncio.create_task(
                fetch_status(session, "https://www.example.com", delay=3)
            ),
        ]

        done, pending = await asyncio.wait(
            fetchers, return_when=asyncio.FIRST_EXCEPTION
        )

        print(f"Done task count: {len(done)}")
        print(f"Pending task count: {len(pending)}")

        for done_task in done:
            if done_task.exception() is None:
                print(done_task.result())
            else:
                logging.error(
                    "Request got an exception", exc_info=done_task.exception()
                )

        for pending_task in pending:
            pending_task.cancel()


if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
