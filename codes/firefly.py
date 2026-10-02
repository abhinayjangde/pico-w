from machine import Pin
import time

# Initialize GP13 as an output
gp13 = Pin(13, Pin.OUT)

# Blink loop using toggle
while True:
    gp13.toggle()  # Switches the state automatically
    time.sleep(0.5)
