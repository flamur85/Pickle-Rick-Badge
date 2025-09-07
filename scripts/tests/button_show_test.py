from gpiozero import PWMOutputDevice, LED, Button
from time import sleep
import subprocess
from signal import pause

# Motor on GPIO18
motor = PWMOutputDevice(18)

led_pins = [22, 19, 6, 13, 5, 26]
leds = [LED(pin) for pin in led_pins]

button = Button(20)

sound_file = "/home/admin/audio_files/pickle_rick_loud.mp3"

def run_show():
    print("Show starting...")
    subprocess.Popen(["mpg123", "-q", sound_file])

    motor.value = 0.21

    for _ in range(15):
        for led in leds:
            led.on()
            sleep(0.07)
            led.off()
        sleep(0.02)

    motor.off()

    for led in leds:
        led.on()
    sleep(8)
    for led in leds:
        led.off()

    print("Show complete.")

button.when_pressed = run_show

print("Press the button to start the show!")
pause() 