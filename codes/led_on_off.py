import machine
import time

led = machine.Pin('LED', machine.Pin.OUT)
# while(True):
#     led.on()
#     time.sleep(0.5)
#     led.off()
#     time.sleep(0.5)
# led.value(0)
# led.value(1)
# while True:
#     led.toggle()
#     time.sleep(1)

while True:
    led.toggle()
    # led.off()
    # time.sleep(1)
    # led.on()
    # time.sleep(0.1)
    time.sleep(1)


