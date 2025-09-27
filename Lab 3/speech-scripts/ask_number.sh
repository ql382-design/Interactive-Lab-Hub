#!/bin/bash
# ask_number.sh - Ask for a number and transcribe using Vosk

# Step 1: Generate prompt to file
espeak "Please say your zipcode now." -w prompt.wav

# Step 2: Play prompt fully (fixes Bluetooth cut-off issue)
aplay prompt.wav

# Step 3: Record 5 seconds from webcam mic (card 0, device 0 for C270)
arecord -D plughw:0,0 -r 16000 -f S16_LE -c 1 -d 5 answer.wav

# Step 4: Transcribe with Vosk
vosk-transcriber -i answer.wav -o result.txt

# Step 5: Show result
echo "You said:"
cat result.txt

