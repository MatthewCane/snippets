from random import random
from time import perf_counter, sleep

from tqdm import tqdm


def task():
    sleep(random())


"""
Simple bar format with shaded blocks
"""
for _ in tqdm(
    range(50), bar_format="{bar}", ascii="░█", ncols=40, colour="green", leave=False
):
    s = perf_counter()
    task()
    tqdm.write(f"Processed in {perf_counter() - s:.2f}s")

print("Done")
