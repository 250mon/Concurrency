import asyncio
from util import delay

"""
It is worth noting that the results for each awaitable we pass in may not complete in
a deterministic order. For example, if we pass coroutines a and b to gather in that
order, b may complete before a. A nice feature of gather is that, regardless of when
our awaitables complete, we are guaranteed the results will be returned in the order
we passed them in
"""
async def main():
    results = await asyncio.gather(delay(3), delay(1))
    print(results)

asyncio.run(main())