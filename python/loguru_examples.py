import sys
from pathlib import Path

from loguru import logger as log

"""
https://www.dash0.com/guides/python-logging-with-loguru#redirecting-standard-logging-into-loguru
"""


def func_a(i):
    log.info("Running func_a", iteration=i)


def func_b(i):
    log.debug(f"Running func_b for iteration {i}")


def func_c():
    log.debug("Running func_c")
    try:
        1 / 0
    except ZeroDivisionError:
        log.error("Error in func_c")


@log.catch()
def func_d():
    log.debug("Running func_d")
    raise ValueError("An error occurred in func_d")


def func_e():
    log.debug("Running func_e")
    with log.catch(reraise=True):
        raise RuntimeError("An error occurred in func_e")


def main():
    log.info("Starting main loop")
    for i in range(5):
        func_a(i)
        func_b(i)
        func_c()
        try:
            func_d()
        except ValueError as e:
            log.error(f"Caught an exception from func_d: {e}")

    log.success("Main loop completed")


def configure_logging():
    # Remove all existing handlers
    log.remove()

    # Add a file handler for info logs in jsonl format
    log.add(Path("log.jsonl"), level="INFO", serialize=True, rotation="1 MB")

    # Add a standard output handler for debug logs
    log.add(sys.stdout, level="DEBUG")

    # Add a file handler for error logs in jsonl format with rotation
    log.add(
        Path("error.jsonl"),
        level="ERROR",
        serialize=True,
        rotation="500 KB",
        filter=lambda record: record["level"].no >= 40,  # Only log ERROR and above
    )


if __name__ == "__main__":
    configure_logging()
    main()
