# 文件名: test_apds9960.py
import time
import board
import busio
import adafruit_apds9960.apds9960

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_apds9960.apds9960.APDS9960(i2c)
sensor.enable_gesture = True

print("Move your hand in front of the sensor!")

while True:
    gesture = sensor.gesture()
    if gesture != 0:
        print("Gesture detected:", gesture)
    time.sleep(0.2)
