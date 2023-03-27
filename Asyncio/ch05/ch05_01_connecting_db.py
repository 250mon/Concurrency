import asyncpg
import asyncio
from ch05_util import get_options


async def main():
    options = get_options("db_settings")
    passwd = options['password']
    connection = await asyncpg.connect(host='127.0.0.1',
                                       port=5432,
                                       user='postgres',
                                       database='postgres',
                                       password=passwd)
    version = connection.get_server_version()
    print(f'Connected! Postgres version is {version}')
    await connection.close()

asyncio.run(main())