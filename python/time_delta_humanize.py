from datetime import datetime, timedelta
from time import sleep

from humanize import precisedelta

# print("Natural delta:", naturaldelta(diff))
birthday = datetime(1993, 11, 1)

while True:
    now = datetime.now()
    diff: timedelta = now - birthday
    print("Precise delta:", precisedelta(diff), "\r", end="")
    sleep(0.1)
