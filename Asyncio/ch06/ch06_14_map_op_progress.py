import asyncio
import functools
import os
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Value
from typing import Dict, List

from util.ch06_utils import merge_dictionaries, partition

# file_path = os.path.join('E:/Datasets', 'googlebooks-eng-all-1gram-20120701-a')
file_path = os.path.join(
    "D:/Datasets/Concurrency", "googlebooks-eng-all-1gram-20120701-a"
)
if not os.path.exists(file_path):
    print("File not found")
    exit(0)

map_progress: Value


def init(progress: Value):
    global map_progress
    map_progress = progress


def map_frequencies(chunk: List[str]) -> Dict[str, int]:
    counter = {}
    for line in chunk:
        word, _, count, _ = line.split("\t")
        counter[word] = counter.setdefault(word, 0) + int(count)

    with map_progress.get_lock():
        map_progress.value += 1

    return counter


async def progress_reporter(total_partition: int):
    while map_progress.value < total_partition:
        print(f"Finished {map_progress.value} / {total_partition} map operations")
        await asyncio.sleep(1)


async def main(partition_size: int):
    global map_progress

    with open(file_path, encoding="utf-8") as f:
        contents = f.readlines()
        loop = asyncio.get_running_loop()
        tasks = []
        map_progress = Value("i", 0)

        with ProcessPoolExecutor(initializer=init, initargs=(map_progress,)) as pool:
            total_partitions = len(contents) // partition_size
            reporter = asyncio.create_task(progress_reporter(total_partitions))
            for chunk in partition(contents, partition_size):
                counter_func = functools.partial(map_frequencies, chunk)
                tasks.append(loop.run_in_executor(pool, counter_func))

            counters = await asyncio.gather(*tasks)
            await reporter

            final_result = functools.reduce(merge_dictionaries, counters)
            print(f"Aardvark has appeared {final_result['Aardvark']} times.")


if __name__ == "__main__":
    asyncio.run(main(partition_size=60000))
