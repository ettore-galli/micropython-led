from collections.abc import Callable
from typing import Any

import network  # type: ignore[import-not-found]

from led.base import (
    EMPTY_WIFI_CLIENT_INFORMATION,
    AccessPointInformation,
    BaseAccessPoint,
    BaseDataService,
    BaseTime,
    BaseWifiClient,
    WifiClientInformation,
    rpi_logger,
)
from led.data_service import get_wifi_data_service


class NetworkData(BaseDataService):
    def __init__(self) -> None:
        pass

    def get_data(self) -> dict[str, Any]:
        try:
            config = network.WLAN(network.STA_IF).ipconfig("addr4")
            return {"ip": config[0], "mask": config[1]}
        except OSError:
            return {"ip": None, "mask": None}

    def save_data(self, data: dict[str, Any]) -> None:
        _ = data


class AccessPoint(BaseAccessPoint):
    def __init__(self, access_point_information: AccessPointInformation) -> None:
        super().__init__(access_point_information=access_point_information)

        self.logger = rpi_logger

    async def startup(self) -> None:
        ap = network.WLAN(network.AP_IF)
        ap.config(
            ssid=self.access_point_information.ssid,
            password=self.access_point_information.password,
        )
        ap.active(True)  # noqa: FBT003


class WifiClient(BaseWifiClient):
    def __init__(
        self,
        wifi_client_information_retriever: Callable[[], WifiClientInformation],
        time: BaseTime,
        logger: Callable[[str], None] = rpi_logger,
    ) -> None:
        super().__init__(
            wifi_client_information_retriever=wifi_client_information_retriever,
            time=time,
            logger=logger,
        )

        self.wifi_client_information: WifiClientInformation = (
            EMPTY_WIFI_CLIENT_INFORMATION
        )

    async def startup(
        self,
        poll_interval: int = 1,
        connection_timeout: int = 10,
    ) -> None:

        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)  # noqa: FBT003  no keyword argument allowed
        self.wifi_client_information = self.wifi_client_information_retriever()
        wlan.connect(
            self.wifi_client_information.ssid, self.wifi_client_information.password
        )
        timeout = connection_timeout
        while not wlan.isconnected() and timeout > 0:
            await self.time.sleep(poll_interval)
            timeout -= 1

        if not wlan.isconnected():
            self.logger("Wi-Fi connection failed.")
            return

        self.logger(f"Connected! IP: {wlan.ifconfig()[0]}")


def retrieve_wifi_client_information() -> WifiClientInformation:
    data = get_wifi_data_service()
    credentials = data.get_data()
    if credentials:
        return WifiClientInformation(
            ssid=credentials["ssid"], password=credentials["password"]
        )
    return EMPTY_WIFI_CLIENT_INFORMATION
