from gpiozero import PWMOutputDevice, LED
from time import sleep
import subprocess

# Motor on GPIO18
motor = PWMOutputDevice(18)

# LEDs on these GPIOs
# led_pins = [22, 19, 6, 13, 5, 26] #counter-clockwise
led_pins = [26, 5, 13, 6, 19, 22] #clockwise
leds = [LED(pin) for pin in led_pins]

sound_file = "/home/admin/audio_files/pickle_rick_loud.mp3"

subprocess.Popen(["mpg123", "-q", sound_file])

motor.value = 0.25
print("Motor ON, LEDs starting...")

# Light show
for _ in range(15):  
    for led in leds:
        led.on()
        sleep(0.07) 
        led.off()
    sleep(0.02)

motor.off()
print("Motor OFF, finishing LED show...")

x = 0
while x < 5:
    x = x + 1
    for led in leds:
        led.on()
    sleep(1)
    for led in leds:
        led.off()
    sleep(1)

print("Show complete.")