# OLED helpers for SSD1306 128x32 via I2C
import time
import board
import busio
from PIL import Image, ImageDraw, ImageFont

try:
    import adafruit_ssd1306
except ImportError:
    raise SystemExit("Please install: pip3 install adafruit-circuitpython-ssd1306 pillow")

I2C_ADDR = 0x3C
WIDTH = 128
HEIGHT = 32

_i2c = None
_disp = None

def _init_display():
    global _i2c, _disp
    if _disp is not None:
        return _disp
    _i2c = busio.I2C(board.SCL, board.SDA)
    _disp = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, _i2c, addr=I2C_ADDR)
    _disp.fill(0)
    _disp.show()
    return _disp

def clear():
    d = _init_display()
    d.fill(0)
    d.show()

def show_text(line1:str="", line2:str=""):
    d = _init_display()
    image = Image.new("1", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)
    y = 0
    if line1:
        draw.text((0, y), str(line1), fill=255)
        y += 16
    if line2:
        draw.text((0, y), str(line2), fill=255)
    d.image(image)
    d.show()

if __name__ == "__main__":
    show_text("Fate System", "READY")
    time.sleep(2)
    clear()
