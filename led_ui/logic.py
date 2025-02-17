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
    sequence: list[tuple[int, float]]
    active: bool
    position: int
    position_ticks_us: int

    def __init__(
        self,
        sequence: list[tuple[int, float]],
        active: bool,
        position: int,
        position_ticks_us: int,
    ) -> None:
        self.sequence = sequence
        self.active = active
        self.position = position
        self.position_ticks_us = position_ticks_us

    def start(self, position_ticks_us: int) -> None:
        self.active = True
        self.position = 0
        self.position_ticks_us = position_ticks_us

    def started(self) -> bool:
        return self.active

    def stop(self) -> None:
        self.active = False


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
        sequence_status = SequenceStatus(
            sequence=[
                (LedStatus.ON, 0.2),
                (LedStatus.OFF, 0.2),
                (LedStatus.ON, 0.6),
                (LedStatus.OFF, 0.2),
                (LedStatus.ON, 0.2),
                (LedStatus.OFF, 0.2),
            ],
            active=False,
            position=0,
            position_ticks_us=0,
        )

        while self.shoud_run():

            value = self.config.button.value()

            if value == ButtonStatus.PRESSED:
                if not sequence_status.started():
                    sequence_status.start(self.config.timer.ticks_us())

            if sequence_status.started():
                ticks = self.config.timer.ticks_diff(
                    self.config.timer.ticks_us(), sequence_status.position_ticks_us
                )

                status, duration_s = sequence_status.sequence[sequence_status.position]
                duration_us = int(1000000 * duration_s)

                if ticks > duration_us:
                    sequence_status.position += 1
                    sequence_status.position_ticks_us = self.config.timer.ticks_us()

                    if sequence_status.position == len(sequence_status.sequence):
                        sequence_status.stop()

                if status == LedStatus.ON:
                    self.config.led.on()
                else:
                    self.config.led.off()

                    # self.notify_sequence(
                    #     [
                    #         (LedStatus.ON, 0.2),
                    #         (LedStatus.OFF, 0.2),
                    #         (LedStatus.ON, 0.6),
                    #         (LedStatus.OFF, 0.2),
                    #         (LedStatus.ON, 0.2),
                    #         (LedStatus.OFF, 0.2),
                    #     ]
                    # )
            # else:
            #     self.config.led.off()
            self.config.timer.sleep(0.01)
