from time import sleep

import schedule

LOOP_INTERVAL = 5


def schedule_task(times: list[str], task, *args):
    for time in times:
        schedule.every().day.at(time).do(task, args)
        print(f"Task scheduled at {time}.")
    while True:
        schedule.run_pending()
        sleep(LOOP_INTERVAL)
