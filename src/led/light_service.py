from collections.abc import Callable

from led.base import (
    DEFAULT_LIGHT_BLINK_INFORMATION,
    BaseLightService,
    BasePin,
    BaseTime,
    LightBlinkInformation,
)
from led.data_service import get_led_data_service
from led.hardware import HardwareInformation


class LightService(BaseLightService):
    def __init__(
        self,
        time: BaseTime,
        pin_class: type[BasePin],
        hardware_information: HardwareInformation,
        light_blink_information_retriever: Callable[[], LightBlinkInformation],
    ) -> None:

        self.time: BaseTime = time
        self.pin_class: type[BasePin] = pin_class

        self.hardware_information = (
            hardware_information
            if hardware_information is not None
            else HardwareInformation()
        )

        self.led = self.pin_class(self.hardware_information.led_pin, self.pin_class.OUT)

        self.light_blink_information_retriever = light_blink_information_retriever

    async def blink_loop(self) -> None:
        pass

    async def led_loop(self) -> None:

        while True:
            info: LightBlinkInformation = self.light_blink_information_retriever()

            for _ in range(info.number_of_flashes):

                self.led.on()
                await self.time.sleep(info.flash_duration)

                self.led.off()
                await self.time.sleep(info.intra_flash_delay)

            await self.time.sleep(info.intra_loop_delay)


def retrieve_light_blink_information() -> LightBlinkInformation:
    data = get_led_data_service()
    info = data.get_data()
    if info:
        return LightBlinkInformation(
            number_of_flashes=int(info["number_of_flashes"]),
            flash_duration=float(info["flash_duration"]),
            intra_flash_delay=float(info["intra_flash_delay"]),
            intra_loop_delay=float(info["intra_loop_delay"]),
        )
    return DEFAULT_LIGHT_BLINK_INFORMATION
