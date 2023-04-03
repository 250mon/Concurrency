import asyncio
from ch05_util import connect_pg


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


async def main():
    connection = await connect_pg()
    print('Creating the product database...')
    queries = [connection.fetch(product_query)]
    # results is the list output from gather
    # connection.fetch(query) will produce a list of Record output
    # so, when we have one query statement to get through fetch(),
    # a list of list of Record will come out.
    results = await asyncio.gather(*queries)
    for item in results[0]:
        print(item)

asyncio.run(main())