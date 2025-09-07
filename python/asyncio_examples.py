import asyncio
import time
from time import perf_counter

from tqdm.asyncio import tqdm


def blocking_action_with_write(wait: int | float = 0.2) -> None:
    """
    Simulate a blocking SDK call that cannot be awaited.
    Uses time.sleep to block the thread and also print
    a message with sync tqdm.write()
    """
    # Simulate variable network/IO delay
    time.sleep(wait)
    tqdm.write(f"Slept for {wait}s")


def blocking_action(wait: int | float = 0.2) -> None:
    """
    Simulate a blocking SDK call that cannot be awaited.
    Uses time.sleep to block the thread.
    """
    # Simulate variable network/IO delay
    time.sleep(wait)


async def main() -> None:
    items = [i for i in range(0, 5)]

    print("Running Syncronously:")
    started_at = perf_counter()
    for i in items:
        blocking_action(i)
    elapsed = perf_counter() - started_at
    print(f"Syncronous time: {elapsed:.2f}")

    """
    Async thread solution:

    1. Create a list of tasks using to_thread()
    2. Use gather with the unpacked list of tasks
    """
    print("Running Asyncronously:")
    started_at = perf_counter()
    tasks = [asyncio.to_thread(blocking_action, i) for i in items]
    await asyncio.gather(*tasks)
    elapsed = perf_counter() - started_at
    print(f"Asyncronous time: {elapsed:.2f}")

    """
    tqdm.async example:

    Import tqdm.asyncio.tqdm and use the tqdm.gather() method
    """
    print("Running asyncronously with tqdm:")
    tasks = [asyncio.to_thread(blocking_action_with_write, i) for i in items]
    await tqdm.gather(*tasks)
    elapsed = perf_counter() - started_at
    print(f"Asyncronous time with tqdm: {elapsed:.2f}")


if __name__ == "__main__":
    asyncio.run(main())
