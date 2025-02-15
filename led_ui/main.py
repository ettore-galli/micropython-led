from led_ui.led import Led
from led_ui.timer import Timer

if __name__ == "__main__":
    led = Led(pin_number=15)
    while True:
        timer = Timer()
        led.on()
        timer.sleep(0.333)
        led.off()
        timer.sleep(0.333)
