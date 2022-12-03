import requests


class Weather:
    def __init__(self, date: str, code: str):
        self.date = date
        self.code = code

    def __str__(self) -> str:
        return f'{self.date}: {self.code}'

    def get_icon(self) -> str:
        for weather_icon in WEATHER_ICONS:
            if self.code in weather_icon.codes:
                return weather_icon.icon
        return ''


class WeatherIcon:
    def __init__(self, icon: str, codes: list[str]):
        self.icon = icon
        self.codes = codes

    def contains(self, code: str):
        return code in self.codes


SUNNY = WeatherIcon('☀️', ['100'])
SUNNY_CLOUDY = WeatherIcon('🌤️',
                           ['101', '110', '111', '130', '131', '132', '201', '210', '211', '223'])
SUNNY_RAIN = WeatherIcon('🌦️',
                         ['102', '103', '104', '105', '106', '107', '108', '112', '113', '114',
                          '115', '116', '117', '118', '119', '120', '121', '122', '123', '124',
                          '125', '126', '127', '128', '140', '160', '170', '181', '301', '311',
                          '320', '323', '324', '325', '371', '401'])
CLOUNDY = WeatherIcon('☁️', ['200', '209', '231'])
CLOUDY_RAINY = WeatherIcon('🌧️',
                           ['202', '203', '204', '205', '206', '207', '208', '212', '213', '214',
                            '215', '216', '217', '218', '219', '220', '221', '222', '224', '225',
                            '226', '228', '229', '230', '240', '250', '260', '270', '281', '302',
                            '316', '317', '321'])
RAINY = WeatherIcon('☔',
                    ['300', '303', '304', '306', '308', '309', '313', '314', '315', '322',
                     '326', '327', '328', '329', '340'])
THUNDER = WeatherIcon('⛈️', ['350'])
SNOWY = WeatherIcon('☃️',
                    ['400', '402', '403', '405', '406', '407', '409', '411', '413', '414',
                     '420', '421', '422' '423', '425', '426', '427', '450'])


WEATHER_ICONS = [SUNNY, SUNNY_CLOUDY, SUNNY_RAIN,
                 CLOUNDY, CLOUDY_RAINY, RAINY, THUNDER, SNOWY]

URL = "https://www.jma.go.jp/bosai/forecast/data/forecast/130000.json"

EMPTY_WEATHER = Weather('9999/99/99', 'NA')
DAYS_IN_WEEK = 7
DELIMITER: str = '-'


def get_weather() -> list[Weather]:
    result: list[Weather] = []

    response = requests.get(URL)
    if (response.status_code != 200):
        return result

    js = response.json()

    idx = 0
    while idx < DAYS_IN_WEEK:
        date_info = js[1]['timeSeries'][0]['timeDefines'][idx][0:10].split(DELIMITER)
        yyyy = date_info[0]
        mm = date_info[1]
        dd = date_info[2]
        formatted_date = f'{yyyy}/{mm}/{dd}'
        weather_code = js[1]['timeSeries'][0]['areas'][0]['weatherCodes'][idx]
        result.append(Weather(formatted_date, weather_code))
        idx += 1

    return result


def get_weather_from_date(weathers: list[Weather], date: str) -> Weather:
    for weather in weathers:
        if weather.date == date:
            return weather
    return EMPTY_WEATHER
