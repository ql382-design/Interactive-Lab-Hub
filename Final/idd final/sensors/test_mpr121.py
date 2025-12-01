import time
import board
import busio
import adafruit_mpr121

# Initialize I2C and sensor
i2c = busio.I2C(board.SCL, board.SDA)
mpr121 = adafruit_mpr121.MPR121(i2c)

print("MPR121 Touch Test Started!")
print("Touch electrodes 0–11")

while True:
    for i in range(12):
        if mpr121[i].value:
            print(f"Electrode {i} touched!")
    time.sleep(0.1)

