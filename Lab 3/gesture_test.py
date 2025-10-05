import time
import board
import busio
from adafruit_apds9960.apds9960 import APDS9960

# Initialize I2C connection
i2c = busio.I2C(board.SCL, board.SDA)

# Wait until the I2C bus is ready
while not i2c.try_lock():
    pass
print(" I2C bus locked successfully.")
i2c.unlock()

# Create sensor instance
sensor = APDS9960(i2c)

# Enable proximity and gesture detection (order matters)
sensor.enable_proximity = True
time.sleep(0.5)
sensor.enable_gesture = True
time.sleep(0.5)

print("Gesture detection started! Try waving your hand...")

while True:
    try:
        gesture = sensor.gesture()
        if gesture:
            print("Detected gesture:", gesture)
        time.sleep(0.1)
    except OSError as e:
        # Handle temporary I2C communication errors gracefully
        print(" I2C read error:", e)
        time.sleep(0.5)
