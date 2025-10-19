# Play audio clips via paplay (PipeWire/Pulse) or aplay (ALSA)
# Adds warmup() to wake Bluetooth sink so first playback isn't truncated.

import subprocess
from pathlib import Path
import wave
import os

AUDIO_DIR = Path(__file__).resolve().parent.parent / "assets" / "audio"
_WARMED = False
_WARMUP_WAV = Path("/tmp/fate_audio_warmup.wav")

def _ensure_warmup_wav():
    """Create a short silent WAV to wake the audio sink."""
    if _WARMUP_WAV.exists():
        return
    # 0.15s silence @ 48kHz
    fr = 48000
    dur = 0.15
    n = int(fr * dur)
    with wave.open(str(_WARMUP_WAV), "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(fr)
        wf.writeframes(b"\x00\x00" * n)

def warmup():
    """Play a tiny silent clip to wake the BT sink from SUSPENDED state."""
    global _WARMED
    if _WARMED:
        return
    try:
        _ensure_warmup_wav()
        for cmd in (["paplay", str(_WARMUP_WAV)], ["aplay", str(_WARMUP_WAV)]):
            try:
                subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                _WARMED = True
                return
            except FileNotFoundError:
                continue
            except subprocess.CalledProcessError:
                continue
    except Exception:
        # Even if warmup fails, don't block normal playback
        pass
    _WARMED = True  # Avoid repeated attempts

def play_clip(name: str):
    """
    Plays an audio file named <name>.ogg or <name>.wav in assets/audio.
    Prefer paplay; fallback to aplay. Calls warmup() on first use.
    """
    warmup()

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

def play_sequence(names, gap_sec=0.0):
    """Play a list/tuple of clip names with a fixed gap (in seconds)."""
    import time
    for i, n in enumerate(names):
        play_clip(n)
        if i < len(names) - 1 and gap_sec > 0:
            time.sleep(gap_sec)
