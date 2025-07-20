import asyncio
import sys

from led.base import (
    DATA_FILES,
    WEB_PAGE_INDEX_LED,
    WEB_PAGE_INDEX_WIFI,
    BaseAccessPoint,
    BaseLightService,
    BasePin,
    BaseTime,
    BaseWebServer,
    BaseWifiClient,
    rpi_logger,
)
from led.data_service import DataService
from led.light_service import LightService
from led.network_service import NetworkData


class LedBlinkerEngine:
    LED_ON: int = 1
    LED_OFF: int = 0

    def __init__(  # noqa: PLR0913
        self,
        time: BaseTime,
        pin_class: type[BasePin],
        access_point: BaseAccessPoint,
        web_server_class: type[BaseWebServer],
        wifi_client: BaseWifiClient,
        light_service: LightService,
    ) -> None:
        self.time: BaseTime = time
        self.pin_class: type[BasePin] = pin_class

        self.access_point: BaseAccessPoint = access_point

        self.wifi_client: BaseWifiClient = wifi_client

        self.light_service: BaseLightService = light_service

        self.web_server_class = web_server_class
        self.web_server = self.web_server_class(
            led_data_service=DataService(
                data_file=DATA_FILES[WEB_PAGE_INDEX_LED], logger=rpi_logger
            ),
            wifi_data_service=DataService(
                data_file=DATA_FILES[WEB_PAGE_INDEX_WIFI], logger=rpi_logger
            ),
            network_data_service=NetworkData(),
        )

    def log(self, message: str) -> None:
        sys.stdout.write(f"{self.time.ticks_ms()}: {message}\n")

    async def main(self) -> None:
        await asyncio.gather(
            self.light_service.led_loop(),
            self.access_point.startup(),
            self.web_server.startup(),
            self.wifi_client.startup(),
        )
