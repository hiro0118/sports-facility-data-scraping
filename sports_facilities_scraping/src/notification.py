import requests
from config import LINE_CHANNEL_ID, LINE_TOKEN
from court import Court
from weather import Weather, get_weather_from_date

PUSH_URL = 'https://api.line.me/v2/bot/message/push'

HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + LINE_TOKEN,
}

PARKS_TO_CHECK: list[str] = [
    '日比谷公園',
    '芝公園',
    '篠崎公園',
    '亀戸中央公園',
    '木場公園',
    '東綾瀬公園',
    '大島小松川公園',
    '大井ふ頭海浜公園',
    '有明テニスの森公園'
]


def notify_availablity(courts: list[Court], weathers: list[Weather]):

    court_info = build_court_info(courts, weathers)
    body = build_body(court_info)

    response = requests.post(PUSH_URL, headers=HEADERS, json=body)

    print("Status Code: ", response.status_code)
    print("JSON response: ", response.json())


def build_court_info(courts: list[Court], weathers: list[Weather]):
    court_info = ''
    for court in courts:
        if not need_to_check(court.park):
            continue
        weather = get_weather_from_date(weathers, court.date)
        new_court = court.__str__() + weather.get_icon()
        if court_info.__len__() == 0:
            court_info = new_court
        else:
            court_info = court_info + '\n' + new_court
    return court_info


def need_to_check(park: str) -> bool:
    for park_to_check in PARKS_TO_CHECK:
        if park_to_check in park:
            return True
    return False


def build_body(court_info: str):
    body = {
        'to': LINE_CHANNEL_ID,
        'messages': [
            {
                'type': 'text',
                'text': f"Available tennis courts found! 🎾\n\n{court_info}\n\nBook from here: https://yoyaku.sports.metro.tokyo.lg.jp/sp/",
            }
        ]
    }
    return body
