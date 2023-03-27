import asyncio
import aiohttp
from util import async_timed
import platform
from ch04_fetch_status import fetch_status


'''
wait
this method returns two sets: a set of tasks that are finished with either
a result or an exception, and a set of tasks that are still running.
This function also allows us to specify a timeout that behaves differently 
from how other API methods operate; it does not throw exceptions.
'''


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        fetchers = [
            asyncio.create_task(fetch_status(session, 'https://www.example.com')),
            asyncio.create_task(fetch_status(session, 'https://www.example.com')),
        ]
        done, pending = await asyncio.wait(fetchers)

        print(f'Done task count: {len(done)}')
        print(f'Pending task count: {len(pending)}')

        for done_task in done:
            result = await done_task
            print(result)

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
