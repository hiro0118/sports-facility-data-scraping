from datetime import datetime
from time import sleep

from appilcation import get_application_status
from export import export_json
from utils import log

INITAL_WAIT = 10
OUTPUT_DIR = "output"


def main():
    sleep(INITAL_WAIT)
    log("Starting task...")
    try:
        result = get_application_status()
        if (len(result) != 0):
            export_json(result, OUTPUT_DIR)
        log("Task completed.")
    except Exception as e:
        log("Error occurred!")
        print(e)


if __name__ == "__main__":
    main()
