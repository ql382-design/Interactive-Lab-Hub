from faster_whisper import WhisperModel
import time
import sys

# Pick audio file from command line, else default to lookdave.wav
audio_file = sys.argv[1] if len(sys.argv) > 1 else "lookdave.wav"

start_time = time.perf_counter()

model_size = "tiny"

# Run on CPU with INT8 (works on Raspberry Pi 5)
model = WhisperModel(model_size, device="cpu", compute_type="int8")

print(f"Transcribing: {audio_file}")
segments, info = model.transcribe(audio_file, beam_size=5)

for segment in segments:
    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))

end_time = time.perf_counter()
elapsed_time = end_time - start_time
print(f"Program executed in {elapsed_time:.6f} seconds")
