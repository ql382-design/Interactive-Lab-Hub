from i2c_encoder import I2CEncoder
import time
enc = I2CEncoder()
print("Rotate encoder; Ctrl+C to exit")
while True:
    d = enc.get_delta()
    if d:
        print("delta:", d, "pos:", enc.get_position())
    time.sleep(0.01)
