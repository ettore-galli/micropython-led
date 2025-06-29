from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any, TypeAlias

Incomplete: TypeAlias = Any

SpecialPins: TypeAlias = str

PICO_W_INTERNAL_LED_PIN: SpecialPins = "LED"

WEB_PAGES_PATH: str = "./web"

WEB_PAGE_INDEX_WIFI = "wifi"
WEB_PAGE_INDEX_LED = "led"

WEB_PAGES: dict[str, str] = {
    WEB_PAGE_INDEX_LED: "led.html",
    WEB_PAGE_INDEX_WIFI: "wifi.html",
}

DATA_FILES: dict[str, str] = {
    WEB_PAGE_INDEX_LED: "./data/led.json",
    WEB_PAGE_INDEX_WIFI: "./data/wifi.json",
}

rpi_logger = print


class BaseTime(ABC):
    @abstractmethod
    async def sleep(self, seconds: float) -> None:
        _ = seconds

    @abstractmethod
    def ticks_ms(self) -> int:
        return 0


class BasePin(ABC):
    OUT: int = 1
    IN: int = 0

    def __init__(self, pin_id: int | SpecialPins, mode: int) -> None:
        _ = pin_id, mode

    @abstractmethod
    def on(self) -> None:
        pass

    @abstractmethod
    def off(self) -> None:
        pass

    @abstractmethod
    def value(self) -> int:
        pass


class AccessPointInformation:
    def __init__(self, ssid: str, password: str) -> None:
        self.ssid: str = ssid
        self.password: str = password


class BaseAccessPoint(ABC):
    def __init__(self, access_point_information: AccessPointInformation) -> None:
        self.access_point_information = access_point_information

    @abstractmethod
    async def startup(self) -> None:
        pass


class WifiClientInformation:
    def __init__(self, ssid: str, password: str) -> None:
        self.ssid: str = ssid
        self.password: str = password
        self.poll_interval: int = 1
        self.connection_timeout: int = 10


EMPTY_WIFI_CLIENT_INFORMATION = WifiClientInformation(ssid="", password="")


class BaseWifiClient(ABC):
    def __init__(
        self, wifi_client_information_retriever: Callable[[], WifiClientInformation]
    ) -> None:
        self.wifi_client_information_retriever = wifi_client_information_retriever

    @abstractmethod
    async def startup(self) -> None:
        pass


class BaseWebServer(ABC):
    @abstractmethod
    def __init__(self) -> None: ...
    @abstractmethod
    async def startup(self) -> None:
        pass


class BaseDataService(ABC):

    def __init__(self, data_file: str) -> None:
        self.data_file = data_file

    @abstractmethod
    def get_data(self) -> dict[str, Any]: ...

    @abstractmethod
    def save_data(self, data: dict[str, Any]) -> None: ...
