import asyncio

from led.base import AccessPointInformation, BaseAccessPoint
from led.engine import LedBlinkerEngine
from led.hardware import (
    ACCESS_POINT_INFORMATION,
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

hardware_information: HardwareInformation = HardwareInformation()

access_point_information: AccessPointInformation = ACCESS_POINT_INFORMATION

light_service = LightService(
    time=HardwareTime(),
    pin_class=HardwarePin,
    hardware_information=hardware_information,
    light_blink_information_retriever=retrieve_light_blink_information,
)

access_point: BaseAccessPoint = AccessPoint(
    access_point_information=access_point_information
)

if __name__ == "__main__":
    control_demo = LedBlinkerEngine(
        time=HardwareTime(),
        pin_class=HardwarePin,
        access_point=access_point,
        wifi_client_class=WifiClient,
        wifi_client_information_retriever=retrieve_wifi_client_information,
        web_server_class=WebServer,
        hardware_information=hardware_information,
        light_service=light_service,
    )
    asyncio.run(control_demo.main())
