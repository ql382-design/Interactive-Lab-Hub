import time
import qwiic_gpio

print("Initializing Qwiic GPIO test...")

gpio = qwiic_gpio.QwiicGPIO()

# ? ??????? isConnected() ??? is_connected()
if not gpio.isConnected():
    print("? Qwiic GPIO board not detected. Check your SDA/SCL wiring and power!")
else:
    print("? Qwiic GPIO board connected successfully.")

# Example: blink pins 0?3 (assuming 4 LEDs)
for pin in range(4):
    gpio.pinMode(pin, gpio.OUTPUT)
    print(f"Blinking LED on pin {pin}...")
    for i in range(3):
        gpio.digitalWrite(pin, gpio.LOW)   # LED ON (current-sinking)
        time.sleep(0.2)
        gpio.digitalWrite(pin, gpio.HIGH)  # LED OFF
        time.sleep(0.2)

print("? Test complete.")
