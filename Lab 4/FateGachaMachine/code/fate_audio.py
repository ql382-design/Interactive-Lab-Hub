# Play pre-rendered audio clips via paplay (PipeWire/Pulse) or aplay (ALSA)
import subprocess
from pathlib import Path

AUDIO_DIR = Path(__file__).resolve().parent.parent / "assets" / "audio"

def play_clip(name: str):
    # Plays an audio file named <name>.ogg or <name>.wav in assets/audio.
    candidates = [AUDIO_DIR / f"{name}.ogg", AUDIO_DIR / f"{name}.wav"]
    clip = next((c for c in candidates if c.exists()), None)
    if not clip:
        print(f"[audio] Missing clip: {name}")
        return
    for cmd in (["paplay", str(clip)], ["aplay", str(clip)]):
        try:
            subprocess.run(cmd, check=True)
            return
        except FileNotFoundError:
            continue
        except subprocess.CalledProcessError:
            continue
    print("[audio] No player available (paplay/aplay).")
