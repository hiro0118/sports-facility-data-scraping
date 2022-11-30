# coding: UTF-8

from time import sleep

import element
import urls
from court import Court
from element import find_elements, get_text, pause_and_click
from selenium import webdriver

#SELENIUM = 'http://localhost:4444/wd/hub'
SELENIUM = 'http://selenium-chrome:4444/wd/hub'

WAIT_SEC = 1
WAIT_INITIAL = 2


def create_driver() -> webdriver.Remote:
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Remote(
        command_executor=SELENIUM, options=options)
    return driver


def get_formatted_date(driver: webdriver.Remote):
    y = get_text(driver, element.YEAR)
    m = get_text(driver, element.MONTH)
    d = get_text(driver, element.DATE)
    if m.__len__() == 1:
        m = '0' + m
    if d.__len__() == 1:
        d = '0' + d
    return f'{y}/{m}/{d}'


def get_available_courts_from_page(driver: webdriver.Remote) -> list[Court]:
    available_courts: list[Court] = []

    # For each weekend
    active_weekends_num = len(find_elements(driver, element.ACTIVE_WEEKEND))
    weekend_idx: int = 0
    while weekend_idx < active_weekends_num:

        active_weekends = find_elements(driver, element.ACTIVE_WEEKEND)
        active_weekends[weekend_idx].click()

        date = get_formatted_date(driver)

        # For each park tables page.
        next_park_tables_page_exists = True
        while next_park_tables_page_exists:

            # For each park table.
            park_tables = find_elements(driver, element.PARK_TABLE)
            for park_table in park_tables:
                park_name = get_text(park_table, element.PARK_NAME)
                availablity_cells = find_elements(
                    park_table, element.AVAILABILITY_CELL)

                # Check available columns.
                available_cell_ids: list[int] = []
                for idx, availability_cell in enumerate(availablity_cells):
                    if availability_cell.text != '0':
                        available_cell_ids.append(idx)

                # Get date/time from the colum IDs.
                if len(available_cell_ids) > 0:
                    times = find_elements(park_table, element.TIME)
                    for available_cell_id in available_cell_ids:
                        time = times[available_cell_id].text
                        if time.__len__() == 4:
                            time = '0' + time
                        new_avaiable_court = Court(date, time, park_name)
                        available_courts.append(new_avaiable_court)
                        print(new_avaiable_court)

            # Go to the next set of park tables. Leave the loop if it's the last page.
            try:
                pause_and_click(driver, element.NEXT_FIVE)
            except Exception:
                next_park_tables_page_exists = False

        weekend_idx += 1

    return available_courts


def get_available_courts() -> list[Court]:
    driver = create_driver()

    sleep(WAIT_INITIAL)
    driver.get(urls.MULTIFUNCTIONAL_MAIN)

    # Go to the availability page
    pause_and_click(driver, element.PURPOSE_SEARCH)
    pause_and_click(driver, element.TENNIS_HARD)
    pause_and_click(driver, element.TENNIS_OMNI)
    pause_and_click(driver, element.AVAILABILITY_SEARCH)

    # Check current month
    available_courts: list[Court] = get_available_courts_from_page(driver)

    # Check next month
    pause_and_click(driver, element.NEXT_MONTH)
    available_courts.extend(get_available_courts_from_page(driver))

    driver.close()

    return available_courts
