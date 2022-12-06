from datetime import datetime
from time import sleep

from availability import get_available_courts
from weather import get_weather

from notification import notify_availablity

INITAL_WAIT = 5


def check_availability():
    sleep(INITAL_WAIT)
    print(get_current_datetime() + " Starting task...")
    available_courts = get_available_courts()
    if available_courts.__len__() > 0:
        weather_info = get_weather()
        notify_availablity(available_courts, weather_info)
    print(get_current_datetime() + " Task completed.")


def get_current_datetime() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M")


if __name__ == "__main__":
    check_availability()
