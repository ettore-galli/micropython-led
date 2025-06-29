from typing import Any

import network  # type: ignore[import-not-found]

from led.base import BaseDataService


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
