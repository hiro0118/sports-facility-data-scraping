import traceback
import requests
from config import LINE_TOKEN, ADMIN_ID
from court import Court
from weather import Weather, get_weather_from_date

BROADCAST_URL = 'https://api.line.me/v2/bot/message/broadcast'
PUSH_URL = 'https://api.line.me/v2/bot/message/push'

HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + LINE_TOKEN,
}


def broadcast(msg: str):
    body = {
        'messages': [
            {
                'type': 'text',
                'text': msg
            }
        ]
    }
    response = requests.post(BROADCAST_URL, headers=HEADERS, json=body)
    print("Status Code: ", response.status_code)
    print("JSON response: ", response.json())


def push(to: str, msg: str):
    body = {
        'to': to,
        'messages': [
            {
                'type': 'text',
                'text': msg
            }
        ]
    }
    response = requests.post(PUSH_URL, headers=HEADERS, json=body)
    print("Status Code: ", response.status_code)
    print("JSON response: ", response.json())


def notify_availablity(courts: list[Court], weathers: list[Weather]):
    court_info = ''
    for court in courts:
        weather = get_weather_from_date(weathers, court.date)
        new_court = court.__str__() + weather.get_icon()
        if court_info.__len__() == 0:
            court_info = new_court
        else:
            court_info = court_info + '\n' + new_court
    msg = f"Available courts found! 🎾\n\n{court_info}\n\nBook from here: https://yoyaku.sports.metro.tokyo.lg.jp/sp/"
    broadcast(msg)


def notify_error(e: Exception):
    error_msg = traceback.format_exception_only(type(e), e)
    push(ADMIN_ID, error_msg)
