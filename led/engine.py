import asyncio
import sys

from led.base import (
    BaseAccessPoint,
    BaseLightService,
    BaseTime,
    BaseWebServer,
    BaseWifiClient,
)
from led.light_service import LightService


class LedBlinkerEngine:
    LED_ON: int = 1
    LED_OFF: int = 0

    def __init__(
        self,
        time: BaseTime,
        access_point: BaseAccessPoint,
        web_server: BaseWebServer,
        wifi_client: BaseWifiClient,
        light_service: LightService,
    ) -> None:
        self.time: BaseTime = time

        self.access_point: BaseAccessPoint = access_point

        self.wifi_client: BaseWifiClient = wifi_client

        self.light_service: BaseLightService = light_service

        self.web_server: BaseWebServer = web_server

    def log(self, message: str) -> None:
        sys.stdout.write(f"{self.time.ticks_ms()}: {message}\n")

    async def main(self) -> None:
        await asyncio.gather(
            self.light_service.led_loop(),
            self.access_point.startup(),
            self.web_server.startup(),
            self.wifi_client.startup(),
        )
