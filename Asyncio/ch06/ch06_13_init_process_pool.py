from concurrent.futures import ProcessPoolExecutor
import asyncio
from multiprocessing import Value
from functools import partial
from typing import List

# shared among processes created by the process pool
# shared_counter will contain the reference to the shared
# Value object we create
shared_counter: Value

# the init function will be called for each process that
# the process pool creates, correctly initializing the shared_counter
# to the one we created in the main coroutine
def init(counter: Value):
    global shared_counter
    shared_counter = counter

def increment(count_to: int):
    local_counter = 0
    for i in range(min(count_to, 100)):
        local_counter += i

    with shared_counter.get_lock():
        shared_counter.value += 1

    for i in range(max(count_to, 100)):
        local_counter += i

    print(local_counter)

async def main():
    counter = Value('d', 0)
    with ProcessPoolExecutor(initializer=init,
                             initargs=(counter,)) as pool:
        nums = [100, 200, 100000]
        calls: List[partial[int]] = [partial(increment, num) for num in nums]
        for call in calls:
            await asyncio.get_running_loop().run_in_executor(pool, call)
        print(counter.value)


if __name__ == "__main__":
    asyncio.run(main())