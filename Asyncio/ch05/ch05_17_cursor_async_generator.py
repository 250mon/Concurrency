import asyncio

from util.db_handler import connect_pg


async def take(generator, to_take: int):
    item_count = 0
    async for item in generator:
        if item_count > to_take - 1:
            return
        item_count += 1
        yield item


async def main():
    connection = await connect_pg()
    async with connection.transaction():
        query = "SELECT product_id, product_name from product"
        product_generator = connection.cursor(query)
        async for product in take(product_generator, 5):
            print(product)

        print("Got the first five products!")

    await connection.close()


asyncio.run(main())

