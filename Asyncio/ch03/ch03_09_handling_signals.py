import asyncio, signal
from asyncio import AbstractEventLoop
from typing import Set
from util import delay

# SIGINT does not work on Windows!!!!!

def cancel_tasks():
    print('Got a SIGINT!')
    tasks: Set[asyncio.Task] = asyncio.all_tasks()
    print(f'Cancelling {len(tasks)} tasks(s).')
    [task.cancel() for task in tasks]

async def main():
    loop: AbstractEventLoop = asyncio.get_running_loop()
    # 'add_signal_handler' takes only a plain python function
    # as a signal handler meaning that we can't run any 'await'
    # statements inside of it
    loop.add_signal_handler(signal.SIGINT, cancel_tasks)

    await delay(10)

asyncio.run(main())
