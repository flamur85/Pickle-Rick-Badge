from gpiozero import Button
from signal import pause

buttons = {
    "Button 1": Button(20),
    "Button 2": Button(16),
    "Button 3": Button(8),   # GPIO8, not physical pin
    "Button 4": Button(12),
    "Button 5": Button(21)
}

for name, btn in buttons.items():
    btn.when_pressed = (lambda n: lambda: print(f"{n} pressed"))(name)

print("Press buttons to test...")
pause()