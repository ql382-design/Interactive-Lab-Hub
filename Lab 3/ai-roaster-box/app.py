import os
import queue
import json
import random
import time
import threading
import subprocess
from gesture_sensor import GestureSensor

import sounddevice as sd
from vosk import Model, KaldiRecognizer
from flask import Flask, render_template
from flask_socketio import SocketIO
import board
import busio
import adafruit_apds9960.apds9960

# -------------------------------------------------
# Configuration
# -------------------------------------------------
MODEL_PATH_CANDIDATES = [
    "/home/pi/vosk_model/model",
    "/home/pi/vosk_models/vosk-model-small-en-us-0.15",
]

SAMPLE_RATE = 16000
BLOCKSIZE = 8000
LISTEN_SECONDS = 5
INPUT_DEVICE = None  # Set your mic name or number if needed

# -------------------------------------------------
# Flask + SocketIO setup
# -------------------------------------------------
app = Flask(__name__)
socketio = SocketIO(app, async_mode="threading", cors_allowed_origins="*")

@app.route("/")
def index():
    return render_template("index.html")

def update_web(user_text: str, ai_text: str):
    """Send latest user and AI text to web client."""
    socketio.emit("update_text", {"user": user_text, "ai": ai_text})

def update_status(status_text: str):
    """Send general status messages (wave detection, etc.)"""
    socketio.emit("status_update", {"status": status_text})

# -------------------------------------------------
# Load Vosk model
# -------------------------------------------------
def find_model_path() -> str:
    for p in MODEL_PATH_CANDIDATES:
        if os.path.exists(p):
            return p
    raise FileNotFoundError(
        "Vosk model not found. Please download one into:\n"
        + "\n".join(MODEL_PATH_CANDIDATES)
    )

MODEL_PATH = find_model_path()
model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, SAMPLE_RATE)

audio_q: "queue.Queue[bytes]" = queue.Queue()

def audio_callback(indata, frames, time_info, status):
    audio_q.put(bytes(indata))

# -------------------------------------------------
# Speech-to-Text
# -------------------------------------------------
def record_and_transcribe(duration=LISTEN_SECONDS) -> str:
    """Record from microphone and transcribe speech using Vosk."""
    try:
        while True:
            audio_q.get_nowait()
    except queue.Empty:
        pass

    print("Listening...")
    text_result = ""

    stream_kwargs = dict(
        samplerate=SAMPLE_RATE,
        blocksize=BLOCKSIZE,
        dtype="int16",
        channels=1,
        callback=audio_callback,
    )
    if INPUT_DEVICE is not None:
        stream_kwargs["device"] = INPUT_DEVICE

    with sd.RawInputStream(**stream_kwargs):
        recognizer.Reset()
        end_time = time.time() + duration
        while time.time() < end_time:
            try:
                data = audio_q.get(timeout=0.5)
            except queue.Empty:
                continue
            if recognizer.AcceptWaveform(data):
                part = json.loads(recognizer.Result())
                if part.get("text"):
                    text_result = part["text"]

        final = json.loads(recognizer.FinalResult())
        if final.get("text"):
            text_result = final["text"] or text_result

    if text_result:
        print(f"You said: {text_result}")
    else:
        print("No speech detected.")
    return text_result

# -------------------------------------------------
# Text-to-Speech (espeak)
# -------------------------------------------------
def speak(text: str):
    """Speak text aloud using espeak + aplay (offline)."""
    print(f"AI says: {text}")
    p1 = subprocess.Popen(["espeak", text, "--stdout"], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["aplay"], stdin=p1.stdout, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    p1.stdout.close()
    p2.communicate()

# -------------------------------------------------
# Roast generation logic
# -------------------------------------------------
def generate_roast(user_text: str) -> str:
    roasts = [
        "Oh, that was deep. Like a puddle.",
        "You call that an argument? Try harder.",
        "Interesting. But still wrong.",
        "You again? I thought we broke up.",
        "Keep talking, I need background noise.",
        "That was almost clever.",
        "I'm sorry, I can't hear you over how wrong you are.",
        "Bold move. Unfortunately, incorrect.",
        "I would agree, but then we would both be wrong.",
    ]
    return random.choice(roasts)

# -------------------------------------------------
# Display text to console + web
# -------------------------------------------------
def display_text(user_text: str, ai_text: str):
    try:
        print(f"User: {user_text}")
        print(f"AI: {ai_text}")
    except UnicodeEncodeError:
        print("Encoding error while printing text.")
    update_web(user_text, ai_text)
def roast_loop():
    while True:
        user_text = record_and_transcribe(duration=LISTEN_SECONDS)
        if not user_text:
            display_text("No speech detected.", "Try again!")
            continue

        # End of argument trigger
        if any(word in user_text.lower() for word in ["stop", "enough", "i'm done", "shut up", "peace"]):
            ai_text = "Fine, truce… for now."
            display_text(user_text, ai_text)
            speak(ai_text)
            break  # Exit the loop (end argument)

        ai_text = generate_roast(user_text)
        display_text(user_text, ai_text)
        speak(ai_text)

# -------------------------------------------------
# Conversation session (triggered by wave)
# -------------------------------------------------
def roast_session():
    """Handle a full roast session until user says stop words."""
    update_status("Listening for your comeback...")
    while True:
        user_text = record_and_transcribe(duration=LISTEN_SECONDS)
        if not user_text:
            display_text("No speech detected.", "Try again!")
            continue

        # --- Stop / end keywords ---
        if any(word in user_text.lower() for word in ["stop", "enough", "i'm done", "shut up", "peace"]):
            ai_text = "Fine, truce... for now."
            display_text(user_text, ai_text)
            speak(ai_text)
            break

        # Normal roast response
        ai_text = generate_roast(user_text)
        display_text(user_text, ai_text)
        speak(ai_text)
    update_status("Session ended. Wave again to start a new one!")

# -------------------------------------------------
# Gesture detection (wave trigger)
# -------------------------------------------------
def gesture_listener():
    """Continuously listen for gesture input from APDS9960."""
    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_apds9960.apds9960.APDS9960(i2c)
    sensor.enable_gesture = True

    print("Gesture sensor initialized. Waiting for waves...")
    update_status("Waiting for your wave...")

    while True:
        gesture = sensor.gesture()
        if gesture != 0:
            print("Wave detected! Starting roast session...")
            update_status("Wave detected! Starting roast session...")
            roast_session()
            time.sleep(1)
        time.sleep(0.2)

# -------------------------------------------------
# Entry point
# -------------------------------------------------
if __name__ == "__main__":
    print("AI Roast Buddy Ready!")
    print("Open: http://<YourPiIP>:5000 in browser")

    # Initialize gesture sensor
    gesture_sensor = GestureSensor()

    # Run web server (in a separate thread so it doesn't block)
    threading.Thread(
        target=lambda: socketio.run(app, host="0.0.0.0", port=5000),
        daemon=True
    ).start()

    # Main loop: wait for a hand wave, then start roast interaction
    while True:
        print("\nWave your hand to start talking...")
        gesture_sensor.detect_wave()   # Wait until gesture detected
        roast_loop()                   # Start the conversation loop
