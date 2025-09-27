#!/bin/bash
# ask_number_whisper.sh - Whisper version with reliable TTS playback

# Step 1: Generate TTS audio to a file
espeak "Please say your zipcode now." -w prompt.wav

# Step 2: Play the audio file (ensures full playback on Bluetooth speaker)
aplay prompt.wav

# Step 3: Record 5 seconds from webcam mic
arecord -D plughw:0,0 -r 16000 -f S16_LE -c 1 -d 5 answer.wav

# Step 4: Transcribe with Whisper
python faster_whisper_try.py answer.wav
