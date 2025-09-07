from gpiozero import PWMOutputDevice, LED, Button
from time import sleep
import subprocess
import time
from signal import pause
from threading import Lock

motor = PWMOutputDevice(18)

# LEDs on these GPIOs (clockwise)
led_pins = [26, 5, 13, 6, 19, 22]
leds = [LED(pin) for pin in led_pins]

# Buttons
buttons = {
    "Button 1": Button(20),
    "Button 2": Button(16),
    "Button 3": Button(21),
    "Button 4": Button(12),
    "Button 5": Button(25)
}

# Sound file for full show
pickle_rick_long = "/home/admin/audio_files/pr_long.mp3"
ohyea = "/home/admin/audio_files/ohyea_loud.mp3"

# Lock to prevent overlapping shows
show_lock = Lock()

# Reset all LEDs at start
for led in leds:
    led.off()

# Full show: Button 1
def full_show():
    if not show_lock.acquire(blocking=False):
        print("Show already running, wait...")
        return

    try:
        subprocess.Popen(["mpg123", "-q", pickle_rick_long])

        motor.value = 0.25
        print("Full show: Motor ON, LEDs starting...")

        for _ in range(15):
            for led in leds:
                led.on()
                sleep(0.07)
                led.off()
            sleep(0.02)

        motor.off()
        print("Full show: Motor OFF, finishing LEDs...")

        for _ in range(5):
            for led in leds:
                led.on()
            sleep(1)
            for led in leds:
                led.off()
            sleep(1)

        print("Full show complete.")

    finally:
        show_lock.release()

# Mini show: Button 2
def mini_show():
    if not show_lock.acquire(blocking=False):
        print("Show already running, wait...")
        return

    try:
        print("Mini show started!")

        subprocess.Popen(["mpg123", "-q", ohyea])


        pulse_steps = 30 
        duration = 10 
        step_time = duration / (pulse_steps * 2)

        start_time = time.time()
        while time.time() - start_time < duration:
            # Ramp up
            for i in range(pulse_steps):
                motor.value = i / pulse_steps * 0.4 
                # Bouncing LED pattern
                for idx, led in enumerate(leds):
                    if idx % 2 == i % 2:
                        led.on()
                    else:
                        led.off()
                sleep(step_time)

            for i in reversed(range(pulse_steps)):
                motor.value = i / pulse_steps * 0.25
                for idx, led in enumerate(leds):
                    if idx % 2 == i % 2:
                        led.on()
                    else:
                        led.off()
                sleep(step_time)

        motor.off()
        for led in leds:
            led.off()

        print("Mini show complete.")

    finally:
        show_lock.release()

# Assign buttons
buttons["Button 1"].when_pressed = full_show
buttons["Button 2"].when_pressed = mini_show

print("Press Button 1 for full show or Button 2 for mini show.")
pause()