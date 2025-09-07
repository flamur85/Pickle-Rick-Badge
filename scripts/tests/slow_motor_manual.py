from gpiozero import OutputDevice
from time import sleep

# Motor on GPIO18
motor = OutputDevice(18)

print("Starting motor test...")

motor.on()
sleep(0.175)

for i in range(5):
    print(f"Cycle {i+1}: Motor ON")

    motor.off()
    sleep(1)

    motor.on()
    sleep(0.075)

    print(f"Cycle {i+1}: Motor OFF")

print("Done. Motor stopped.")
motor.off()