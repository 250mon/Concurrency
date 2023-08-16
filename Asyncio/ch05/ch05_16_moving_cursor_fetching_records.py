import asyncio
from ch05_util import connect_pg


async def main():
    connection = await connect_pg()
    async with connection.transaction():
        query = "SELECT product_id, product_name FROM product"
        cursor = await connection.cursor(query)
        # move the cursor forward 500 records
        await cursor.forward(500)
        # get the next 100 records
        products = await cursor.fetch(100)
        for product in products:
            print(product)

    await connection.close()

asyncio.run(main())
