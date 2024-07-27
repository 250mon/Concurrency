import asyncio

from util.delay_functions import delay

"""
'await'
This keyword causes the coroutine following it to be run,
unlike calling a coroutine directly, which produces a coroutine
obj.

The await expression will also pause the coroutine where it
is contained in until the coroutine we awaited finishes and
returns a result
---

It is important to know that we should usually use an
'await' keyword on our tasks at some point in our application.

if we did not use await, our task would be scheduled to run, 
but it would almost immediately be stopped and cleaned when
asyncio.run shut down the event loop. 

Using await on our tasks in our application 
also has implications for how exceptions are handled.
"""


async def main():
    # await
    sleep_for_three = asyncio.create_task(delay(3))
    print(type(sleep_for_three))
    result = await sleep_for_three
    print(result)

    # no await
    sleep_for_another_three = asyncio.create_task(delay(3))
    print(type(sleep_for_another_three))


asyncio.run(main())

