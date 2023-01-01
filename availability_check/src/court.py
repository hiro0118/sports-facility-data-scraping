class Court:
    def __init__(self, date: str, time: str, park: str):
        self.date = date
        self.time = time
        self.park = park

    def __str__(self):
        return f'{self.date} {self.time} {self.park}'
