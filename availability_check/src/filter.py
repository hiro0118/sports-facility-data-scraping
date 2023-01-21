import datetime

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
    '有明テニスの森公園',
]


def need_to_check_park(park: str):
    for park_to_check in PARKS_TO_CHECK:
        if park_to_check in park:
            return True
    return False


class Time:
    def __init__(self, day_of_week: int, time: str):
        self.day_of_week = day_of_week
        self.time = time

    def matches(self, year: int, month: int, day: int, time: str):
        date_input = datetime.date(year, month, day)
        weekday_input = date_input.weekday()
        return (self.day_of_week == weekday_input) and (self.time == time)


TIMES_TO_IGNORE: list[Time] = [
    # For day_of_week, Monday is 0 and Sunday is 6
    Time(6, '19:00')
]


def need_to_check_time(date: str, time: str):
    ymd = date.split('/')
    if (ymd.__len__ == 3):
        # Illegal data, but return true to not overlook possible issues.
        return True
    for time_to_ignore in TIMES_TO_IGNORE:
        time_to_ignore.matches(int(ymd[0]), int(ymd[1]), int(ymd[2]), time)
        if time == time_to_ignore:
            return False
    return True
