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
    last_press_ticks_us: int

    def __init__(
        self,
        sequence: list[tuple[int, float]],
        active: bool,
        position: int,
        position_ticks_us: int,
        last_press_ticks_us: int,
    ) -> None:
        self.sequence = sequence
        self.active = active
        self.position = position
        self.position_ticks_us = position_ticks_us
        self.last_press_ticks_us = last_press_ticks_us

    def start(self, position_ticks_us: int) -> None:
        self.active = True
        self.position = 0
        self.position_ticks_us = position_ticks_us

    def started(self) -> bool:
        return self.active

    def stop(self) -> None:
        self.active = False


class ButtonPressResult:
    reliably_pressed: bool
    last_press_ticks_us: int

    def __init__(
        self,
        reliably_pressed: bool,
        last_press_ticks_us: int,
    ) -> None:
        self.reliably_pressed = reliably_pressed
        self.last_press_ticks_us = last_press_ticks_us

    def __str__(self) -> str:
        return (
            f"{'PRESSED' if self.reliably_pressed else ''}; {self.last_press_ticks_us}"
        )


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

    def get_button_press_result(
        self, current_ticks: int, button_status: ButtonStatus, last_press_ticks_us: int
    ) -> ButtonPressResult:
        if button_status == ButtonStatus.PRESSED:
            ticks_since_last = self.config.timer.ticks_diff(
                current_ticks, last_press_ticks_us
            )
            if ticks_since_last > 500000:
                return ButtonPressResult(
                    reliably_pressed=True, last_press_ticks_us=current_ticks
                )
        return ButtonPressResult(
            reliably_pressed=False, last_press_ticks_us=last_press_ticks_us
        )

    def ui_loop(self) -> None:
        sequence_status = SequenceStatus(
            sequence=[
                (LedStatus.ON, 0.2),
                (LedStatus.OFF, 0.2),
                (LedStatus.ON, 0.2),
                (LedStatus.OFF, 0.2),
                (LedStatus.ON, 0.2),
                (LedStatus.OFF, 0.6),
                (LedStatus.ON, 0.6),
                (LedStatus.OFF, 0.2),
                (LedStatus.ON, 0.6),
                (LedStatus.OFF, 0.2),
                (LedStatus.ON, 0.6),
                (LedStatus.OFF, 0.6),
                (LedStatus.ON, 0.2),
                (LedStatus.OFF, 0.2),
                (LedStatus.ON, 0.2),
                (LedStatus.OFF, 0.2),
                (LedStatus.ON, 0.2),
                (LedStatus.OFF, 0.6),
            ],
            active=False,
            position=0,
            position_ticks_us=0,
            last_press_ticks_us=0,
        )

        while self.shoud_run():

            value = self.config.button.value()

            current = self.config.timer.ticks_us()

            button_press_result = self.get_button_press_result(
                current_ticks=current,
                button_status=value,
                last_press_ticks_us=sequence_status.last_press_ticks_us,
            )

            sequence_status.last_press_ticks_us = (
                button_press_result.last_press_ticks_us
            )

            if button_press_result.reliably_pressed:
                if not sequence_status.started():
                    sequence_status.start(current)
                else:
                    sequence_status.stop()

            if sequence_status.started():
                ticks = self.config.timer.ticks_diff(
                    current, sequence_status.position_ticks_us
                )

                status, duration_s = sequence_status.sequence[sequence_status.position]
                duration_us = int(1000000 * duration_s)

                if ticks > duration_us:
                    sequence_status.position += 1
                    sequence_status.position_ticks_us = current

                    if sequence_status.position == len(sequence_status.sequence):
                        sequence_status.stop()

                if status == LedStatus.ON:
                    self.config.led.on()
                else:
                    self.config.led.off()
