import asyncio
import aiohttp
import platform
from util import async_timed
from ch04_fetch_status import fetch_status

@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        url = 'https://www.example.com'
        pending = [
            asyncio.create_task(fetch_status(session, url)),
            asyncio.create_task(fetch_status(session, url, 3)),
            asyncio.create_task(fetch_status(session, url, 1)),
        ]

        while pending:
            done, pending = await asyncio.wait(pending,
                                               return_when=asyncio.FIRST_COMPLETED)

            print(f'Done task count: {len(done)}')
            print(f'Pending task count: {len(pending)}')

            for done_task in done:
                print(await done_task)

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
