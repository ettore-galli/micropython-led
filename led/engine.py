import asyncio
import sys
from collections.abc import Callable
from typing import TYPE_CHECKING

from led.base import (
    PICO_W_INTERNAL_LED_PIN,
    AccessPointInformation,
    BaseAccessPoint,
    BasePin,
    BaseTime,
    BaseWebServer,
    BaseWifiClient,
    WifiClientInformation,
)
from led.hardware import ACCESS_POINT_INFORMATION

if TYPE_CHECKING:
    from led.base import SpecialPins


class HardwareInformation:
    def __init__(self) -> None:
        self.led_pin: int | SpecialPins = PICO_W_INTERNAL_LED_PIN


class ControlDemoEngine:
    LED_ON: int = 1
    LED_OFF: int = 0

    def __init__(  # noqa: PLR0913
        self,
        time: BaseTime,
        pin_class: type[BasePin],
        access_point_class: type[BaseAccessPoint],
        web_server_class: type[BaseWebServer],
        wifi_client_class: type[BaseWifiClient],
        wifi_client_information_retriever: Callable[[], WifiClientInformation],
        hardware_information: HardwareInformation | None = None,
        access_point_information: AccessPointInformation | None = None,
    ) -> None:
        self.time: BaseTime = time
        self.pin_class: type[BasePin] = pin_class

        self.hardware_information = (
            hardware_information
            if hardware_information is not None
            else HardwareInformation()
        )

        self.access_point_information = (
            access_point_information
            if access_point_information is not None
            else ACCESS_POINT_INFORMATION
        )

        self.led = self.pin_class(self.hardware_information.led_pin, self.pin_class.OUT)

        self.access_point_class = access_point_class
        self.access_point = self.access_point_class(
            access_point_information=self.access_point_information
        )

        self.wifi_client_information_retriever = wifi_client_information_retriever
        self.wifi_client_class = wifi_client_class
        self.wifi_client = self.wifi_client_class(
            wifi_client_information_retriever=self.wifi_client_information_retriever
        )

        self.web_server_class = web_server_class
        self.web_server = self.web_server_class()

    def log(self, message: str) -> None:
        sys.stdout.write(f"{self.time.ticks_ms()}: {message}\n")

    async def led_loop(self) -> None:
        while True:
            self.led.on()
            await self.time.sleep(1)

            self.led.off()
            await self.time.sleep(1)

    async def main(self) -> None:
        await asyncio.gather(
            self.led_loop(),
            self.access_point.startup(),
            self.web_server.startup(),
            self.wifi_client.startup(),
        )
