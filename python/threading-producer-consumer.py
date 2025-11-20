from datetime import datetime, timedelta
from queue import Queue
from random import randint
from sys import stdout
from threading import Thread
from time import sleep

from loguru import logger as log

log.remove()
log.add(stdout, level="INFO", format="<lvl>{level}</lvl> - {function}::{message}")

"""
Producer-consumer example using threading and Queue.

The producer fetches tasks at the start of every minute and adds them to a shared queue.
The consumer processes tasks from the queue as they become available.
"""


def get_wait_sec() -> float:
    """Return the number of seconds to wait before the next minute"""
    now = datetime.now()
    future = datetime(now.year, now.month, now.day, now.hour, now.minute) + timedelta(
        minutes=1
    )
    return (future - now).total_seconds()


def producer(queue: Queue):
    log.info("Running")
    while True:
        log.info(f"Fetching tasks for {datetime.now().strftime('%H:%M:%S')}")
        sleep(randint(1, 3))
        tasks = [randint(1, 3) for i in range(randint(1, 5))]
        log.info(f"Fetched {len(tasks)} tasks")
        for t in tasks:
            queue.put(t)
            log.info(f"Added task {t} to queue")
        sleep(get_wait_sec())


def consumer(queue: Queue):
    log.info("Running")
    # consume items
    while True:
        item = queue.get()
        log.info(f"Processing item {item}")
        sleep(item)
        log.info(f"Processed item {item}")
        log.info(f"Queue size: {queue.qsize()}")


# create the shared queue
queue = Queue()
# start the consumer
consumer_t = Thread(target=consumer, args=(queue,))
consumer_t.start()

# start the producer
producer_t = Thread(target=producer, args=(queue,))
producer_t.start()

# wait for all threads to finish
producer_t.join()
consumer_t.join()
