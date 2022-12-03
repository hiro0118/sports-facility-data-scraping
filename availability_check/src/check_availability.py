from datetime import datetime
from time import sleep

import schedule
from availability import get_available_courts
from weather import get_weather

from notification import notify_availablity

INITAL_WAIT = 10
SLEEP_WAIT = 5


def main():

    print("Waiting for selenium service to be ready...")
    sleep(INITAL_WAIT)

    # UTC
    check_availability()
    check_availability_at("07:55")
    check_availability_at("08:55")
    check_availability_at("09:55")
    check_availability_at("10:55")
    check_availability_at("11:55")
    check_availability_at("12:55")
    check_availability_at("13:55")
    check_availability_at("14:55")
    check_availability_at("15:55")
    check_availability_at("16:55")
    check_availability_at("17:55")
    check_availability_at("18:55")
    check_availability_at("19:55")
    check_availability_at("20:55")
    check_availability_at("21:55")

    while True:
        schedule.run_pending()
        sleep(SLEEP_WAIT)


def check_availability_at(time: str):
    schedule.every().day.at(time).do(check_availability)


def check_availability():
    print(get_current_datetime() + " Running task...")
    available_courts = get_available_courts()
    if available_courts.__len__() > 0:
        weather_info = get_weather()
        notify_availablity(available_courts, weather_info)
    print(get_current_datetime() + " Task completed.")


def get_current_datetime() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M")


if __name__ == "__main__":
    main()
