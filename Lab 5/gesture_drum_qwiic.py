#!/usr/bin/env python3
"""
Gesture Drum Synthesizer v4
Very clear distinction between Fist ✊ and OneFinger ☝️
Gestures: Pinch 🤏 / Fist ✊ / OneFinger ☝️ / OpenHand 🖐
Pins: Blue=P0, Yellow=P1, White=P6, Orange=P7
Logic: HIGH = ON (your Qwiic GPIO board)
"""

import cv2
import mediapipe as mp
import numpy as np
import time
import sys
import qwiic_gpio
import pygame

# ---------------------------- GPIO Initialization ----------------------------
gpio = qwiic_gpio.QwiicGPIO()
if not gpio.isConnected():
    print("❌ Qwiic GPIO not detected. Check SDA/SCL wiring.")
    sys.exit(1)
gpio.begin()

# LED pin mapping
BLUE_PIN, YELLOW_PIN, WHITE_PIN, ORANGE_PIN = 0, 1, 6, 7
pins = [BLUE_PIN, YELLOW_PIN, WHITE_PIN, ORANGE_PIN]

# Set all pins as outputs and turn them OFF initially
for p in pins:
    gpio.pinMode(p, gpio.GPIO_OUT)
    gpio.digitalWrite(p, gpio.GPIO_LO)
print("✅ Qwiic GPIO ready (HIGH = ON logic)\n")

# ---------------------------- Audio Initialization ----------------------------
pygame.mixer.init()
sounds = {
    "pinch": pygame.mixer.Sound("drum_sounds/snare.wav"),
    "fist":  pygame.mixer.Sound("drum_sounds/kick.wav"),
    "one":   pygame.mixer.Sound("drum_sounds/hihat.wav"),
    "open":  pygame.mixer.Sound("drum_sounds/tom.wav")
}
print("🎵 Drum sounds loaded successfully\n")

# ---------------------------- MediaPipe Hands ----------------------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

# ---------------------------- LED Helpers ----------------------------
def led_on(pin):
    gpio.digitalWrite(pin, gpio.GPIO_HI)

def led_off(pin):
    gpio.digitalWrite(pin, gpio.GPIO_LO)

def turn_all_off():
    for p in pins:
        led_off(p)

# ---------------------------- Gesture Detection Helpers ----------------------------
def distance(handLms, p1, p2, w, h):
    """Helper to compute Euclidean distance between two landmarks."""
    x1, y1 = int(handLms.landmark[p1].x * w), int(handLms.landmark[p1].y * h)
    x2, y2 = int(handLms.landmark[p2].x * w), int(handLms.landmark[p2].y * h)
    return np.hypot(x2 - x1, y2 - y1)

def is_fist(handLms, h, w):
    """Detects true fist: all fingertips close to the palm."""
    tips = [8, 12, 16, 20]  # index, middle, ring, pinky
    palm_x, palm_y = int(handLms.landmark[0].x * w), int(handLms.landmark[0].y * h)
    dists = [np.hypot(int(handLms.landmark[t].x * w) - palm_x,
                      int(handLms.landmark[t].y * h) - palm_y) for t in tips]
    avg_dist = np.mean(dists)
    return avg_dist < 120  # all fingers bent close to palm

def is_onefinger(handLms, h, w):
    """
    Detects only the index finger extended.
    Uses relative distance difference: index farther than others.
    """
    tips = [8, 12, 16, 20]  # index, middle, ring, pinky
    palm_x, palm_y = int(handLms.landmark[0].x * w), int(handLms.landmark[0].y * h)
    dists = [np.hypot(int(handLms.landmark[t].x * w) - palm_x,
                      int(handLms.landmark[t].y * h) - palm_y) for t in tips]
    index_dist = dists[0]
    others_avg = np.mean(dists[1:])
    # index must be significantly longer than others
    diff = index_dist - others_avg
    return index_dist > 150 and diff > 80  # clearly separated

def is_openhand(handLms, h, w):
    """Detects full open hand (all five fingers extended)."""
    tips = [4, 8, 12, 16, 20]
    palm_x, palm_y = int(handLms.landmark[0].x * w), int(handLms.landmark[0].y * h)
    far = 0
    for t in tips:
        dist = np.hypot(int(handLms.landmark[t].x * w) - palm_x,
                        int(handLms.landmark[t].y * h) - palm_y)
        if dist > 150:
            far += 1
    return far >= 5  # all five fingers extended

# ---------------------------- Main Loop ----------------------------
last_state = None
last_change_time = 0
DEBOUNCE = 0.25  # seconds

print("🎬 Gesture Drum v4 running — press ESC to exit")

while True:
    ret, img = cap.read()
    if not ret:
        break

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    current_state = "Idle"

    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand, mp_hands.HAND_CONNECTIONS)
            h, w, _ = img.shape

            # --- Gesture recognition ---
            x_thumb, y_thumb = int(hand.landmark[4].x * w), int(hand.landmark[4].y * h)
            x_index, y_index = int(hand.landmark[8].x * w), int(hand.landmark[8].y * h)
            pinch_dist = np.hypot(x_index - x_thumb, y_index - y_thumb)

            if pinch_dist < 40:
                current_state = "Pinch"
            elif is_fist(hand, h, w):
                current_state = "Fist"
            elif is_onefinger(hand, h, w):
                current_state = "OneFinger"
            elif is_openhand(hand, h, w):
                current_state = "OpenHand"

    # ------------------- Debounce and Actuate -------------------
    if current_state != last_state and (time.time() - last_change_time) > DEBOUNCE:
        last_state = current_state
        last_change_time = time.time()
        turn_all_off()

        if current_state == "Pinch":
            led_on(YELLOW_PIN)
            sounds["pinch"].play()
            print("🤏 Pinch → Snare + Yellow")
        elif current_state == "Fist":
            led_on(ORANGE_PIN)
            sounds["fist"].play()
            print("✊ Fist → Kick + Orange")
        elif current_state == "OneFinger":
            led_on(BLUE_PIN)
            sounds["one"].play()
            print("☝️ OneFinger → HiHat + Blue")
        elif current_state == "OpenHand":
            led_on(WHITE_PIN)
            sounds["open"].play()
            print("🖐 OpenHand → Tom + White")
        else:
            print("🫳 Idle")

    # ------------------- Display -------------------
    cv2.putText(img, f"State: {current_state}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Gesture Drum v4", img)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC
        break

# ---------------------------- Cleanup ----------------------------
turn_all_off()
cap.release()
cv2.destroyAllWindows()
pygame.mixer.quit()
print("🛑 End — all LEDs off, mixer closed.")
