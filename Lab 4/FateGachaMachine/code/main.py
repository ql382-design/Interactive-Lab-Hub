# main.py — Fate Ritual System (Encoder + Qwiic Button + OLED + Bluetooth Speaker)
# Behavior:
# - Rotate the I²C encoder to "charge" fate tension (visualized on OLED).
# - Press the Qwiic Button to commit fate:
#     1) Play a subtle click sound (click.wav) for tactile confirmation.
#     2) Play fate sound (yes/no/delay/chaos).
#     3) Pause 0.3s (ritual timing).
#     4) Play witch-voice line (yes_voice/no_voice/delay_voice/chaos_voice).
#
# Dependencies:
#   pip install adafruit-circuitpython-ssd1306 adafruit-circuitpython-seesaw qwiic_button pillow smbus2
# Make sure your Bluetooth speaker is connected and default sink is set.

import time
import qwiic_button  # Official SparkFun library
from i2c_encoder import I2CEncoder
from oled_display import show_text, clear
from fate_audio import play_clip, play_sequence, warmup

# ---------- Tunable parameters ----------
TICK_INTERVAL   = 0.02
OLED_RATE_LIMIT = 0.08

CHAOS_THRESHOLD = 30
YES_THRESHOLD   = 6
NO_THRESHOLD    = -6

COOLDOWN_SEC    = 1.2
BUTTON_DEBOUNCE_MS = 90
VOICE_PAUSE_SEC = 0.3  # ritual pause between fate beep and witch voice
CLICK_PAUSE_SEC = 0.15 # tiny pause after click (feel mechanical)

def pick_fate(score: int) -> str:
    """Map a tension score to a fate outcome."""
    if abs(score) >= CHAOS_THRESHOLD:
        return "CHAOS"
    if score >= YES_THRESHOLD:
        return "YES"
    if score <= NO_THRESHOLD:
        return "NO"
    return "DELAY"

def reveal_with_audio(fate: str):
    """
    Ordered playback requested by user:
      click → fate_beep → 0.3s pause → witch_voice
    """
    # click
    play_clip("button-2")
    time.sleep(CLICK_PAUSE_SEC)

    # fate beep + witch voice
    if fate == "YES":
        play_clip("yes")
        time.sleep(VOICE_PAUSE_SEC)
        play_clip("yes_voice")
    elif fate == "NO":
        play_clip("no")
        time.sleep(VOICE_PAUSE_SEC)
        play_clip("no_voice")
    elif fate == "CHAOS":
        play_clip("chaos")
        time.sleep(VOICE_PAUSE_SEC)
        play_clip("chaos_voice")
    else:  # DELAY
        play_clip("delay")
        time.sleep(VOICE_PAUSE_SEC)
        play_clip("delay_voice")

def main():
    # --- Warm audio to avoid first-play truncation ---
    warmup()

    # --- Initialize devices ---
    enc = I2CEncoder()

    btn = qwiic_button.QwiicButton()  # default 0x6F
    if not btn.begin():
        raise RuntimeError("Qwiic Button not detected. Check I2C wiring/address (0x6F).")

    # UI
    clear()
    show_text("Fate Gacha", "Twist to tune...")

    tension = 0
    last_oled = 0.0
    last_btn_state = False
    last_btn_time_ms = 0

    try:
        while True:
            # 1) Encoder → tension
            try:
                delta = enc.get_delta()
            except OSError:
                # I2C hiccup resilience: brief sleep and continue
                time.sleep(0.02)
                continue
            if delta:
                tension += delta

            # 2) OLED rate-limited update
            now = time.time()
            if now - last_oled > OLED_RATE_LIMIT:
                label = f"tension:{'+' if tension >= 0 else ''}{tension}"
                show_text("Fate Tuning...", label)
                last_oled = now

            # 3) Button edge detection + debounce
            level = btn.is_button_pressed()  # True when pressed
            now_ms = int(now * 1000)
            pressed_edge = False
            if level and (not last_btn_state) and (now_ms - last_btn_time_ms > BUTTON_DEBOUNCE_MS):
                pressed_edge = True
                last_btn_time_ms = now_ms
            last_btn_state = level

            # 4) Commit fate on press
            if pressed_edge:
                fate = pick_fate(tension)

                # OLED reveal
                if fate == "YES":
                    show_text("FATE:", "YES")
                elif fate == "NO":
                    show_text("FATE:", "NO")
                elif fate == "CHAOS":
                    show_text("FATE:", "⚠ CHAOS")
                else:
                    show_text("FATE:", "DELAY")

                # Audio reveal: click → beep → pause → witch voice
                reveal_with_audio(fate)

                # cooldown & reset
                time.sleep(COOLDOWN_SEC)
                tension = 0
                show_text("Fate Gacha", "Twist to tune...")

            time.sleep(TICK_INTERVAL)

    except KeyboardInterrupt:
        clear()
        print("Bye.")

if __name__ == "__main__":
    main()
