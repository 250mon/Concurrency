import asyncio
import aiohttp
import platform
from util import async_timed
from ch04_fetch_status import fetch_status


'''
Note that our tasks in the pending set are not canceled and will
continue to run despite the timeout. If we have a use case where we want to
terminate the tasks, we'll need to explicitly loop through the pending set
and call cancel on each task.
'''
@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        url = 'https://www.example.com'
        fetchers = [
            asyncio.create_task(fetch_status(session, url)),
            asyncio.create_task(fetch_status(session, url)),
            asyncio.create_task(fetch_status(session, url, 3)),
        ]

        done, pending = await asyncio.wait(fetchers, timeout=1)

        print(f'Done task count: {len(done)}')
        print(f'Pending task count: {len(pending)}')

        for done_task in done:
            print(await done_task)

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
