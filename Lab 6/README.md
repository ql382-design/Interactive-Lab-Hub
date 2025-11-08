# Distributed Interaction

**Hester Li, Joy Sun, Sandy Zhan**

For submission, replace this section with your documentation!

---

<details>
	<summary><strong>(Click to Expand)</strong></summary>

## Prep

1. Pull the new changes
2. Read: [The Presence Table](https://dl.acm.org/doi/10.1145/1935701.1935800) ([video](https://vimeo.com/15932020))

## Overview

Build interactive systems where **multiple devices communicate over a network** using MQTT messaging. Work in teams of 3+ with Raspberry Pis.

**Parts:**
- A: Learn MQTT messaging
- B: Try collaborative pixel grid demo  
- C: Build your own distributed system

</details>


---

## Part A: MQTT Messaging

<details>
	<summary><strong>(Click to Expand)</strong></summary>
 
MQTT = lightweight messaging for IoT. Publish/subscribe model with central broker.

**Concepts:**
- **Broker**: `farlab.infosci.cornell.edu:1883`
- **Topic**: Like `IDD/bedroom/temperature` (use `#` wildcard)
- **Publish/Subscribe**: Send and receive messages

**Install MQTT tools on your Pi:**
```bash
sudo apt-get update
sudo apt-get install -y mosquitto-clients
```

**Test it:**

**Subscribe to messages (listener):**
```bash
mosquitto_sub -h farlab.infosci.cornell.edu -p 1883 -t 'IDD/#' -u idd -P 'device@theFarm'
```

**Publish a message (sender):**
```bash
mosquitto_pub -h farlab.infosci.cornell.edu -p 1883 -t 'IDD/test/yourname' -m 'Hello!' -u idd -P 'device@theFarm'
```

> **💡 Tips:**
> - Replace `yourname` with your actual name in the topic
> - Use single quotes around the password: `'device@theFarm'`

**🔧 Debug Tool:** View all MQTT messages in real-time at `http://farlab.infosci.cornell.edu:5001`

![MQTT Explorer showing messages](imgs/MQTT-explorer.png)

</details>


## 💡 Brainstorm — 5 Ideas for Messaging Between Devices

### 1. Mood Lights Across Rooms
**Concept:** Each Raspberry Pi controls an RGB LED strip that reflects the user’s mood.  
**Mechanism:**  
- A Pi with a color sensor or slider publishes to `IDD/mood/hester → {r,g,b}`.  
- Other Pis subscribe to `IDD/mood/#` and blend incoming colors (average RGB).  
**Effect:** Everyone’s lights softly synchronize — if one sets blue (calm), all rooms drift cooler.  
**Learning focus:** Continuous data messaging, aggregation logic, visual feedback.

---

### 2. Presence Ping-Pong
**Concept:** A playful “I’m here” or “poke” system between teammates.  
**Mechanism:**  
- Pressing a Pi button publishes `IDD/ping/name`.  
- The recipient Pi flashes an LED or plays a tone, then auto-replies `pong`.  
**Effect:** Low-latency emotional connection loop.  
**Learning focus:** Topic-based targeting, timing, and event acknowledgment.

---

### 3. Collaborative Counter / Shared Scoreboard
**Concept:** Each device has a button that increases or decreases a shared counter.  
**Mechanism:**  
- Publish increments to `IDD/counter/increment` or `IDD/counter/decrement`.  
- All subscribers maintain and display the global total.  
**Effect:** Live distributed tally for votes, focus tracking, or group progress.  
**Learning focus:** State synchronization and conflict resolution across devices.

---

### 4. Sound Ripple Network
**Concept:** One device plays a tone; others echo or harmonize in sequence.  
**Mechanism:**  
- A Pi detects sound amplitude or button press → publishes `IDD/sound/note:C4`.  
- Other Pis subscribe and trigger tones with slight delay (+200 ms each).  
**Effect:** A cascading “musical wave.”  
**Learning focus:** Timestamp-based scheduling, ordering of messages, coordinated timing.

---

### 5. Distributed Weather Display
**Concept:** Each device shares local sensor readings (temperature, humidity, or light).  
**Mechanism:**  
- Each Pi publishes `IDD/weather/piName → {temp, humidity}`.  
- A dashboard Pi aggregates and visualizes all nodes’ data.  
**Effect:** A small IoT network sensing micro-environments across a space.  
**Learning focus:** Data collection, JSON message structure, and visualization.

---


## Part B: Collaborative Pixel Grid

<details>
	<summary><strong>(Click to Expand)</strong></summary>
 
Each Pi = one pixel, controlled by RGB sensor, displayed in real-time grid.

**Architecture:** `Pi (sensor) → MQTT → Server → Web Browser`

**Setup:**

1. **Sensor**

#### Light/Proximity/Gesture sensor (APDS-9960)
We use this sensor [Adafruit APDS-9960](https://www.adafruit.com/product/3595) for this exmaple to detect light (also RGB)
 
<img src="https://cdn-shop.adafruit.com/970x728/3595-06.jpg" width=200>

Connect it to your pi with Qwiic connector


<img src="imgs/IMG_0270.jpg" height="200" />
We need to use the screen to display the color detection, so we need to stop the running piscreen.service to make your screen available again

```bash
# stop the screen service
sudo systemctl stop piscreen.service
```

if you want to restart the screen service
```bash
# start the screen service
sudo systemctl start piscreen.service
```
 
2. **Server** (one person on laptop):
```bash
cd "Lab 6"  
source .venv/bin/activate
pip install -r requirements-server.txt
python app.py
```

2. **View in browser:**
   - Grid: `http://farlab.infosci.cornell.edu:5000`
   - Controller: `http://farlab.infosci.cornell.edu:5000/controller`

3. **Pi publisher** (everyone on their Pi):
```bash
# First time setup - create virtual environment
cd "Lab 6"
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-pi.txt

# Run the publisher
python pixel_grid_publisher.py
```

Hold colored objects near sensor to change your pixel!

![Pixel grid with two devices](imgs/two-devices-grid.png)

</details>

**📸 Include: Screenshot of grid + photo of your Pi setup**

[![Video 1](https://img.youtube.com/vi/6vmiTTxWM5w/0.jpg)](https://youtu.be/6vmiTTxWM5w)
*Demo 1 – grid color changes.*


---

## Part C: Make Your Own


[![Video 4](https://img.youtube.com/vi/HpCUQ5m_lUI/0.jpg)](https://youtu.be/HpCUQ5m_lUI)
*Demo 2 – Successful mechanism activation & treasure reveal.*
[![Video 3](https://img.youtube.com/vi/X49TW9GbIAs/0.jpg)](https://youtu.be/X49TW9GbIAs?si=_uI-3xRdj2L-BlTg)
*Demo 3 – Test with ourself.*




[![Video 4](https://img.youtube.com/vi/I4TWD0MCLDg/0.jpg)](https://youtu.be/I4TWD0MCLDg?si=YFtWZD_QqbNtnUdA)
*Demo 4 – test with 3 users.*


<details>
	<summary><strong>(Click to Expand)</strong></summary>
 
**Requirements:**
- 3+ people, 3+ Pis
- Each Pi contributes sensor input via MQTT
- Meaningful or fun interaction

**Ideas:**

**Sensor Fortune Teller**
- Each Pi sends 0-255 from different sensor
- Server generates fortunes from combined values

**Frankenstories**
- Sensor events → story elements (not text!)
- Red = danger, gesture up = climbed, distance <10cm = suddenly

**Distributed Instrument**
- Each Pi = one musical parameter
- Only works together

**Others:** Games, presence display, mood ring

### Deliverables

Replace this README with your documentation:

**1. Project Description**
- What does it do? Why interesting? User experience?

**2. Architecture Diagram**
- Hardware, connections, data flow
- Label input/computation/output

**3. Build Documentation**
- Photos of each Pi + sensors
- MQTT topics used
- Code snippets with explanations

**4. User Testing**
- **Test with 2+ people NOT on your team**
- Photos/video of use
- What did they think before trying?
- What surprised them?
- What would they change?

**5. Reflection**
- What worked well?
- Challenges with distributed interaction?
- How did sensor events work?
- What would you improve?

---

## Code Files

**Server files:**
- `app.py` - Pixel grid server (Flask + WebSocket + MQTT)
- `mqtt_viewer.py` - MQTT message viewer for debugging
- `mqtt_bridge.py` - MQTT → WebSocket bridge
- `requirements-server.txt` - Server dependencies

**Pi files:**
- `pixel_grid_publisher.py` - Example (RGB sensor → MQTT)
- `requirements-pi.txt` - Pi dependencies

**Web interface:**
- `templates/grid.html` - Pixel grid display
- `templates/controller.html` - Color picker
- `templates/mqtt_viewer.html` - Message viewer

---

## Debugging Tools

**MQTT Message Viewer:** `http://farlab.infosci.cornell.edu:5001`
- See all MQTT messages in real-time
- View topics and payloads
- Helpful for debugging your own projects

**Command line:**
```bash
# See all IDD messages
mosquitto_sub -h farlab.infosci.cornell.edu -p 1883 -t "IDD/#" -u idd -P "device@theFarm"
```

---

## Troubleshooting

**MQTT:** Broker `farlab.infosci.cornell.edu:1883`, user `idd`, pass `device@theFarm`

**Sensor:** Check `i2cdetect -y 1`, APDS-9960 at `0x39`

**Grid:** Verify server running, check MQTT in console, test with web controller

**Pi venv:** Make sure to activate: `source .venv/bin/activate`


---

## Submission Checklist

Before submitting:
- [ ] Delete prep/instructions above
- [ ] Add YOUR project documentation
- [ ] Include photos/videos/diagrams  
- [ ] Document user testing with non-team members
- [ ] Add reflection on learnings
- [ ] List team names at top

**Your README = story of what YOU built!**

---

Resources: [MQTT Guide](https://www.hivemq.com/mqtt-essentials/) | [Paho Python](https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php) | [Flask-SocketIO](https://flask-socketio.readthedocs.io/)

</details>

