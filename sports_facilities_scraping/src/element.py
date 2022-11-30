from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

DEFAULT_PAUSE_SEC = 1


class Element:
    def __init__(self, by: By, path: str):
        self.by = by
        self.path = path


def click(parent: WebElement, element: Element):
    parent.find_element(element.by, element.path).click()


def pause_and_click(parent: WebElement, element: Element, pause: int = DEFAULT_PAUSE_SEC):
    sleep(pause)
    parent.find_element(element.by, element.path).click()


def find_element(parent: WebElement, element: Element) -> WebElement:
    return parent.find_element(element.by, element.path)


def find_elements(parent: WebElement, element: Element) -> list[WebElement]:
    return parent.find_elements(element.by, element.path)


def get_text(parent: WebElement, element: Element) -> str:
    return parent.find_element(element.by, element.path).text


########## MULTIFUNCTIONAL SITE ##########

# MAIN PAGE MAIIN

PURPOSE_SEARCH = Element(By.XPATH, "//a[contains(@href,'rsvPurposeSearch')]")
TENNIS_HARD = Element(By.XPATH, "//span[text()='テニス（ハード）']")
TENNIS_OMNI = Element(By.XPATH, "//span[text()='テニス（人工芝）']")
AVAILABILITY_SEARCH = Element(By.XPATH, "//input[contains(@id,'srchBtn')]")

# AVAILABILITY PAGE

ACTIVE_WEEKEND = Element(
    By.XPATH, "//td[@bgcolor='#ffdcf5' or @bgcolor='#e6e6fa' or @bgcolor='#2efecd']//a[@class='calclick']")
PARK_TABLE = Element(
    By.XPATH, "//div[@id='isNotEmptyPager']/table[@class='tablebg2']")
PARK_NAME = Element(By.XPATH, ".//span[@id='bnamem']")
AVAILABILITY_CELL = Element(By.XPATH, ".//span[@id='emptyFieldCnt']")
TIME = Element(By.XPATH, ".//span[@id='tzoneStimeLabel']")
NEXT_FIVE = Element(By.XPATH, "//a[@id='goNextPager']")
NEXT_MONTH = Element(By.XPATH, "//a[text()='次月']")
YEAR = Element(By.XPATH, "//span[@id='year--']")
MONTH = Element(By.XPATH, "//span[@id='month--']")
DATE = Element(By.XPATH, "//span[@id='day--']")
