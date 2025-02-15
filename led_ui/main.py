import time

from led_ui.led import Led

if __name__ == "__main__":
    led = Led(pin_number=15)
    while True:
        led.on()
        time.sleep(0.333)
        led.off()
        time.sleep(0.333)
