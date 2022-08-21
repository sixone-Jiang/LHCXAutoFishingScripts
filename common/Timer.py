from datetime import datetime


class Timer:
    start_time = None

    def __init__(self):
        self.start_time = datetime.now()

    def get_duration(self):
        return (datetime.now() - self.start_time).seconds
