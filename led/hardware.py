import asyncio

import utime as time  # type: ignore[import-not-found]
from machine import Pin  # type: ignore[import-not-found]

from led.base import (
    PICO_W_INTERNAL_LED_PIN,
    AccessPointInformation,
    BasePin,
    BaseTime,
    SpecialPins,
)


class HardwareTime(BaseTime):
    async def sleep(self, seconds: float) -> None:
        await asyncio.sleep(seconds)

    def ticks_ms(self) -> int:
        return time.ticks_ms()


class HardwarePin(BasePin):
    OUT: int = 1
    IN: int = 0

    def __init__(self, pin_id: int | SpecialPins, mode: int) -> None:
        self._pin: Pin = Pin(pin_id, mode)

    def on(self) -> None:
        self._pin.on()

    def off(self) -> None:
        self._pin.off()

    def value(self) -> int:
        return self._pin.value()


ACCESS_POINT_INFORMATION = AccessPointInformation(
    ssid="CONFIG-HOST", password="password!"  # noqa: S106
)


class HardwareInformation:
    def __init__(self) -> None:
        self.led_pin: int | SpecialPins = PICO_W_INTERNAL_LED_PIN
