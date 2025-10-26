#!/usr/bin/env python3
"""
MediaPipe + Qwiic GPIO LED Control (Debounced, Correct Logic)
Detect hand gestures and control three LEDs (yellow, white, blue)
via SparkFun Qwiic GPIO on Raspberry Pi.
"""

import cv2
import mediapipe as mp
import numpy as np
import sys
import time
import qwiic_gpio

# ----------------------------
# Initialize Qwiic GPIO
# ----------------------------
gpio = qwiic_gpio.QwiicGPIO()

if not gpio.isConnected():
    print("Qwiic GPIO not detected. Check wiring.")
    sys.exit(1)

gpio.begin()

# LED pin mapping (based on your wiring)
YELLOW_PIN = 0
WHITE_PIN = 2
BLUE_PIN = 5

for pin in [YELLOW_PIN, WHITE_PIN, BLUE_PIN]:
    gpio.pinMode(pin, gpio.GPIO_OUT)
    gpio.digitalWrite(pin, gpio.GPIO_LO)  # default OFF (reversed logic)

print("Qwiic GPIO ready at I2C address 0x27")

# ----------------------------
# Initialize MediaPipe Hands
# ----------------------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

# ----------------------------
# LED control helpers (reversed logic)
# ----------------------------
def led_on(pin):
    gpio.digitalWrite(pin, gpio.GPIO_HI)  # HIGH = ON

def led_off(pin):
    gpio.digitalWrite(pin, gpio.GPIO_LO)  # LOW = OFF

def turn_all_off():
    for p in [YELLOW_PIN, WHITE_PIN, BLUE_PIN]:
        led_off(p)

# ----------------------------
# Debounce setup
# ----------------------------
last_state = None
last_change_time = 0
DEBOUNCE_DELAY = 0.25  # seconds

# ----------------------------
# Main loop
# ----------------------------
while True:
    ret, img = cap.read()
    if not ret:
        break

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    current_state = "Idle"

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)
            h, w, _ = img.shape

            x_thumb, y_thumb = int(handLms.landmark[4].x * w), int(handLms.landmark[4].y * h)
            x_index, y_index = int(handLms.landmark[8].x * w), int(handLms.landmark[8].y * h)
            x_pinky, y_pinky = int(handLms.landmark[20].x * w), int(handLms.landmark[20].y * h)

            pinch_dist = np.hypot(x_index - x_thumb, y_index - y_thumb)
            coyote_dist = np.hypot(x_pinky - x_thumb, y_pinky - y_thumb)

            # Determine gesture
            if pinch_dist < 40:
                current_state = "Pinch"
            elif coyote_dist < 50:
                current_state = "QuietCoyote"
            elif pinch_dist > 90:
                current_state = "OpenHand"
            else:
                current_state = "Idle"

    # ----------------------------
    # Debounced LED updates
    # ----------------------------
    if current_state != last_state and (time.time() - last_change_time) > DEBOUNCE_DELAY:
        last_state = current_state
        last_change_time = time.time()
        turn_all_off()

        if current_state == "Pinch":
            led_on(YELLOW_PIN)
            print("Pinch ? Yellow ON")
        elif current_state == "QuietCoyote":
            led_on(BLUE_PIN)
            print("Quiet Coyote ? Blue ON")
        elif current_state == "OpenHand":
            led_on(WHITE_PIN)
            print("Open Hand ? White ON")
        else:
            print("Idle (All OFF)")

    # ----------------------------
    # Show video feed
    # ----------------------------
    cv2.putText(img, f"State: {current_state}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("MediaPipe Qwiic LED Control", img)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

# ----------------------------
# Cleanup
# ----------------------------
turn_all_off()
cap.release()
cv2.destroyAllWindows()
print("Program ended ? all LEDs OFF.")
