import asyncio

import asyncpg
from asyncpg.transaction import Transaction

from util.db_handler import connect_pg


async def main():
    connection = await connect_pg()

    # create a transaction instance
    transaction: Transaction = connection.transaction()
    await transaction.start()
    try:
        await connection.execute("INSERT INTO brand " "VALUES(DEFAULT, 'brand_1')")
        await connection.execute("INSERT INTO brand " "VALUES(DEFAULT, 'brand_2')")
    except asyncpg.PostgresError:
        # if there was an exception, roll back
        print("Errors, rolling back transaction!")
        await transaction.rollback()
    else:
        # if there was an exception, commit
        print("No errors, committing transaction!")
        await transaction.commit()

    query = """SELECT brand_name FROM brand
                WHERE brand_name LIKE 'brand%'"""
    brands = await connection.fetch(query)
    print(brands)

    await connection.close()


asyncio.run(main())
