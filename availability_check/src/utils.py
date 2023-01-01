from datetime import datetime


def log(msg: str) -> None:
    time: str = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(time + ' ' + msg)
