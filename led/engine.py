import asyncio
import sys
from collections.abc import Callable

from led.base import (
    DATA_FILES,
    WEB_PAGE_INDEX_LED,
    WEB_PAGE_INDEX_WIFI,
    AccessPointInformation,
    BaseAccessPoint,
    BasePin,
    BaseTime,
    BaseWebServer,
    BaseWifiClient,
    WifiClientInformation,
    rpi_logger,
)
from led.data_service import DataService
from led.hardware import ACCESS_POINT_INFORMATION, HardwareInformation, HardwareTime
from led.light_service import LightService
from led.network_service import NetworkData


class LedBlinkerEngine:
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
        light_service: LightService,
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

        self.access_point_class = access_point_class
        self.access_point = self.access_point_class(
            access_point_information=self.access_point_information
        )

        self.wifi_client_information_retriever = wifi_client_information_retriever
        self.wifi_client_class = wifi_client_class
        self.wifi_client = self.wifi_client_class(
            wifi_client_information_retriever=self.wifi_client_information_retriever,
            time=HardwareTime(),
        )

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

        self.light_service = light_service

    def log(self, message: str) -> None:
        sys.stdout.write(f"{self.time.ticks_ms()}: {message}\n")

    async def main(self) -> None:
        await asyncio.gather(
            self.light_service.led_loop(),
            self.access_point.startup(),
            self.web_server.startup(),
            self.wifi_client.startup(),
        )
