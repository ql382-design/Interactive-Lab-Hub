# Wrapper for Adafruit I2C Rotary Encoder (seesaw STEMMA QT/Qwiic)
import time
import board
import busio

try:
    from adafruit_seesaw.seesaw import Seesaw
    from adafruit_seesaw import rotaryio, digitalio
except ImportError:
    raise SystemExit("Please install: pip3 install adafruit-circuitpython-seesaw")

I2C_ADDR = 0x36  # default for Adafruit I2C encoder breakout

class I2CEncoder:
    def __init__(self, address=I2C_ADDR):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.ss = Seesaw(i2c, addr=address)
        self.encoder = rotaryio.IncrementalEncoder(self.ss)
        self.last = self.encoder.position
    
    def get_delta(self):
        pos = self.encoder.position
        delta = pos - self.last
        self.last = pos
        return delta
    
    def get_position(self):
        return self.encoder.position

if __name__ == "__main__":
    enc = I2CEncoder()
    print("Rotate the encoder; Ctrl+C to exit.")
    try:
        while True:
            d = enc.get_delta()
            if d != 0:
                print("delta:", d, " pos:", enc.get_position())
            time.sleep(0.02)
    except KeyboardInterrupt:
        print("Bye")
