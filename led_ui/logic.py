from led_ui.base import (
    BaseButton,
    BaseLed,
    BaseTimer,
    ButtonStatus,
    LedStatus,
    PwmStatus,
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
        active: bool,  # noqa: FBT001
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
        reliably_pressed: bool,  # noqa: FBT001
        last_press_ticks_us: int,
    ) -> None:
        self.reliably_pressed = reliably_pressed
        self.last_press_ticks_us = last_press_ticks_us

    def __str__(self) -> str:
        return (
            f"{'PRESSED' if self.reliably_pressed else ''}; {self.last_press_ticks_us}"
        )


class OneUI:
    RELIABLE_PRESS_DELAY: int = 500000
    MICROSECONDS_PER_SECOND: int = 1000000

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
        self, current_ticks: int, button_status: int, last_press_ticks_us: int
    ) -> ButtonPressResult:
        if button_status == ButtonStatus.PRESSED:
            ticks_since_last = self.config.timer.ticks_diff(
                current_ticks, last_press_ticks_us
            )
            if ticks_since_last > OneUI.RELIABLE_PRESS_DELAY:
                return ButtonPressResult(
                    reliably_pressed=True, last_press_ticks_us=current_ticks
                )
        return ButtonPressResult(
            reliably_pressed=False, last_press_ticks_us=last_press_ticks_us
        )

    @staticmethod
    def get_sequence_to_play() -> list[tuple[int, float]]:
        return [
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
        ]

    def perform_sequence_step(
        self,
        button_value: int,
        current_ticks: int,
        sequence_status: SequenceStatus,
    ) -> SequenceStatus:

        button_press_result = self.get_button_press_result(
            current_ticks=current_ticks,
            button_status=button_value,
            last_press_ticks_us=sequence_status.last_press_ticks_us,
        )

        sequence_status.last_press_ticks_us = button_press_result.last_press_ticks_us

        if button_press_result.reliably_pressed:
            if not sequence_status.started():
                sequence_status.start(current_ticks)
            else:
                sequence_status.stop()

        if sequence_status.started():
            ticks = self.config.timer.ticks_diff(
                current_ticks, sequence_status.position_ticks_us
            )

            status, duration_s = sequence_status.sequence[sequence_status.position]
            duration_us = int(OneUI.MICROSECONDS_PER_SECOND * duration_s)

            if ticks > duration_us:
                sequence_status.position += 1
                sequence_status.position_ticks_us = current_ticks

                if sequence_status.position == len(sequence_status.sequence):
                    sequence_status.stop()

            if status == LedStatus.ON:
                self.config.led.on()
            else:
                self.config.led.off()
        return sequence_status

    def ui_loop(self) -> None:
        sequence_status = SequenceStatus(
            sequence=self.get_sequence_to_play(),
            active=False,
            position=0,
            position_ticks_us=0,
            last_press_ticks_us=0,
        )

        while self.shoud_run():

            value = self.config.button.value()

            current = self.config.timer.ticks_us()

            sequence_status = self.perform_sequence_step(
                button_value=value,
                current_ticks=current,
                sequence_status=sequence_status,
            )


class Strobo:
    def __init__(self, config: OneUIConfiguration) -> None:
        self.config = config

    def strobo_loop(self, frequency: float) -> None:
        pwm_status: int = 0
        while True:
            if self.config.button.value() == ButtonStatus.PRESSED:
                if pwm_status == PwmStatus.OFF:
                    pwm_status = PwmStatus.ON
                    self.config.led.start_pwm(frequency=frequency)
            elif pwm_status == PwmStatus.ON:
                pwm_status = PwmStatus.OFF
                self.config.led.stop_pwm()
