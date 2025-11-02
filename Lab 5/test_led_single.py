import time, qwiic_gpio
gpio = qwiic_gpio.QwiicGPIO()
if not gpio.isConnected():
    print("? Qwiic GPIO not detected ? check SDA/SCL!")
else:
    print("? Detected Qwiic GPIO at address", hex(gpio.address))

gpio.begin()
pin = 0  # try the pin your orange LED is on
gpio.pinMode(pin, gpio.GPIO_OUT)

print("Blink test on pin", pin)
for i in range(3):
    gpio.digitalWrite(pin, gpio.GPIO_HI)  # should turn LED ON
    time.sleep(0.5)
    gpio.digitalWrite(pin, gpio.GPIO_LO)  # should turn LED OFF
    time.sleep(0.5)
print("Test complete")
