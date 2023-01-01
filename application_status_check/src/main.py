import os
from time import sleep

from appilcation import get_application_status
from export import export_json, export_s3
from utils import log

INITAL_WAIT = 10
OUTPUT_DIR = "output"

MODE_KEY = 'MODE'
LOCAL_MODE = 'local'
CLOUD_MODE = 'cloud'
MODES = [LOCAL_MODE, CLOUD_MODE]


def main():
    mode = get_mode()
    log(f"Starting task in {mode} mode")
    sleep(INITAL_WAIT)
    try:
        result = get_application_status()
        if (len(result) != 0):
            export_result(mode, result)
        log("Task completed.")
    except Exception as e:
        log("Error occurred!")
        print(e)


def get_mode() -> str:
    mode = os.environ.get(MODE_KEY)
    if mode not in MODES:
        mode = CLOUD_MODE
    return mode


def export_result(mode: str, result: list) -> None:
    if (mode == LOCAL_MODE):
        export_json(result, OUTPUT_DIR)
    elif (mode == CLOUD_MODE):
        export_s3(result, OUTPUT_DIR)


if __name__ == "__main__":
    main()
