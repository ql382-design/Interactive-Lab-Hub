#!/usr/bin/env python3
"""
Gesture Drum Machine
MediaPipe Hands + SparkFun Qwiic GPIO + Pygame Audio
Four colored LEDs (orange, white, yellow, blue) represent different drum hits.
"""

import cv2
import mediapipe as mp
import numpy as np
import sys
import time
import qwiic_gpio
import pygame

# ----------------------------
# Initialize Qwiic GPIO
# ----------------------------
gpio = qwiic_gpio.QwiicGPIO()

if not gpio.isConnected():
    print("❌ Qwiic GPIO not detected. Check SDA/SCL wiring and power.")
    sys.exit(1)

gpio.begin()

# LED pin mapping (adjust to your wiring)
ORANGE_PIN = 0   # Kick
WHITE_PIN  = 1   # Snare
YELLOW_PIN = 2   # Hi-hat
BLUE_PIN   = 3   # Tom

for pin in [ORANGE_PIN, WHITE_PIN, YELLOW_PIN, BLUE_PIN]:
    gpio.pinMode(pin, gpio.GPIO_OUT)
    gpio.digitalWrite(pin, gpio.GPIO_LO)  # default OFF

print("✅ Qwiic GPIO ready at I2C address 0x27")

# ----------------------------
# Initialize Audio (Pygame)
# ----------------------------
pygame.mixer.init()
sounds = {
    "kick":  pygame.mixer.Sound("drum_sounds/kick.wav"),
    "snare": pygame.mixer.Sound("drum_sounds/snare.wav"),
    "hihat": pygame.mixer.Sound("drum_sounds/hihat.wav"),
    "tom":   pygame.mixer.Sound("drum_sounds/tom.wav")
}

def play(sound_key):
    """Play a drum sample."""
    if sound_key in sounds:
        sounds[sound_key].play()

# ----------------------------
# Initialize MediaPipe Hands
# ----------------------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

# ----------------------------
# LED helper functions
# ----------------------------
def led_on(pin):
    gpio.digitalWrite(pin, gpio.GPIO_HI)

def led_off(pin):
    gpio.digitalWrite(pin, gpio.GPIO_LO)

def all_off():
    for p in [ORANGE_PIN, WHITE_PIN, YELLOW_PIN, BLUE_PIN]:
        led_off(p)

# ----------------------------
# Debounce setup
# ----------------------------
last_state = None
last_change_time = 0
DEBOUNCE_DELAY = 0.3  # seconds between beats

# ----------------------------
# Main loop
# ----------------------------
print("🥁 Starting Gesture Drum Machine (Press ESC to exit)")

while True:
    ret, img = cap.read()
    if not ret:
        break

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    state = "Rest"

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)
            h, w, _ = img.shape
            # Extract landmark coordinates
            x_thumb, y_thumb = int(handLms.landmark[4].x * w), int(handLms.landmark[4].y * h)
            x_index, y_index = int(handLms.landmark[8].x * w), int(handLms.landmark[8].y * h)
            x_pinky, y_pinky = int(handLms.landmark[20].x * w), int(handLms.landmark[20].y * h)

            pinch_dist = np.hypot(x_index - x_thumb, y_index - y_thumb)
            pinky_dist = np.hypot(x_pinky - x_thumb, y_pinky - y_thumb)

            # Gesture logic → map to drums
            if pinch_dist < 40:
                state = "Tom"           # 🤏 = tom
            elif pinky_dist < 50:
                state = "HiHat"         # 🤙 = hi-hat
            elif pinch_dist > 120:
                state = "Snare"         # 🖐 = snare
            elif 50 < pinch_dist < 90 and 50 < pinky_dist < 90:
                state = "Kick"          # ✊ = kick
            else:
                state = "Rest"

    # ----------------------------
    # Debounced updates
    # ----------------------------
    if state != last_state and (time.time() - last_change_time) > DEBOUNCE_DELAY:
        last_state = state
        last_change_time = time.time()
        all_off()

        if state == "Kick":
            led_on(ORANGE_PIN)
            play("kick")
            print("Kick 🧡")
        elif state == "Snare":
            led_on(WHITE_PIN)
            play("snare")
            print("Snare 🤍")
        elif state == "HiHat":
            led_on(YELLOW_PIN)
            play("hihat")
            print("Hi-hat 💛")
        elif state == "Tom":
            led_on(BLUE_PIN)
            play("tom")
            print("Tom 💙")
        else:
            print("Rest (All OFF)")

    # ----------------------------
    # Display
    # ----------------------------
    cv2.putText(img, f"State: {state}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Gesture Drum Machine", img)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC key
        break

# ----------------------------
# Cleanup
# ----------------------------
all_off()
cap.release()
cv2.destroyAllWindows()
print("Program ended — all LEDs OFF.")

