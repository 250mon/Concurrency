import asyncio
import concurrent.futures
import functools
import os
import time
from typing import Dict, List

# file_path = os.path.join('E:/Datasets', 'googlebooks-eng-all-1gram-20120701-a')
file_path = os.path.join("res", "googlebooks-eng-all-1gram-20120701-a")
if not os.path.exists(file_path):
    print("File not found")
    exit(0)


def partition(data: List, chunk_size: int) -> List:
    for i in range(0, len(data), chunk_size):
        yield data[i : i + chunk_size]


def map_frequencies(chunk: List[str]) -> Dict[str, int]:
    counter = {}
    for line in chunk:
        word, _, count, _ = line.split("\t")
        counter[word] = counter.setdefault(word, 0) + int(count)
    return counter


def merge_dictionaries(first: Dict[str, int], second: Dict[str, int]) -> Dict[str, int]:
    merged = first
    for key in second:
        merged[key] = merged.get(key, 0) + second[key]
    return merged


async def main(partition_size: int):
    with open(file_path, encoding="utf-8") as f:
        contents = f.readlines()
        loop = asyncio.get_running_loop()
        tasks = []
        start = time.time()
        with concurrent.futures.ProcessPoolExecutor() as pool:
            for chunk in partition(contents, partition_size):
                # for each partition, run our map operation in a separate process
                tasks.append(
                    loop.run_in_executor(
                        pool, functools.partial(map_frequencies, chunk)
                    )
                )
            # wait for all map operation to complete
            intermediate_results = await asyncio.gather(*tasks)
            # reduce all our intermediate map results into a result
            final_result = functools.reduce(merge_dictionaries, intermediate_results)

            print(f"Aardvark has appeared {final_result['Aardvark']} times.")

            end = time.time()
            print(f"MapReduce took: {(end - start):.4f} seconds")


if __name__ == "__main__":
    asyncio.run(main(partition_size=60000))

