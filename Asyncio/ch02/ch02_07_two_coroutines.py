import asyncio

from util.delay_functions import delay

"""
Think of a coroutine like a regular Python function but with the superpower that it
can pause its execution when it encounters an operation that could take a while to
complete. When that long-running operation is complete, we can wake our
paused coroutine and finish executing any other code in that coroutine. While a
paused coroutine is waiting for the operation it paused for to finish, we can run other
code.

We use 'async def' to mark a function as a coroutine.

To run a coroutine, we need to explicitly run it on an event loop.
There is a convenient default event loop which is asyncio.run().
"""


# 2 coroutins behaves as if it were sequential
# To run two coroutins concurrently, we need tasks
async def add_one(number: int) -> int:
    return number + 1


async def hello_world_message() -> str:
    await delay(1)
    return "Hello World"


async def main() -> None:
    message = await hello_world_message()
    one_plus_one = await add_one(1)
    print(one_plus_one)
    print(message)


asyncio.run(main())
