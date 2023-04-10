import asyncio
import asyncpg
from util import async_timed
from ch05.ch05_util import get_options
from typing import List, Dict
from concurrent.futures.process import ProcessPoolExecutor


product_query = \
    """
    SELECT
        p.product_id,
        p.product_name,
        p.brand_id,
        s.sku_id,
        pc.product_color_name,
        ps.product_size_name
    FROM product as p
    JOIN sku as s on s.product_id = p.product_id
    JOIN product_color as pc on pc.product_color_id = s. product_color_id
    JOIN product_size as ps on ps.product_size_id = s.product_size_id
    WHERE p.product_id = 100
    """

async def query_product(pool):
    async with pool.acquire() as connection:
        return await connection.fetchrow(product_query)


@async_timed()
async def query_products_concurrently(pool, queries):
    queries = [query_product(pool) for _ in range(queries)]
    return await asyncio.gather(*queries)


def run_in_new_loop(num_queries: int) -> List[Dict]:
    async def run_queries():
        options = get_options("db_settings")
        host_addr = options['host_addr']
        port_num = int(options['port_num'])
        passwd = options['password']
        async with asyncpg.create_pool(host=host_addr,
                                       port=port_num,
                                       user='postgres',
                                       password=passwd,
                                       database='postgres',
                                       min_size=6,
                                       max_size=6) as pool:
            return await query_products_concurrently(pool, num_queries)

    # Run queries in a new event loop, and convert them to dictionaries
    results = [dict(result) for result in asyncio.run(run_queries())]
    return results

@async_timed()
async def main():
    loop = asyncio.get_running_loop()
    pool = ProcessPoolExecutor()
    # Create five processes
    tasks = [loop.run_in_executor(pool, run_in_new_loop, 1000) for _ in range(5)]
    # Wait for all query results to complete
    all_results = await asyncio.gather(*tasks)
    total_queries = sum([len(result) for result in all_results])
    print(f'Retrieved {total_queries} products the product database')


if __name__ == "__main__":
    asyncio.run(main())