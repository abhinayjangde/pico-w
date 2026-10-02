from machine import Pin
import time

# Initialize GP13 as an output
led = Pin(13, Pin.OUT)

# Blink loop using toggle
while True:
    led.toggle()  # Switches the state automatically
    time.sleep(0.2)
