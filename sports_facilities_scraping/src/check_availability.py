from time import sleep

import schedule
from availability import get_available_courts
from notification import notify_availablity
from weather import get_weather

SLEEP_WAIT = 5


def check_availability():
    print("Running task...")
    available_courts = get_available_courts()
    if available_courts.__len__() > 0:
        weather_info = get_weather()
        notify_availablity(available_courts, weather_info)
    print("Task completed.")


def check_availability_at(time: str):
    schedule.every().day.at(time).do(get_available_courts)


def main():
    check_availability()
    check_availability_at("07:55")
    check_availability_at("09:55")
    check_availability_at("11:55")
    check_availability_at("13:55")
    check_availability_at("15:55")
    check_availability_at("17:55")
    check_availability_at("19:55")
    check_availability_at("21:55")
    while True:
        schedule.run_pending()
        sleep(SLEEP_WAIT)


main()
