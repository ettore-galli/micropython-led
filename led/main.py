import asyncio

from led.engine import LedBlinkerEngine
from led.hardware import (
    HardwarePin,
    HardwareTime,
)
from led.network_service import (
    AccessPoint,
    WifiClient,
    retrieve_wifi_client_information,
)
from led.web_server import WebServer

if __name__ == "__main__":
    control_demo = LedBlinkerEngine(
        time=HardwareTime(),
        pin_class=HardwarePin,
        access_point_class=AccessPoint,
        wifi_client_class=WifiClient,
        wifi_client_information_retriever=retrieve_wifi_client_information,
        web_server_class=WebServer,
    )
    asyncio.run(control_demo.main())
