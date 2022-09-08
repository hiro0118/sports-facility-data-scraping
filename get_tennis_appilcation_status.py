# coding: UTF-8

import csv
import json
from datetime import datetime
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

import login_info

URL_HOME = "https://yoyaku.sports.metro.tokyo.lg.jp/web/"
URL_LOGIN = URL_HOME + "rsvLoginUserAction.do"
URL_MAIN = URL_HOME + "rsvWUA_Action.do"

CHROME_DRIVER_PATH = "./lib/chromedriver.exe"
OUTPUT_PATH = "output/"

WAIT_SEC = 2
WAIT_SEC_FOR_LOGIN = 4

def create_driver():
  options = webdriver.ChromeOptions()
  options.add_experimental_option('excludeSwitches', ['enable-logging'])
  options.use_chromium = True

  driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=options)
  return driver


def log_in(driver):
  print("logging in...")
  sleep(WAIT_SEC)
  # Go to home page
  driver.get(URL_HOME)
  sleep(WAIT_SEC)
  # Go to login page
  driver.switch_to.frame("pawae1002")
  driver.find_element(By.XPATH, "//a[contains(@href,\"gRsvLoginUserAction\")]").click()
  # Input login info
  driver.find_element(By.NAME, "userId").send_keys(login_info.ID)
  driver.find_element(By.NAME, "password").send_keys(login_info.PASSWORD)
  sleep(WAIT_SEC_FOR_LOGIN)
  # Click log-in button
  driver.find_element(By.XPATH, "//a[contains(@href,\"submitLogin\")]").click()


def go_to_tennis_page(driver):
  print("Going to tennis page...")
  sleep(WAIT_SEC)
  # Go to raffle page
  driver.find_element(By.XPATH, "//a[contains(@href,\"gLotWSetupLotAcceptAction\")]").click()
  sleep(WAIT_SEC)
  # Go to sport types page
  driver.find_element(By.XPATH, "//a[contains(@href,\"lotWTransLotAcceptListAction\")]").click()
  sleep(WAIT_SEC)
  # Go to tennis page
  driver.find_element(By.XPATH, "//a[contains(@href,\"130\")]").click()


def get_park_id_list(driver):
  park_id_list = []
  parks = driver.find_elements(By.XPATH, "//a[contains(@href,\"sendBldGrpCd\")]")
  for park in parks:
    href = park.get_attribute("href")
    park_id_list.append(href[-11:-4])
  return park_id_list


def get_cell_data(cell, park_name: str):

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
    "time": href_split[len(href_split) - 4] + "-" + href_split[len(href_split) - 3],
    "courts": courts,
    "applications": applications,
    "ratio": float(applications) / float(courts)
  }


def find_next_week_button(driver):
  week_buttons = driver.find_elements(By.XPATH, "//a[contains(@href,\"gLotWTransLotInstSrchVacantAction\")]")
  for week_button in week_buttons:
    try:
      week_button.find_element(By.XPATH, ".//img[contains(@alt,\"次の週\")]")
      next_week_button = week_button
      return next_week_button
    except NoSuchElementException as e:
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


def main():  
  driver = create_driver()

  log_in(driver)
  go_to_tennis_page(driver)

  cell_data_list = []

  # Check each park.
  for park_id in get_park_id_list(driver):
    sleep(WAIT_SEC)

    # Go to the park page.
    driver.find_element(By.XPATH, "//a[contains(@href,\"" + park_id + "\")]").click()

    park_name = driver.find_element(By.XPATH, "//*[@id=\"disp\"]/center/form/table[3]/tbody/tr[1]/td/table/tbody/tr[2]/td[2]").text

    # Check each week.
    while True:
      # Check all the cells in the week.
      cells = driver.find_elements(By.XPATH, "//a[contains(@href,\"selectOnKoma\")]")
      for cell in cells:
        cell_data = get_cell_data(cell, park_name)
        print(cell_data)
        cell_data_list.append(cell_data)

      # Go to the next week if it exists.
      next_week_button = find_next_week_button(driver)
      if next_week_button is not None:
        sleep(WAIT_SEC)
        next_week_button.click()
      else:
        break

    sleep(WAIT_SEC)

    # Go back to the park selection page.
    driver.find_element(By.XPATH, "//a[contains(@href,\"gLotWTransLotInstGrpPageMoveAction\")]").click()

  driver.close()

  if (len(cell_data_list) != 0):
    export_csv_data(cell_data_list)
    export_json_data(cell_data_list)


main()
