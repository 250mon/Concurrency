import asyncio
from ch05_util import connect_pg
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
    connection = await connect_pg()
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