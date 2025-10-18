# Wrapper for SparkFun Qwiic Button
import time
try:
    import qwiic_button
except ImportError:
    raise SystemExit("Please install: pip3 install qwiic_button")

DEFAULT_ADDR = 0x6F

class QwiicButtonWrapper:
    def __init__(self, address=DEFAULT_ADDR):
        self.btn = qwiic_button.QwiicButton(address)
        if not self.btn.begin():
            raise RuntimeError("Qwiic Button not detected. Check wiring/address.")
        self.btn.LED_off()
        self._last_state = False
        self._debounce_ms = 40
        self._last_time = 0

    def pressed(self):
        # Return True once per press (debounced edge).
        now = int(time.time() * 1000)
        state = self.btn.is_button_pressed()
        pressed_edge = False
        if state and not self._last_state and (now - self._last_time) > self._debounce_ms:
            pressed_edge = True
            self._last_time = now
        self._last_state = state
        return pressed_edge

    def led_blink(self, on_ms=60, off_ms=60, times=3):
        for _ in range(times):
            self.btn.LED_on(0xFF)
            time.sleep(on_ms/1000.0)
            self.btn.LED_off()
            time.sleep(off_ms/1000.0)

if __name__ == "__main__":
    btn = QwiicButtonWrapper()
    print("Press the Qwiic Button; Ctrl+C to exit.")
    try:
        while True:
            if btn.pressed():
                print("Button pressed!")
                btn.led_blink()
            time.sleep(0.01)
    except KeyboardInterrupt:
        pass
