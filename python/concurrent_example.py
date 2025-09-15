from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from math import sqrt
from random import random
from time import sleep
from typing import Any

type number = float | int


def do_task(t: number) -> number:
    print(f"Starting sleep for {t:.2f}s")
    sleep(t)
    print(f"Done sleeping for {t:.2f}s")
    if random() > 0.5:
        raise ValueError("Failed")
    return sqrt(t)


@dataclass
class Result:
    args: Any
    result: Any | None = None
    err: Exception | None = None


def do_task_result(t: number) -> Result:
    try:
        print(f"Starting sleep for {t:.2f}s")
        sleep(t)
        print(f"Done sleeping for {t:.2f}s")
        if random() > 0.5:
            raise ValueError("Failed")
        return Result(t, sqrt(t))
    except Exception as e:
        return Result(t, None, e)


def full_example(tasks: list[float]) -> None:
    """
    Example with proper error handling. Only results that did not throw an error
    will be included in the results list.

    When running this example, notice that the sleep durations are randomly distributed
    when the execution starts but the done messages come through in order of shortest
    to longest, indicating that the tasks are happening in seperate threads and the
    tasks come back in the order in which they complete.
    """
    with ThreadPoolExecutor() as exe:
        # Submit the tasks and get Future objects for each one
        futures = [exe.submit(do_task, t) for t in tasks]

        results = []
        # As each one completes, it yeilds
        for future in as_completed(futures):
            try:
                # If there is a result, capture it
                results.append(future.result())
            except Exception as e:
                # If a task has an exception, handle it
                print("A task generated an exception:", e)

        print("\nResults:", results)


def one_line_example(tasks: list[float]) -> None:
    """
    A much more concise way of doing it is use the map function, but any
    exceptions thrown by the task will be thrown at the end of the map process
    and are not able to be caught individually. This is fine for simple stuff.

    map also returns the results in the order in which they are called, not
    in the order in which they are completed.
    """

    with ThreadPoolExecutor() as exe:
        results = list(exe.map(do_task, tasks))

    print("\nResults:", results)


def one_line_example_with_result(tasks) -> None:
    with ThreadPoolExecutor() as exe:
        results = list(exe.map(do_task_result, tasks))

    for res in results:
        print(f"sqrt({res.args})={res.result if res.result else res.err}")


if __name__ == "__main__":
    tasks = [random() * 10 for _ in range(10)]
    # full_example(tasks)
    # one_line_example(tasks)
    one_line_example_with_result(tasks)
