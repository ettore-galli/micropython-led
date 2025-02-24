from led_ui.button import Button
from led_ui.led import Led
from led_ui.logic import OneUIConfiguration, Strobo
from led_ui.timer import Timer

if __name__ == "__main__":
    led = Led(pin_number=15)
    button = Button(pin_number=16)
    # ui = OneUI(config=OneUIConfiguration(led=led, timer=Timer(), button=button))  # noqa: ERA001
    # ui.ui_loop() # noqa: ERA001
    strobo = Strobo(config=OneUIConfiguration(led=led, timer=Timer(), button=button))
    strobo.strobo_loop(8)
