# ✅ FINAL CONFIRMED VERSION — Compatible with your environment
import time

try:
    import qwiic_button  # This should work with your installed sparkfun-qwiic-button 2.0.3
    ButtonClass = qwiic_button.QwiicButton
except Exception:
    raise SystemExit(
        "❌ QwiicButton class not found. Try reinstalling with: pip install sparkfun-qwiic-button"
    )

DEFAULT_ADDR = 0x6F

class QwiicButtonWrapper:
    def __init__(self, address=DEFAULT_ADDR):
        self.btn = ButtonClass(address)
        if not self.btn.begin():
            raise RuntimeError("❌ Qwiic Button not detected. Check I2C or address.")
        # Turn off internal LED by default
        if hasattr(self.btn, "LED_off"):
            self.btn.LED_off()

        self._last_state = False
        self._debounce_ms = 40
        self._last_time = 0

    def pressed(self):
        """Return True once per clean button press (debounced edge trigger)."""
        now = int(time.time() * 1000)
        state = self.btn.is_button_pressed()
        pressed_edge = False

        if state and not self._last_state and (now - self._last_time) > self._debounce_ms:
            pressed_edge = True
            self._last_time = now

        self._last_state = state
        return pressed_edge

    # You can remove this if you don't want even the onboard LED feedback
    def led_feedback(self, duration_ms=80):
        """Optional: blink internal LED once for debug."""
        if hasattr(self.btn, "LED_on") and hasattr(self.btn, "LED_off"):
            self.btn.LED_on(255)
            time.sleep(duration_ms / 1000)
            self.btn.LED_off()

if __name__ == "__main__":
    btn = QwiicButtonWrapper()
    print("Press the Qwiic Button... Ctrl+C to exit")
    try:
        while True:
            if btn.pressed():
                print("Pressed!")
                btn.led_feedback()
            time.sleep(0.01)
    except KeyboardInterrupt:
        pass
