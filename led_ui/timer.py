import time

from led_ui.base import BaseTimer


class Timer(BaseTimer):
    def sleep(self, seconds: float) -> None:
        time.sleep(seconds)

    def ticks_diff(self, ticks1: int, ticks2: int) -> int:
        return time.ticks_diff(ticks1, ticks2)  # type: ignore[attr-defined]

    def ticks_us(self) -> int:
        return time.ticks_us()  # type: ignore[attr-defined]
