import time
import smbus2

BUS_NUMBER = 1

def scan_i2c():
    bus = smbus2.SMBus(BUS_NUMBER)
    found = []
    for addr in range(0x03, 0x78):
        try:
            bus.write_quick(addr)
            found.append(addr)
        except OSError:
            pass
    bus.close()
    if found:
        print("I2C devices:"," ".join(f"0x{a:02x}" for a in found))
    else:
        print("No I2C devices found.")

if __name__ == "__main__":
    while True:
        scan_i2c()
        time.sleep(3)
