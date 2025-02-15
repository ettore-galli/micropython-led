from led_ui.base import BaseButton, BaseLed, BaseTimer


class OneUIConfiguration:
    def __init__(self, led: BaseLed, button: BaseButton, timer: BaseTimer) -> None:

        self.led: BaseLed = led
        self.button: BaseButton = button
        self.timer: BaseTimer = timer


class OneUI:
    def __init__(self, config: OneUIConfiguration) -> None:
        self.config = config

    def demo_blink(self, delay: float) -> None:
        while True:
            self.config.led.on()
            self.config.timer.sleep(delay)
            self.config.led.off()
            self.config.timer.sleep(delay)
