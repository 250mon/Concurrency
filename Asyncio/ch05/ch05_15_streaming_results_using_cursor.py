import asyncio
from ch05_util import connect_pg


async def main():
    connection = await connect_pg()
    query = 'SELECT product_id, product_name FROM product'
    async with connection.transaction():
        async for product in connection.cursor(query):
            print(product)

    await connection.close()

asyncio.run(main())