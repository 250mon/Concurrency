import asyncio
import logging

from util.db_handler import connect_pg

"""
transaction consists of one or more SQL statements that are
executed as one atomic unit. (ACID)
if no error, it commits the statements to the DB.
if any error, it rolls back the statements
"""


async def main():
    connection = await connect_pg()
    try:
        async with connection.transaction():
            insert_brand = "INSERT INTO brand VALUES(9999, 'big_brand')"
            await connection.execute(insert_brand)
            await connection.execute(insert_brand)
    except Exception:
        logging.exception("Error while running transaction")
    finally:
        query = """SELECT brand_name FROM brand
                    WHERE brand_name LIKE 'big_%'"""
        brands = await connection.fetch(query)
        print(f"Query result was: {brands}")

        await connection.close()


asyncio.run(main())
