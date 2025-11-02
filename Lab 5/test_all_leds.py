#!/usr/bin/env python3
"""
Final Qwiic GPIO LED Test
Pins: Blue=P0, Yellow=P1, White=P6, Orange=P7
Logic: LOW = ON (current-sinking)
"""

import time, qwiic_gpio, sys

gpio = qwiic_gpio.QwiicGPIO()
if not gpio.isConnected():
    print("? Qwiic GPIO not detected. Check SDA/SCL and power.")
    sys.exit(1)

gpio.begin()
print(f"? Qwiic GPIO detected at {hex(gpio.address)} (LOW=ON logic)\n")

# LED pin mapping
BLUE_PIN   = 0
YELLOW_PIN = 1
WHITE_PIN  = 6
ORANGE_PIN = 7

pins = [BLUE_PIN, YELLOW_PIN, WHITE_PIN, ORANGE_PIN]
labels = ["? Blue (P0)", "? Yellow (P1)", "? White (P6)", "? Orange (P7)"]

# Init all OFF
for p in pins:
    gpio.pinMode(p, gpio.GPIO_OUT)
    gpio.digitalWrite(p, gpio.GPIO_HI)

print("? Sequential LED blink test...\n")
for p, label in zip(pins, labels):
    print(f"Testing {label} ...")
    gpio.digitalWrite(p, gpio.GPIO_LO)
    time.sleep(0.5)
    gpio.digitalWrite(p, gpio.GPIO_HI)
    time.sleep(0.3)

print("\n? All LEDs ON for 2 seconds...")
for p in pins:
    gpio.digitalWrite(p, gpio.GPIO_LO)
time.sleep(2)
for p in pins:
    gpio.digitalWrite(p, gpio.GPIO_HI)

print("? All OFF ? test complete.")
