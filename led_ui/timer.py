import time

from led_ui.base import BaseTimer


class Timer(BaseTimer):
    def sleep(self, seconds: float) -> None:
        time.sleep(seconds)
