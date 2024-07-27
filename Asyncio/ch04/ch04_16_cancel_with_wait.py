import asyncio
import platform

import aiohttp

from ch04.ch04_fetch_status import fetch_status

"""
Why wrap everything in a task???

We'd expect for this code to print out API B is too slow and cancelling, but what
happens if we don't see this message at all? This can happen because when we call
'wait' with just coroutines they are automatically wrapped in tasks, and the 'done'
and 'pending' sets returned are those tasks that 'wait' created for us. This means
that we can't do any comparisons to see which specific task is in the 'pending'
set such as 'if task is api_b', since we'll be comparing a task object, we have no
access to with a coroutine
"""


async def main():
    async with aiohttp.ClientSession() as session:
        api_a = fetch_status(session, "https://www.example.com")
        api_b = fetch_status(session, "https://www.example.com", delay=2)

        done, pending = await asyncio.wait([api_a, api_b], timeout=1)

        for task in pending:
            if task is api_b:
                print("API B too slow, cancelling")
                task.cancel()


if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
