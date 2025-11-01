import cv2
import mediapipe as mp
import pygame
import time
import qwiic_gpio
import math

# -------------------------------------------------------------
# 1. INITIAL SETUP
# -------------------------------------------------------------
# Initialize audio mixer
pygame.mixer.init()

# Initialize Qwiic GPIO board
gpio = qwiic_gpio.QwiicGPIO()

# Define LED pin mapping (adjust according to your wiring)
LED_PINS = {
    "kick": 0,     # orange LED
    "snare": 1,    # white LED
    "hihat": 2,    # yellow LED
    "tom": 3       # blue LED
}

# Load drum sounds
sounds = {
    "kick": pygame.mixer.Sound("drum_sounds/kick.wav"),
    "snare": pygame.mixer.Sound("drum_sounds/snare.wav"),
    "hihat": pygame.mixer.Sound("drum_sounds/hihat.wav"),
    "tom": pygame.mixer.Sound("drum_sounds/tom.wav")
}

# Set all LEDs as outputs and turn them OFF (HIGH = off for current-sinking GPIO)
for pin in LED_PINS.values():
    gpio.pin_mode(pin, gpio.OUTPUT)
    gpio.digital_write(pin, gpio.HIGH)

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1,
                       min_detection_confidence=0.6,
                       min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# Start webcam
cap = cv2.VideoCapture(0)

# -------------------------------------------------------------
# 2. HELPER FUNCTIONS
# -------------------------------------------------------------
def flash_led(pin, duration=0.1):
    """Turn LED ON briefly, then OFF again."""
    gpio.digital_write(pin, gpio.LOW)   # LED ON
    time.sleep(duration)
    gpio.digital_write(pin, gpio.HIGH)  # LED OFF


def euclidean_distance(a, b):
    """Compute Euclidean distance between two 3D landmarks."""
    return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2 + (a.z - b.z)**2)


def detect_gesture(hand):
    """
    Classify simple static hand gestures using relative distances.
    Returns one of: 'fist', 'open', 'shaka', 'pinch', or 'rest'.
    """

    thumb_tip = hand.landmark[4]
    index_tip = hand.landmark[8]
    middle_tip = hand.landmark[12]
    ring_tip = hand.landmark[16]
    pinky_tip = hand.landmark[20]
    wrist = hand.landmark[0]

    # Distances to wrist (to know if fingers are extended)
    d_index = euclidean_distance(index_tip, wrist)
    d_middle = euclidean_distance(middle_tip, wrist)
    d_ring = euclidean_distance(ring_tip, wrist)
    d_pinky = euclidean_distance(pinky_tip, wrist)
    avg_open = (d_index + d_middle + d_ring + d_pinky) / 4

    # Key distances for gestures
    d_thumb_index = euclidean_distance(thumb_tip, index_tip)
    d_thumb_pinky = euclidean_distance(thumb_tip, pinky_tip)

    # Simple thresholds (tuned empirically)
    if avg_open < 0.15:
        return "fist"
    elif d_thumb_index < 0.05:
        return "pinch"
    elif d_thumb_pinky < 0.10 and d_index > 0.15 and d_middle > 0.15:
        return "shaka"
    elif avg_open > 0.25:
        return "open"
    else:
        return "rest"

# -------------------------------------------------------------
# 3. MAIN LOOP
# -------------------------------------------------------------
last_gesture = None
cooldown = 0.3   # seconds between beats

print("Starting Gesture Drum Machine... Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Mirror view
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    gesture = "rest"
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            gesture = detect_gesture(hand_landmarks)
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Trigger sound and LED only when gesture changes
    if gesture != last_gesture:
        if gesture == "fist":
            sounds["kick"].play()
            flash_led(LED_PINS["kick"])
        elif gesture == "open":
            sounds["snare"].play()
            flash_led(LED_PINS["snare"])
        elif gesture == "shaka":
            sounds["hihat"].play()
            flash_led(LED_PINS["hihat"])
        elif gesture == "pinch":
            sounds["tom"].play()
            flash_led(LED_PINS["tom"])
        elif gesture == "rest":
            # Turn all LEDs off
            for pin in LED_PINS.values():
                gpio.digital_write(pin, gpio.HIGH)

        last_gesture = gesture
        time.sleep(cooldown)

    # Display on-screen feedback
    cv2.putText(frame, f"Gesture: {gesture}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.imshow("Gesture Drum Machine", frame)

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
