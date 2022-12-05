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


def create_park_element(park_id: str) -> Element:
    return Element(By.XPATH, f"//a[contains(@href,'{park_id}')]")


# Main page
GO_TO_LOGIN = Element(By.XPATH, "//a[contains(@href,'gRsvLoginUserAction')]")

# Log-in page
ID_FIELD = Element(By.NAME, "userId")
PASS_FIELD = Element(By.NAME, "password")
LOGIN_BUTTON = Element(By.XPATH, "//a[contains(@href,'submitLogin')]")

# Member page
GO_TO_RAFFLE = Element(
    By.XPATH, "//a[contains(@href,'gLotWSetupLotAcceptAction')]")
GO_TO_SPORT_TYPES = Element(
    By.XPATH, "//a[contains(@href,'lotWTransLotAcceptListAction')]")
GO_TO_TENNIS = Element(By.XPATH, "//a[contains(@href,'130')]")

# Raffle page
PARK_IN_LIST = Element(By.XPATH, "//a[contains(@href,'sendBldGrpCd')]")
PARK_NAME = Element(By.XPATH, "//td[@class='lotselectlist'][2]")
CELL = Element(By.XPATH, "//a[contains(@href,'selectOnKoma')]")
GO_TO_NEXT_WEEK = Element(By.XPATH, "//a[contains(@href,'gLotWTransLotInstSrchVacantAction')]")
WEEK_BUTTON = Element(By.XPATH, "//a[contains(@href,'gLotWTransLotInstSrchVacantAction')]")
GO_TO_NEXT_WEEK = Element(By.XPATH, ".//img[@alt='次の週']")
GO_BACK_TO_PARK_LIST = Element(By.XPATH, "//a[contains(@href,'gLotWTransLotInstGrpPageMoveAction')]")