from led_ui.button import Button
from led_ui.led import Led
from led_ui.logic import OneUI, OneUIConfiguration
from led_ui.timer import Timer

if __name__ == "__main__":
    led = Led(pin_number=15)
    button = Button(pin_number=16)
    ui = OneUI(config=OneUIConfiguration(led=led, timer=Timer(), button=button))
    ui.ui_loop()
