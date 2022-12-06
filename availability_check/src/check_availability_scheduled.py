from time import sleep

import schedule
from check_availability import check_availability

INITAL_WAIT = 10
SLEEP_WAIT = 5


def check_availability_scheduled():
    check_availability_at("08:00")
    check_availability_at("09:00")
    check_availability_at("10:00")
    check_availability_at("11:00")
    check_availability_at("12:00")
    check_availability_at("13:00")
    check_availability_at("14:00")
    check_availability_at("15:00")
    check_availability_at("16:00")
    check_availability_at("17:00")
    check_availability_at("18:00")
    check_availability_at("19:00")
    check_availability_at("20:00")
    check_availability_at("21:00")
    check_availability_at("22:00")
    while True:
        schedule.run_pending()
        sleep(SLEEP_WAIT)


def check_availability_at(time: str):
    schedule.every().day.at(time).do(check_availability)


if __name__ == "__main__":
    check_availability_scheduled()
