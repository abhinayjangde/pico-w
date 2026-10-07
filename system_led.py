from machine import Pin


led = Pin('LED', Pin.OUT)  # Initialize the onboard LED as an output

# led.value(0)  # Turn the LED on

# led.on()  # Turn the LED on
led.off()  # Turn the LED off