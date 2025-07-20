import asyncio

from led.base import (
    DATA_FILES,
    WEB_PAGE_INDEX_LED,
    WEB_PAGE_INDEX_WIFI,
    AccessPointInformation,
    BaseAccessPoint,
    BaseWebServer,
    rpi_logger,
)
from led.data_service import DataService
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
    NetworkData,
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

wifi_client = WifiClient(
    wifi_client_information_retriever=retrieve_wifi_client_information,
    time=HardwareTime(),
)

web_server: BaseWebServer = WebServer(
    led_data_service=DataService(
        data_file=DATA_FILES[WEB_PAGE_INDEX_LED], logger=rpi_logger
    ),
    wifi_data_service=DataService(
        data_file=DATA_FILES[WEB_PAGE_INDEX_WIFI], logger=rpi_logger
    ),
    network_data_service=NetworkData(),
)

if __name__ == "__main__":
    control_demo = LedBlinkerEngine(
        time=HardwareTime(),
        access_point=access_point,
        wifi_client=wifi_client,
        web_server=web_server,
        light_service=light_service,
    )
    asyncio.run(control_demo.main())
