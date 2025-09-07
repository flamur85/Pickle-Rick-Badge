from gpiozero import PWMOutputDevice, LED
from time import sleep
import subprocess
from threading import Lock
import random

motor = PWMOutputDevice(18)
led_pins = [26, 5, 13, 6, 19, 22]
leds = [LED(pin) for pin in led_pins]

pickle_rick_long = "/home/admin/audio_files/pr_long.mp3"

show_lock = Lock()

for led in leds:
    led.off()

def full_show():
    if not show_lock.acquire(blocking=False):
        print("Show already running, wait...")
        return

    try:
        subprocess.Popen(["mpg123", "-q", pickle_rick_long])
        motor.on()
        sleep(0.1)
        motor.off()

        motor.value = 0.1
        print("Full show: Motor ON, LEDs starting...")

        for _ in range(15):
            for _ in range(len(leds)):
                led = random.choice(leds)
                led.on()
                sleep(0.05)
                led.off()
            sleep(0.02)

        motor.off()
        print("Full show: Motor OFF, finishing LEDs...")

        for _ in range(10): 
            for led in leds:
                led.on()
            sleep(0.3)
            for led in leds:
                led.off()
            sleep(0.3)

        print("Full show complete.")

    finally:
        show_lock.release()

if __name__ == "__main__":
    full_show()