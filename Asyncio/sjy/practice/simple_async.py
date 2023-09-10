import asyncio


async def check_version():
    version = await look_up_version()
    print(version)


async def look_up_version():
    return 12


async def main():
    await check_version()
    print('end process')


asyncio.run(main())
