import asyncio

from led.engine import LedBlinkerEngine
from led.hardware import (
    HardwareInformation,
    HardwarePin,
    HardwareTime,
)
from led.light_service import LightService, retrieve_light_blink_information
from led.network_service import (
    AccessPoint,
    WifiClient,
    retrieve_wifi_client_information,
)
from led.web_server import WebServer

light_service = LightService(
    time=HardwareTime(),
    pin_class=HardwarePin,
    hardware_information=HardwareInformation(),
    light_blink_information_retriever=retrieve_light_blink_information,
)

if __name__ == "__main__":
    control_demo = LedBlinkerEngine(
        time=HardwareTime(),
        pin_class=HardwarePin,
        access_point_class=AccessPoint,
        wifi_client_class=WifiClient,
        wifi_client_information_retriever=retrieve_wifi_client_information,
        web_server_class=WebServer,
        light_service=light_service,
    )
    asyncio.run(control_demo.main())
