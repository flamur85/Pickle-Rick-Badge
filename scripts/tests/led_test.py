from gpiozero import LED
from time import sleep

led_pins = [26, 5, 13, 6, 19, 22]
leds = [LED(pin) for pin in led_pins]

print("LED test starting...")
for _ in range(3):
    for led in leds:
        led.on(); sleep(0.2); led.off()
print("LED test done.")
