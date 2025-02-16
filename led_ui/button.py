from machine import Pin  # type: ignore[import-not-found]

from led_ui.base import BaseButton, ButtonStatus


class Button(BaseButton):

    def __init__(self, pin_number: int) -> None:
        self.pin: Pin = Pin(pin_number, Pin.IN, Pin.PULL_UP)

    def value(self) -> int:
        return ButtonStatus.RELEASED if self.pin.value() else ButtonStatus.PRESSED
