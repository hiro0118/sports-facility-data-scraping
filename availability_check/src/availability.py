# coding: UTF-8

from time import sleep

import element
from court import Court
from element import (find_elements, get_text, pause_and_click,
                     weekend_element_on)
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

SELENIUM_ADDRESS = 'http://localhost:4444/wd/hub'
MULTIFUNCTIONAL_MAIN_PAGE = "https://yoyaku.sports.metro.tokyo.lg.jp/user/view/user/homeIndex.html"

WAIT_SEC = 1
WAIT_INITIAL = 2

PARKS_TO_CHECK: list[str] = [
    '日比谷公園',
    '芝公園',
    '猿江恩賜公園',
    '篠崎公園',
    '亀戸中央公園',
    '木場公園',
    '東綾瀬公園',
    '大島小松川公園',
    '大井ふ頭海浜公園',
    '有明テニスの森公園'
]


def get_available_courts() -> list[Court]:

    driver = create_driver()

    try:
        sleep(WAIT_INITIAL)
        driver.get(MULTIFUNCTIONAL_MAIN_PAGE)

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

    finally:
        driver.quit()

    return available_courts


def create_driver() -> webdriver.Remote:
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Remote(
        command_executor=SELENIUM_ADDRESS, options=options)
    return driver


def get_available_courts_from_page(driver: webdriver.Remote) -> list[Court]:
    result: list[Court] = []

    # For each weekend
    weekend_dates = get_weekend_dates(driver)
    for weekend_date in weekend_dates:

        # Go to the next weekend day.
        pause_and_click(driver, weekend_element_on(weekend_date))
        date_info = get_formatted_date(driver)  # yyyy/mm/dd
        print(f"Checking {date_info}...")

        # For each park tables page.
        next_park_tables_page_exists = True
        while next_park_tables_page_exists:

            # For each park table.
            park_tables = find_elements(driver, element.PARK_TABLE)
            for park_table in park_tables:

                # If the park is not in the list, skip it.
                park_name = get_text(park_table, element.PARK_NAME)
                if not need_to_check_park(park_name):
                    continue

                # Get available times and register them to the result.
                available_times: list[str] = get_available_times(park_table)
                for available_time in available_times:
                    new_court = Court(date_info, available_time, park_name)
                    result.append(new_court)
                    print(new_court)

            # Go to the next set of park tables if it exists.
            try:
                pause_and_click(driver, element.NEXT_FIVE)
            except Exception:
                next_park_tables_page_exists = False

    return result


def get_weekend_dates(driver: webdriver.Remote) -> list[str]:
    result: list[str] = []
    active_weekends = find_elements(driver, element.ACTIVE_WEEKEND)
    for active_weekend in active_weekends:
        result.append(active_weekend.text)
    return result


def get_formatted_date(driver: webdriver.Remote):
    y = get_text(driver, element.YEAR)
    m = get_text(driver, element.MONTH)
    d = get_text(driver, element.DATE)
    if m.__len__() == 1:
        m = '0' + m
    if d.__len__() == 1:
        d = '0' + d
    return f'{y}/{m}/{d}'


def need_to_check_park(park: str) -> bool:
    for park_to_check in PARKS_TO_CHECK:
        if park_to_check in park:
            return True
    return False


def get_available_times(park_table: WebElement) -> list[str]:

    # Check available column IDs.
    availablity_cells = find_elements(park_table, element.AVAILABILITY_CELL)
    available_cell_ids: list[int] = []
    for idx, availability_cell in enumerate(availablity_cells):
        if availability_cell.text != '0':
            available_cell_ids.append(idx)

    # Return empty here if none are found.
    if len(available_cell_ids) == 0:
        return []

    # Get available times based on the IDs.
    result: list[str] = []
    times = find_elements(park_table, element.TIME)
    for available_cell_id in available_cell_ids:
        available_time = times[available_cell_id].text
        if available_time.__len__() == 4:
            available_time = '0' + available_time
        result.append(available_time)

    return result
