# coding: UTF-8

from time import sleep

import config
import element
from element import (create_park_element, find_element, find_element_below,
                     find_elements, get_text, pause_and_click)
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

SELENIUM_URL = "http://localhost:4445/wd/hub"
SIMPLIFIED_MAIN_PAGE = "https://yoyaku.sports.metro.tokyo.lg.jp/web/"

WAIT_SEC = 1
WAIT_SEC_FOR_LOGIN = 4


def get_application_status() -> list:

    driver = create_driver()
    result = []

    try:
        driver.get(SIMPLIFIED_MAIN_PAGE)

        log_in(driver)
        go_to_tennis_page(driver)

        # Check each park.
        print("Checking application_status...")
        for park_id in get_park_id_list(driver):

            # Go to the park page.
            pause_and_click(driver, create_park_element(park_id))
            park_name = get_text(driver, element.PARK_NAME)
            print(f"Checking {park_name}...")

            # Check each week.
            next_week_exists = True
            while next_week_exists:
                # Check all the cells in the week.
                cells = find_elements(driver, element.CELL)
                for cell in cells:
                    cell_data = get_cell_data(cell, park_name)
                    result.append(cell_data)

                # Go to the next week if it exists.
                next_week_button = find_next_week_button(driver)
                if next_week_button is not None:
                    sleep(WAIT_SEC)
                    next_week_button.click()
                else:
                    next_week_exists = False

            # Go back to the park selection page.
            pause_and_click(driver, element.GO_BACK_TO_PARK_LIST)
    finally:
        driver.quit()

    return result


def create_driver() -> webdriver.Remote:
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Remote(
        command_executor=SELENIUM_URL, options=options)
    return driver


def log_in(driver: webdriver.Remote):
    print("logging in...")
    # Go to login page
    driver.switch_to.frame("pawae1002")
    pause_and_click(driver, element.GO_TO_LOGIN)
    # Input login info
    find_element(driver, element.ID_FIELD).send_keys(config.ID)
    find_element(driver, element.PASS_FIELD).send_keys(config.PASSWORD)
    # Click log-in button
    pause_and_click(driver, element.LOGIN_BUTTON, WAIT_SEC_FOR_LOGIN)


def go_to_tennis_page(driver: webdriver.Remote):
    print("Going to tennis page...")
    pause_and_click(driver, element.GO_TO_RAFFLE)
    pause_and_click(driver, element.GO_TO_SPORT_TYPES)
    pause_and_click(driver, element.GO_TO_TENNIS)


def get_park_id_list(driver: webdriver.Remote):
    park_id_list = []
    parks = find_elements(driver, element.PARK_IN_LIST)
    for park in parks:
        href = park.get_attribute("href")
        park_id_list.append(href[-11:-4])
    return park_id_list


def get_cell_data(cell: WebElement, park_name: str):

    courts = 0
    applications = 0
    num_text = cell.text
    if (num_text is not None):
        nums = num_text.split("/")
        courts = nums[0]
        applications = nums[1]

    href_split = cell.get_attribute("href").split(",%20")
    return {
        "date": href_split[len(href_split) - 5],
        "park": park_name,
        "time": href_split[len(href_split) - 4] + '-' + href_split[len(href_split) - 3],
        "courts": courts,
        "applications": applications,
        "ratio": float(applications) / float(courts)
    }


def find_next_week_button(driver: webdriver.Remote):
    week_buttons = find_elements(driver, element.WEEK_BUTTON)
    for week_button in week_buttons:
        try:
            return find_element_below(week_button, element.GO_TO_NEXT_WEEK)
        except NoSuchElementException:
            continue
    # Next week button doesn't exist.
    return None
