import json
from collections.abc import Callable
from typing import Any

from led.base import (
    DATA_FILES,
    WEB_PAGE_INDEX_LED,
    WEB_PAGE_INDEX_WIFI,
    BaseDataService,
    rpi_logger,
)


class DataService(BaseDataService):
    def __init__(
        self,
        data_file: str,
        logger: Callable[[str], None],
        model: dict[str, type] | None = None,
    ) -> None:
        super().__init__(data_file)
        self.logger: Callable[[str], None] = logger
        self.model: dict[str, type] | None = model

    @staticmethod
    def cast_data_to_model(
        data: dict[str, Any], model: dict[str, type]
    ) -> dict[str, Any]:
        return {
            key: model[key](value) if key in model else value
            for key, value in data.items()
        }

    def get_data(self) -> dict[str, Any]:
        try:
            with open(self.data_file, encoding="utf-8") as datafile:
                return json.load(datafile)
        except OSError as error:
            self.logger(str(error))
            return {}

    def save_data(self, data: dict[str, Any]) -> None:
        try:
            with open(self.data_file, "w", encoding="utf-8") as datafile:
                return json.dump(
                    (
                        self.cast_data_to_model(data, self.model)
                        if self.model is not None
                        else data
                    ),
                    datafile,
                )
        except OSError as error:
            self.logger(str(error))


def get_led_data_service() -> BaseDataService:
    return DataService(data_file=DATA_FILES[WEB_PAGE_INDEX_LED], logger=rpi_logger)


def get_wifi_data_service() -> BaseDataService:
    return DataService(data_file=DATA_FILES[WEB_PAGE_INDEX_WIFI], logger=rpi_logger)
