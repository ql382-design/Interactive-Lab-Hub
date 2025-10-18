# Fate Gacha Machine — Multi-Input / Multi-Output (Encoder + Qwiic Button + Speaker + OLED)

This repo contains runnable code and assets for the **Fate Gacha Machine** using a **Qwiic I²C chain** (OLED, Qwiic Button, I²C Rotary Encoder) and a **Bluetooth speaker** for audio output.

## Quick Start
```bash
sudo apt update
sudo apt install -y python3-pip python3-pil python3-numpy i2c-tools
pip3 install adafruit-circuitpython-ssd1306 adafruit-circuitpython-seesaw qwiic_button smbus2 pillow

sudo raspi-config  # Interface Options -> I2C -> Enable

sudo i2cdetect -y 1  # expect: 0x36 (encoder), 0x3c (oled), 0x6f (button)

# pair/connect BT speaker then test:
paplay /usr/share/sounds/alsa/Front_Center.wav

# run tests:
python3 code/scan_i2c_devices.py
python3 code/test_oled.py
python3 code/test_button.py
python3 code/test_encoder.py

# run main:
python3 code/main.py
```
---

## 🎮 Interaction Reflections (Part E — Multi-Device Insights)

### 1. What new types of interaction become possible when you combine two or more sensors or actuators?

In this prototype, I combine a **rotary encoder** with a **Qwiic button**, and use **speaker audio output + OLED fate display** as feedback channels.  
This transforms the interaction from a simple binary control into a **layered ritual sequence**:

- **Encoder rotation** generates **gradual tension**, simulating hesitation and emotional buildup.
- **Button press** acts as a **commitment gesture**, similar to “pulling the lever” on a gacha machine.
- **Speaker output** conveys emotional tone using **pitch, rhythm, and frequency shifts**:
  - Soft chime → Indecision
  - Rising tone → Growing urge
  - Harsh buzz → Fate rejection
  - Chaotic frequency sweep → **CHAOS / uncontrollable destiny**
- **OLED display** presents the final **fate reveal message (YES / NO / DELAY / CHAOS)** like a prophecy screen.

Together, these elements turn a simple electronic interaction into a **mini dramatic performance of fate negotiation**, rather than just “pressing a button to see a result.”

---

### 2. How does the physical arrangement of devices change the user experience?

The **encoder is placed low and centered**, mimicking the physical handle of a capsule toy or arcade gacha machine — users naturally perform a **theatrical twisting gesture**.

The **button is positioned separately**, slightly elevated or isolated, to clearly communicate that **this is the decisive input**, distinct from the exploratory nature of rotation.

Placing the **speaker inside the enclosure** makes the sound feel like it is coming from within the machine — as if the system is "thinking" or "speaking" its fate.  
Meanwhile, the **OLED is positioned at eye level**, functioning visually as a **fortune display window**.

Layout alone communicates the interaction sequence without text:

> **Twist → Pause → Press → Machine speaks → Fate appears**

---

### 3. What happens when one device modulates another?

Instead of treating components separately, I allow the **encoder to dynamically influence the speaker output before fate is confirmed**:

| Encoder Behavior            | Speaker Feedback (before confirmation)                   |
|---------------------------|----------------------------------------------------------|
| Slow rotation / hesitation | Low ticking or subtle hum                               |
| Fast rotation / impulse    | Rising pitch tone                                       |
| Over-rotation / chaos      | Irregular sweep tone (unstable, distorted)              |

Once the button is pressed, the **stored tension is released** as a short **audio signature**, followed by a final **OLED display message**.

This makes the encoder feel less like an input device and more like a **"fate tension dial"**, charging emotional energy before release.

---

### 4. How does the system feel when you swap primary and secondary roles?

| Configuration                            | Emotional Feel                                        |
|-----------------------------------------|------------------------------------------------------|
| **Encoder as primary, button secondary** | Cinematic and ritualistic — user "negotiates fate"   |
| **Button as primary, encoder secondary** | Game-like and immediate — quick trigger interaction  |

When the **encoder leads**, users feel like they are **actively shaping their destiny**.  
When the **button leads**, the experience becomes **binary and abrupt**, similar to a normal consumer device.

This demonstrates that **input hierarchy is not just a technical decision — it defines the entire emotional pacing of interaction.**
