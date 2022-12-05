# coding: UTF-8

import csv
import json
from datetime import datetime
from time import sleep

import config
import element
from element import (create_park_element, find_element, find_elements,
                     get_text, pause_and_click)
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

SELENIUM_URL = "http://application-selenium:14444/wd/hub"
SIMPLIFIED_MAIN_PAGE = "https://yoyaku.sports.metro.tokyo.lg.jp/web/"

OUTPUT_PATH = "output/"

WAIT_SEC = 1
WAIT_SEC_FOR_LOGIN = 4


def get_application_status():
    driver = create_driver()
    driver.get(SIMPLIFIED_MAIN_PAGE)

    log_in(driver)
    go_to_tennis_page(driver)

    cell_data_list = []

    # Check each park.
    for park_id in get_park_id_list(driver):

        # Go to the park page.
        pause_and_click(driver, create_park_element(park_id))
        park_name = get_text(driver, element.PARK_NAME)

        # Check each week.
        next_week_exists = True
        while next_week_exists:
            # Check all the cells in the week.
            cells = find_elements(driver, element.CELL)
            for cell in cells:
                cell_data = get_cell_data(cell, park_name)
                cell_data_list.append(cell_data)

            # Go to the next week if it exists.
            next_week_button = find_next_week_button(driver)
            if next_week_button is not None:
                sleep(WAIT_SEC)
                next_week_button.click()
            else:
                next_week_exists = False

        # Go back to the park selection page.
        pause_and_click(driver, element.GO_BACK_TO_PARK_LIST)

    driver.quit()

    if (len(cell_data_list) != 0):
        export_csv_data(cell_data_list)
        export_json_data(cell_data_list)


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
    find_element(element.ID_FIELD).send_keys(config.ID)
    find_element(element.PASS_FIELD).send_keys(config.PASSWORD)
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

    href_split = cell.get_attribute("href").split(",%20")

    courts = 0
    applications = 0
    num_text = cell.text
    if (num_text is not None):
        nums = num_text.split("/")
        courts = nums[0]
        applications = nums[1]

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
            return find_element(week_button, element.GO_TO_NEXT_WEEK)
        except NoSuchElementException:
            continue
    # Next week button doesn't exist.
    return None


def export_csv_data(cell_data_list):
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = OUTPUT_PATH + "tennis_data_" + current_time + ".csv"

    with open(file_name, "w", encoding="UTF8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=cell_data_list[0].keys())
        writer.writeheader()
        writer.writerows(cell_data_list)


def export_json_data(cell_data_list):
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = OUTPUT_PATH + "tennis_data_" + current_time + ".json"

    with open(file_name, "w", encoding="UTF8", newline="") as file:
        json.dump(cell_data_list, file)


get_application_status()
