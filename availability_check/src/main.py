import os
from time import sleep

from availability import get_available_courts
from notification import notify_availablity, notify_error
from scheduler import schedule_task
from utils import log
from weather import get_weather

MODE_KEY = 'MODE'
SINGLE_MODE = 'single'
SCHEDULED_MODE = 'scheduled'
INITAL_WAIT = 10

SCHEDULE_TIMES = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00",
                  "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00"]


def main():
    mode = os.environ.get(MODE_KEY)
    if mode == SCHEDULED_MODE:
        log("Starting in scheduled mode.")
        schedule_task(check_availability, SCHEDULE_TIMES)
    elif mode == SINGLE_MODE:
        log("Starting in single mode.")
        selenium_address = 'http://selenium-chrome:4444/wd/hub'
        check_availability(selenium_address, False)
    else:
        log("Starting in cloud mode.")
        selenium_address = 'http://localhost:4444/wd/hub'
        check_availability(selenium_address, True)


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
