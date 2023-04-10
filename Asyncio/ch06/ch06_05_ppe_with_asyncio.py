import asyncio
from asyncio.events import AbstractEventLoop
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from typing import List


def count(count_to: int) -> int:
    counter = 0
    while counter < count_to:
        counter = counter +1
    return counter

async def main():
    with ProcessPoolExecutor() as process_pool:
        loop: AbstractEventLoop = asyncio.get_running_loop()
        nums = [1, 3, 5, 100000000, 22]
        # create a partially applied function
        calls: List[partial[int]] = [partial(count, num) for num in nums]
        call_coros = []

        for call in calls:
            # submit each call to the process pool
            call_coros.append(loop.run_in_executor(process_pool, call))

        # results will have a list of string values
        # results = await asyncio.gather(*call_coros)
        # for result in results:
        #     print(result)

        # an iterator of futures is returned
        for finished_task in asyncio.as_completed(call_coros):
            print(await finished_task)



if __name__ == "__main__":
    asyncio.run(main())