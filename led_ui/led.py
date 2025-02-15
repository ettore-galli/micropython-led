from machine import Pin  # type: ignore[import-not-found]

from led_ui.base import BaseLed


class Led(BaseLed):
    def __init__(self, pin_number: int) -> None:
        self.pin: Pin = Pin(pin_number)

    def on(self) -> None:
        self.pin.on()

    def off(self) -> None:
        self.pin.off()
