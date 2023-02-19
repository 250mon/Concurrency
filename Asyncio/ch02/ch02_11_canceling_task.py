import asyncio
from asyncio import CancelledError
from util import delay

'''
Something important to note about cancellation is that a
CancelledError can only be thrown from an await statement.

This means that if we call cancel on a task when it is executing 
plain Python code, that code will run until completion until we
hit the next await statement (if one exists) and a CancelledError
can be raised

Calling cancel won't magically stop the task in its tracks;
it will only stop the task if you're currently at an await point
or its next await point.

'''
async def main():
    long_task = asyncio.create_task(delay(5))
    seconds_elapsed = 0

    while not long_task.done():
        print('Task not finished, checking again in a second.')
        await asyncio.sleep(1)
        print(f'long_task.done?? {long_task.done()}')
        seconds_elapsed = seconds_elapsed + 1
        if seconds_elapsed == 2:
            print("Canceling the long task ...")
            long_task.cancel()

    try:
        await long_task
    except CancelledError:
        print('Our task was cancelled')

asyncio.run(main())