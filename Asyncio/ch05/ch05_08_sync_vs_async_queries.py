import asyncio

import asyncpg

from util.async_timer import async_timed
from util.db_handler import get_options

product_query = """
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
async def query_products_synchronously(pool, queries):
    return [await query_product(pool) for _ in range(queries)]


@async_timed()
async def query_products_concurrently(pool, queries):
    queries = [query_product(pool) for _ in range(queries)]
    return await asyncio.gather(*queries)


async def main():
    options = get_options("db_settings")
    host_addr = options["host_addr"]
    port_num = int(options["port_num"])
    passwd = options["password"]
    async with asyncpg.create_pool(
        host=host_addr,
        port=port_num,
        user="postgres",
        password=passwd,
        database="postgres",
        min_size=6,
        max_size=6,
    ) as pool:
        result = await query_products_synchronously(pool, 1)
        print(result)
        # await query_products_concurrently(pool, 10000)


asyncio.run(main())

