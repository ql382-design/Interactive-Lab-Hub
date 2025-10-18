from qwiic_button import QwiicButtonWrapper
import time
btn = QwiicButtonWrapper()
print("Press the Qwiic Button... Ctrl+C to exit")
while True:
    if btn.pressed():
        print("Pressed!")
        btn.led_blink()
    time.sleep(0.01)
