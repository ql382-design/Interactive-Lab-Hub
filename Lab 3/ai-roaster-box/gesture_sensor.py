# gesture_sensor.py
import time
import board
import busio
import adafruit_apds9960.apds9960

class GestureSensor:
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_apds9960.apds9960.APDS9960(i2c)
        self.sensor.enable_proximity = True
        self.sensor.enable_gesture = True

        # --- Increase LED and gain for better range ---
        self.sensor.proximity_gain = 3       # 0–3, higher = more sensitive
        self.sensor.led_drive = 0            # 0=100 mA (brightest)
        self.sensor.gesture_gain = 3         # max gain
        self.sensor.gesture_fifo_threshold = 1
        self.sensor.gesture_proximity_threshold = 10
        self.sensor.gesture_exit_threshold = 10

        print("Gesture sensor initialized (high sensitivity mode).")

    def detect_wave(self):
        """Wait for any gesture (up/down/left/right)."""
        gesture_map = {
            0x01: "UP",
            0x02: "DOWN",
            0x03: "LEFT",
            0x04: "RIGHT"
        }
        gesture = None
        while gesture is None:
            g = self.sensor.gesture()
            if g in gesture_map:
                gesture = gesture_map[g]
                print("Gesture detected:", gesture)
                return gesture
            time.sleep(0.05)
