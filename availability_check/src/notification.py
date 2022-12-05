import requests
from config import LINE_TOKEN
from court import Court
from weather import Weather, get_weather_from_date

BROADCAST_URL = 'https://api.line.me/v2/bot/message/broadcast'

HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + LINE_TOKEN,
}


def notify_availablity(courts: list[Court], weathers: list[Weather]):

    court_info = build_court_info(courts, weathers)
    body = build_body(court_info)

    response = requests.post(BROADCAST_URL, headers=HEADERS, json=body)

    print("Status Code: ", response.status_code)
    print("JSON response: ", response.json())


def build_court_info(courts: list[Court], weathers: list[Weather]):
    court_info = ''
    for court in courts:
        weather = get_weather_from_date(weathers, court.date)
        new_court = court.__str__() + weather.get_icon()
        if court_info.__len__() == 0:
            court_info = new_court
        else:
            court_info = court_info + '\n' + new_court
    return court_info


def build_body(court_info: str):
    body = {
        'messages': [
            {
                'type': 'text',
                'text': f"Available courts found! 🎾\n\n{court_info}\n\nBook from here: https://yoyaku.sports.metro.tokyo.lg.jp/sp/",
            }
        ]
    }
    return body
