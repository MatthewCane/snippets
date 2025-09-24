from contextlib import contextmanager
from time import sleep


@contextmanager
def time_it(message: str = "Context took"):
    from time import perf_counter

    s = perf_counter()
    yield
    print(f"{message} {perf_counter() - s:.4f}s")


with time_it("Slept for"):
    sleep(1)
