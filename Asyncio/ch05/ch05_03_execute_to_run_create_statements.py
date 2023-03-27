import asyncpg
import asyncio
from ch05_util import get_options
from ch05_product_schema import (
    CREATE_BRAND_TABLE,
    CREATE_PRODUCT_TABLE,
    CREATE_SKU_TABLE,
    COLOR_INSERT,
    SIZE_INSERT,
    CREATE_PRODUCT_SIZE_TABLE,
    CREATE_PRODUCT_COLOR_TABLE
)


async def main():
    options = get_options("db_settings")
    passwd = options['password']
    connection = await asyncpg.connect(host='127.0.0.1',
                                       port=5432,
                                       user='postgres',
                                       database='postgres',
                                       password=passwd)

    statements = [CREATE_BRAND_TABLE,
                  CREATE_PRODUCT_TABLE,
                  CREATE_PRODUCT_COLOR_TABLE,
                  CREATE_PRODUCT_SIZE_TABLE,
                  CREATE_SKU_TABLE,
                  SIZE_INSERT,
                  COLOR_INSERT]
    print('Creating the product dabatabse...')
    for statement in statements:
        status = await connection.execute(statement)
        print(status)
    print('Finished creating the product database')
    await connection.close()

asyncio.run(main())