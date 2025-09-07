from gpiozero import PWMOutputDevice
from time import sleep

# Motor on GPIO18 with PWM
motor = PWMOutputDevice(18)

print("Motor test with PWM...")

motor.on()
sleep(0.175)

motor.value = 0.07
sleep(5)

motor.off()
print("Done. Motor stopped.")
