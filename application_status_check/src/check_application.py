from datetime import datetime
from time import sleep

from appilcation import get_application_status
from export import export_json

INITAL_WAIT = 5
OUTPUT_DIR = "output"


def check_application():
    sleep(INITAL_WAIT)
    print(get_current_datetime() + " Starting task...")
    try:
        result = get_application_status()
        if (len(result) != 0):
            export_json(result, OUTPUT_DIR)
        print(get_current_datetime() + " Task completed.")
    except Exception as e:
        print("Error occurred!")
        print(e)


def get_current_datetime() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M")


if __name__ == "__main__":
    check_application()
