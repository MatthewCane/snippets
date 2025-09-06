from pathlib import Path
from time import sleep

from loguru import logger as log
from tqdm import tqdm

if __name__ == "__main__":
    log.remove()
    log.add(lambda x: tqdm.write(x, end=""), level="INFO", format="> {message}")

    log.info("Starting processing with progress bar")

    files = list(Path(".").iterdir())

    for i in tqdm(files, desc="Processing"):
        sleep(0.1)
        log.info(f"Found file {i}")

    log.success("Processing completed")
