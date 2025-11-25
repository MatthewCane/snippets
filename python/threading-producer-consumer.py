from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from queue import Queue, ShutDown
from random import randint
from signal import SIGTERM, signal
from sys import stdout
from time import sleep

from loguru import logger as log

log.remove()
log.add(stdout, level="INFO", format="<lvl>{level}</lvl> - {function}::{message}")

"""
Producer-consumer example using threading and Queue.

The producer fetches tasks at the start of every minute and adds them to a shared queue.
The consumer processes tasks from the queue as they are added.
On reception of a SIGTERM signal, the producer stops fetching new tasks and waits for the queue to empty before shutting down.
"""


def handle_sigterm(*args):
    log.info("Received SIGTERM, gracefully exiting.")
    global shutdown
    shutdown = True
    count = 0
    while count < GRACEFUL_SHUTDOWN_PERIOD:
        if queue.qsize() == 0:
            break
        count += GRACEFUL_SHUTDOWN_PERIOD / 10
        sleep(GRACEFUL_SHUTDOWN_PERIOD / 10)
    queue.shutdown()


def get_wait_sec() -> float:
    """Return the number of seconds to wait before the next minute"""
    now = datetime.now()
    future = datetime(now.year, now.month, now.day, now.hour, now.minute) + timedelta(
        minutes=1
    )
    return (future - now).total_seconds()


def sleep_thread(seconds: float):
    """Sleep for the given number of seconds, handling on shutdown signal."""
    global shutdown
    end_time = datetime.now().timestamp() + seconds
    while datetime.now().timestamp() < end_time:
        if shutdown:
            break
        sleep(0.1)


def producer(queue: Queue):
    log.info("Running")
    global shutdown
    while True:
        if shutdown:
            log.info("Shutdown signal received, exiting.")
            break
        log.info(f"Fetching tasks for {datetime.now().strftime('%H:%M:%S')}")
        sleep(randint(1, 3))
        tasks = [randint(1, 3) for i in range(randint(1, 5))]
        log.info(f"Fetched {len(tasks)} tasks")
        for t in tasks:
            try:
                queue.put(t)
            except ShutDown:
                continue
            log.info(f"Added task {t} to queue")
        sleep_thread(get_wait_sec())


def consumer(queue: Queue):
    log.info("Running")
    # consume items
    while True:
        try:
            item = queue.get()
        except ShutDown:
            log.info("Shutdown signal received, exiting.")
            break
        log.info(f"Processing item {item}")
        sleep(item)
        log.info(f"Processed item {item}")
        log.info(f"Queue size: {queue.qsize()}")


shutdown = False
GRACEFUL_SHUTDOWN_PERIOD = 1
queue = Queue()


signal(SIGTERM, handle_sigterm)

log.info("Starting main thread.")
with ThreadPoolExecutor() as executor:
    executor.submit(consumer, queue)
    executor.submit(producer, queue)

log.info("Exiting main thread.")
