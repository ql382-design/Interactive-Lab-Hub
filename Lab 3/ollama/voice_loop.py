import os
import subprocess
import requests
from faster_whisper import WhisperModel

# Ollama server details
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL_NAME = "phi3:mini"

def record_audio(filename="input.wav", duration=4):
    """Record audio from the USB webcam microphone."""
    print(f"[INFO] Recording {duration} seconds...")
    subprocess.run([
        "arecord", "-D", "plughw:0,0", "-f", "cd",
        "-t", "wav", "-d", str(duration), "-r", "16000", filename
    ])

def transcribe_audio(filename="input.wav"):
    """Use Whisper to transcribe audio into text."""
    print("[INFO] Transcribing with Whisper...")
    model = WhisperModel("tiny", device="cpu", compute_type="int8")
    segments, _ = model.transcribe(filename)
    text = " ".join([seg.text for seg in segments])
    return text.strip()

def ask_ollama(prompt):
    """Send the transcribed text to Ollama and get the response."""
    print(f"[INFO] Sending to Ollama: {prompt}")
    r = requests.post(
        OLLAMA_URL,
        json={"model": MODEL_NAME, "prompt": prompt, "stream": False},
        timeout=120
    )
    return r.json().get("response", "No response")

def speak(text):
    """Use espeak to generate speech from text and play it."""
    print(f"[INFO] Speaking: {text}")
    subprocess.run(f'espeak "{text}" --stdout | aplay', shell=True)

if __name__ == "__main__":
    print("🎤 Simple Voice Assistant (say something!)")
    print("Type Ctrl+C or say 'exit' to stop.\n")

    while True:
        record_audio()
        user_text = transcribe_audio()
        print("You said:", user_text)

        if not user_text or user_text.lower() in ["exit", "quit", "bye"]:
            print("[INFO] Exiting assistant...")
            break

        reply = ask_ollama(user_text)
        print("AI:", reply)
        speak(reply)
