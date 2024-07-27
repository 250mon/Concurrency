import asyncio

from util.db_handler import connect_pg


async def main():
    connection = await connect_pg()
    version = connection.get_server_version()
    print(f"Connected! Postgres version is {version}")
    await connection.close()


asyncio.run(main())

