import os
from time import sleep

from availability import get_available_courts
from notification import notify_availablity, notify_error
from scheduler import schedule_task
from utils import log
from weather import get_weather

MODE_KEY = 'MODE'
TEST_MODE = 'test'
SCHEDULED_MODE = 'scheduled'
CLOUD_MODE = 'cloud'
MODES = [TEST_MODE, SCHEDULED_MODE, CLOUD_MODE]

INITAL_WAIT = 10

SCHEDULE_TIMES = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00",
                  "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00"]

SELENIUM_IN_DOCKER_NW = 'http://selenium-chrome:4444/wd/hub'
SELENIUM_IN_LOCALHOST = 'http://localhost:4444/wd/hub'


def main():
    mode = os.environ.get(MODE_KEY)
    mdoe = get_mode()
    log(f"Starting task in {mode} mode.")
    if mode == SCHEDULED_MODE:
        schedule_task(SCHEDULE_TIMES, check_availability,
                      SELENIUM_IN_DOCKER_NW, True)
    elif mode == TEST_MODE:
        check_availability(SELENIUM_IN_DOCKER_NW, False)
    elif mode == CLOUD_MODE:
        check_availability(SELENIUM_IN_LOCALHOST, True)
    else:
        log(f"Mode, {mode}, was not recognized. Terminating the task.")


def get_mode() -> str:
    mode = os.environ.get(MODE_KEY)
    if mode not in MODES:
        mode = CLOUD_MODE
    return mode


def check_availability(selenium_address: str, broad: bool):
    sleep(INITAL_WAIT)
    log("Starting task...")
    try:
        available_courts = get_available_courts(selenium_address)
        if available_courts.__len__() > 0:
            weather_info = get_weather()
            notify_availablity(available_courts, weather_info, broad)
        log("Task completed.")
    except Exception as e:
        log("Error occurred.")
        print(e)
        notify_error(e)


if __name__ == "__main__":
    main()
