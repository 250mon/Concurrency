import asyncio
from ch05_util import connect_pg
import logging


async def main():
    connection = await connect_pg()
    async with connection.transaction():
        await connection.execute("INSERT INTO brand VALUES(DEFAULT, "
                                 "'my_new_brand')")
        try:
            async with connection.transaction():
                await connection.execute("INSERT INTO product_color"
                                         "VALUES(1, 'black')")

        except Exception as ex:
            logging.warning('Ignoring error inserting product color',
                            exc_info=ex)
    await connection.close()

asyncio.run(main())
