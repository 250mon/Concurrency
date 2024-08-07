import asyncio

import asyncpg

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
        results = await asyncio.gather(query_product(pool), query_product(pool))
        print(results)


asyncio.run(main())

