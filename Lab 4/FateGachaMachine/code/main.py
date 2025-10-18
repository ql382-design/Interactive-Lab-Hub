# Main fate ritual: Encoder (tension) + Qwiic Button (commit) + OLED + Bluetooth speaker
import time
from i2c_encoder import I2CEncoder
from qwiic_button import QwiicButtonWrapper
from oled_display import show_text, clear
from fate_audio import play_clip

TICK_INTERVAL = 0.02
CHAOS_THRESHOLD = 30
YES_THRESHOLD = 6
NO_THRESHOLD  = -6
COOLDOWN_SEC  = 1.2

def pick_fate(score:int):
    if abs(score) >= CHAOS_THRESHOLD:
        return "CHAOS"
    if score >= YES_THRESHOLD:
        return "YES"
    if score <= NO_THRESHOLD:
        return "NO"
    return "DELAY"

def main():
    enc = I2CEncoder()
    btn = QwiicButtonWrapper()
    tension = 0
    last_show = 0
    show_text("Fate Gacha", "Twist to tune...")
    try:
        while True:
            d = enc.get_delta()
            if d:
                tension += d
            now = time.time()
            if now - last_show > 0.08:
                label = "tension:" + ("+" if tension>=0 else "") + str(tension)
                show_text("Fate Tuning...", label)
                last_show = now
            if btn.pressed():
                fate = pick_fate(tension)
                if fate == "YES":
                    show_text("FATE:", "YES")
                    play_clip("yes")
                elif fate == "NO":
                    show_text("FATE:", "NO")
                    play_clip("no")
                elif fate == "CHAOS":
                    show_text("FATE:", "⚠ CHAOS")
                    play_clip("chaos")
                else:
                    show_text("FATE:", "DELAY")
                    play_clip("delay")
                time.sleep(COOLDOWN_SEC)
                tension = 0
                show_text("Fate Gacha", "Twist to tune...")
            time.sleep(TICK_INTERVAL)
    except KeyboardInterrupt:
        clear()
        print("Bye.")

if __name__ == "__main__":
    main()
