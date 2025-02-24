from machine import PWM, Pin  # type: ignore[import-not-found]

from led_ui.base import BaseLed


class Led(BaseLed):
    LED_DUTY_ON = 32768
    LED_DUTY_OFF = 0

    def __init__(self, pin_number: int) -> None:
        self.pin: Pin = Pin(pin_number, Pin.OUT)
        self.pwm = PWM(self.pin)
        self.pwm.duty_u16(Led.LED_DUTY_ON)

    def on(self) -> None:
        self.pin.on()

    def off(self) -> None:
        self.pin.off()

    def start_pwm(self, frequency: float) -> None:
        self.pwm.freq(frequency)
        self.pwm.duty_u16(Led.LED_DUTY_ON)

    def stop_pwm(self) -> None:
        self.pwm.duty_u16(Led.LED_DUTY_OFF)
