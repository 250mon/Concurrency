import asyncio
import concurrent.futures
import functools
import time
import os
from typing import Dict, List
from ch06_08_count_words_freq_parallel import (
    partition, merge_dictionaries, map_frequencies
)


file_path = os.path.join('E:/Datasets', 'googlebooks-eng-all-1gram-20120701-a')
if not os.path.exists(file_path):
    print('File not found')
    exit(0)

async def reduce(loop, pool, counters, chunk_size) -> Dict[str, int]:
    chunks: List[List[Dict]] = list(partition(counters, chunk_size))
    reducers = []
    # while len(chunks[0]) > 1:
    while len(chunks[0]) > 1:
        for chunk in chunks:
            reducer = functools.partial(functools.reduce,
                                        merge_dictionaries,
                                        chunk)
            reducers.append(loop.run_in_executor(pool, reducer))
        reducer_chunks = await asyncio.gather(*reducers)
        chunks = list(partition(reducer_chunks, chunk_size))
        reducers.clear()
    return chunks[0][0]

async def main(partition_size: int):
    with open(file_path, encoding='utf-8') as f:
        contents = f.readlines()
        loop = asyncio.get_running_loop()
        tasks = []
        start = time.time()
        with concurrent.futures.ProcessPoolExecutor() as pool:
            for chunk in partition(contents, partition_size):
                # for each partition, run our map operation in a separate process
                counter_func = functools.partial(map_frequencies, chunk)
                tasks.append(loop.run_in_executor(pool, counter_func))
            # wait for all map operation to complete
            intermediate_results = await asyncio.gather(*tasks)
            # parallel reduce all our intermediate map results into a result
            final_result = await reduce(loop, pool, intermediate_results, 500)

            print(f"Aardvark has appeared {final_result['Aardvark']} times.")

            end = time.time()
            print(f'MapReduce took: {(end - start):.4f} seconds')


if __name__ == '__main__':
    asyncio.run(main(partition_size=60000))
