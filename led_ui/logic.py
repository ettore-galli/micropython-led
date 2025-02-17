from led_ui.base import (
    BaseButton,
    BaseLed,
    BaseTimer,
    ButtonStatus,
    LedStatus,
)


class OneUIConfiguration:
    def __init__(self, led: BaseLed, button: BaseButton, timer: BaseTimer) -> None:

        self.led: BaseLed = led
        self.button: BaseButton = button
        self.timer: BaseTimer = timer


class SequenceStatus:
    sequence: list[tuple[int, float]] | None
    position: int
    position_ticks_us: int

    def __init__(
        self,
        sequence: list[tuple[int, float]] | None,
        position: int,
        position_ticks_us: int,
    ) -> None:
        self.sequence = sequence
        self.position = position
        self.position_ticks_us = position_ticks_us


class OneUI:
    def __init__(self, config: OneUIConfiguration) -> None:
        self.config = config

    def demo_blink(self, delay: float) -> None:
        while True:
            self.config.led.on()
            self.config.timer.sleep(delay)
            self.config.led.off()
            self.config.timer.sleep(delay)

    def shoud_run(self) -> bool:
        return True

    def notify_sequence(self, sequence: list[tuple[int, float]]) -> None:
        for status, duration in sequence:
            if status == LedStatus.ON:
                self.config.led.on()
            else:
                self.config.led.off()
            self.config.timer.sleep(seconds=duration)

    def ui_loop(self) -> None:
        while self.shoud_run():
            value = self.config.button.value()

            if value == ButtonStatus.PRESSED:

                self.notify_sequence(
                    [
                        (LedStatus.ON, 0.2),
                        (LedStatus.OFF, 0.2),
                        (LedStatus.ON, 0.6),
                        (LedStatus.OFF, 0.2),
                        (LedStatus.ON, 0.2),
                        (LedStatus.OFF, 0.2),
                    ]
                )
            else:
                self.config.led.off()
            self.config.timer.sleep(0.01)
