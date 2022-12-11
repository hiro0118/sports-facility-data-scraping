from datetime import datetime
from time import sleep

import schedule
from availability import get_available_courts
from notification import notify_availablity, notify_error
from weather import get_weather

INITAL_WAIT = 5
LOOP_INTERVAL = 5

SCHEDULE_TIMES = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00",
                  "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00"]


def check_availability():
    sleep(INITAL_WAIT)
    print(get_current_datetime() + " Starting task...")
    try:
        available_courts = get_available_courts()
        if available_courts.__len__() > 0:
            weather_info = get_weather()
            notify_availablity(available_courts, weather_info)
        print(get_current_datetime() + " Task completed.")
    except Exception as e:
        print(e)
        notify_error(e)


def check_availability_scheduled():
    for time in SCHEDULE_TIMES:
        schedule.every().day.at(time).do(check_availability)
        print(f"Task scheduled at {time}.")
    while True:
        schedule.run_pending()
        sleep(LOOP_INTERVAL)


def get_current_datetime() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M")
