# Final Project

[Project Plan](#project-plan) 

[Functioning Project](#functioning-project) 

[Documentation of Design Process](#documentation-of-design-process) 

[Archive of All Code and Design Patterns](#archive-of-all-code-and-design-patterns) 

[Video Demo](#video-demo) 

[Reflections on Process](#reflections-on-process) 

[Group Work Distribution](#group-work-distribution) 

## Project Plan
Hester Li(ql382), Joy Sun(js888), Huiying Zhan (hz764)

### Big Idea
Inner Constellation is an interactive art installation that visualizes a person’s inner energy as a living constellation made of light, color, and motion. It invites people to reflect on their emotions through simple, intuitive interactions.

When a participant begins, they choose one of six symbolic elements — Fire 🔥, Water 💧, Wind ❄️, Earth 🌍, Light 💡, or Shadow 🧍‍♀️🧍‍♂️ — each representing a different emotional tone or personality energy. This choice is made by tapping an NFC card or selecting on screen. The system, powered by a Raspberry Pi, then generates a real-time animation that moves and transforms based on that element’s characteristics — for example, Fire glows and flickers, Water flows smoothly, Wind drifts and spins, Earth pulses steadily, Light radiates softly, and Shadow creates shifting patterns.

A computer screen displays the animation blended with a live camera feed of the user, allowing them to see both their reflection and their personalized constellation at the same time. As they move their hands or adjust their posture, gesture and touch sensors detect these actions and feed them back into the system. The constellation reacts instantly — expanding, contracting, or changing colors — as if breathing together with the user.

Through these visual and sensory responses, Inner Constellation transforms abstract emotions into tangible experiences. It connects technology and self-awareness in a poetic way, turning each participant’s reflection on the screen into a unique portrait of their energy and mood in that moment.   
<img src="prototype.jpg" alt="Inner Constellation concept image" width="500">

### Timeline
| **Milestone** | **Date** | **Notes / Details** |
|:--|:--:|:--|
| **Concept Lock & Story Development** | Nov 10–11 | Finalize core interaction and six energy elements. Write story concept and plan MVP scope. |
| **Visual MVP** | Nov 15 | Design an interactive energy circle that expands or contracts with hand gestures. |
| **Input Integration** | Nov 20 | Add gesture detection for circle control. Test responsiveness and stability. |
| **Projection Interaction** | Nov 22 | Project visualization on a large screen. Enable full-screen gesture control and adjust brightness. |
| **Parameter Tuning & Visual Polish** | Nov 25 | Refine color, motion, and gesture sensitivity. Add an “Energy Fortune” line and save-image feature. |
| **Functional Check-off** | Dec 1 | Demonstrate full flow: gesture → real-time motion → image save. Record performance notes. |
| **User Testing** | Dec 5 | Test with non-team users. Gather feedback on usability, aesthetics, and response. |
| **Final Presentation Prep** | Dec 6 | Prepare short demo video and slides. Present motivation, technical design, and evolution. |
| **Final Write-up & Repository Submission** | Dec 8 | Complete README, diagrams, and documentation. Upload final materials. |

### Parts Needed
**The Device**
- 1× Raspberry Pi 4 Board  
- 1× 32GB MicroSD Card w/ Card Reader  
- 1× Computer Display / Monitor  
- 1× USB Camera (for live reflection feed)  
- 1× NFC Reader + NFC Cards (for element selection)  
- 1× Gesture or Touch Sensor (e.g., APDS-9960 or Capacitive Pad)  
- 1× HDMI Cable  
- 1× USB Powered Speaker *(optional, for ambient sound)*  
- 1× Power Supply for Raspberry Pi (5V 3A recommended)  
- 1× Dupont Wire Set *(for sensor connections)*  

**For Exhibition Setup (optional)**
- 1× Projector *(for large-scale projection display)*  
- 1× Tripod or Mounting Stand  
- 1× External Light Diffuser or Frame *(for aesthetic setup)*

### Fallback Plan

If any hardware or sensor components fail, the system can still demonstrate the core experience through simplified input and display modes.


| Category | Risk / Challenge | Mitigation |
|-----------|------------------|-------------|
| **Hardware** | Sensor or camera failure due to wiring or power issues. | Test components early; add keyboard/mouse fallback. |
| **Gesture Detection** | Inaccurate or unstable hand tracking under different lighting. | Calibrate thresholds; add on-screen feedback. |
| **Performance** | Rendering + live camera feed may overload Raspberry Pi. | Lower resolution / particle count; optimize code. |
| **Integration** | Combining gesture, NFC, and camera may cause conflicts. | Build modular code; integrate step-by-step. |
| **Lighting / Projection** | Bright rooms may wash out visuals. | Adjust brightness; use diffuser or darker backdrop. |
| **User Experience** | Users may not understand how to interact. | Add quick on-screen hints; ensure immediate feedback. |
| **Timeline** | Tight schedule for testing and polishing. | Lock MVP early; layer extra features gradually. |

💡 *These fallback modes ensure the installation remains functional and visually expressive, even if some hardware components are unavailable.*
## Functioning Project
左边外观图，右边内部结构图

## Documentation of Design Process
### Verplank Diagram

![Verplank Diagram](images/Verplank_Diagram.jpg)


### Storyboards

#### Scenario 1
![Scenario 1](images/Scenario_1.jpg)


#### Scenario 2
![Scenario 2](images/Scenario_2.jpg)


#### Scenario 3
![Scenario 3](images/Scenario_3.jpg)

### Wiring Diagram 线怎么连接的

### Inner Constellation Design 外观的画


## Archive of All Code and Design Patterns

All related code lives in: [idd final](./idd%20final/)

#### 🧩 Sensor Layer Overview

**📷 Camera — Motion & Background Feed**

The camera module provides:

- Continuous frame capture

- Motion energy estimation by comparing consecutive grayscale frames

- Soft background blending so the silhouette subtly influences animation

Output is unified: get_frame() returns a processed frame or None.

**🖥️ OLED / TFT Display — Minimal Physical Feedback**

The OLED display module:

- Shows the currently selected element

- Shows the three-element personalized profile

Falls back to dummy mode automatically if hardware is unavailable

**👆 MPR121 Touch Sensor — Element Selection**

The MPR121 maps touch pads to elemental identities:

- Touch → "Fire", "Water", "Wind", "Earth", "Light", "Shadow"

- Input is debounced

- Supports 3-step profile selection (user picks their top three elements)

<img src="images/elements.png" width="320">


#### 🌀 Animation Layer Overview

**✨ Overall Architecture**

The animation engine runs 60 FPS with:

- A time-based update loop

- Motion-driven scaling and breathing

- Camera-derived features (motion, body center, size estimation)

- Profile-based color palettes

- 14 visual patterns + camera blending + spectrum tinting

Everything is modular: each visual effect is a separate pattern method.

**🎨 Core Logic**

**1. Profile & Element System**

If user selected a 3-element profile → full spectrum mode

If only one element is touched → fallback single-color mode

get_spectrum_style() provides:

- base colors

- background color

- pattern choice (e.g., galaxy, vortex, pillar)

- per-profile parameters (orb speed, pillar width, halo scale)

**2. Camera → Motion, Size, and Body Position**

The engine extracts:

- **motion_level** → how intensely the user moves

- **size_level**→ approximate distance to camera

- **body_x / body_y** → centroid of motion (horizontal/vertical)

These feed animation:

- motion → breathing & expansion

- body_x → color temperature shift (cooler ↔ warmer)

- size_level → pillar size & orb radius

Camera overlay is softly composited at 60% alpha.

**3. Energy Model**

Animation is governed by a derived energy value:

- pillar height

- halo radius

- orb speed

- bloom strength

- vortex spiral range

- grid pulse brightness

**🌌 Visual Pattern System**

All visual effects automatically adapt to:

- profile colors (3-element spectrum or single fallback element)

- camera motion energy

- user distance (size estimation from camera)

#### 📡 Web Server Layer

server.py runs two parallel systems:

1. Flask Web Server

- Hosts the webpage (index.html)

- Streams the animation frames as MJPEG (/frame)

- Provides control endpoints (e.g., reset, hide/show labels)

2. Pygame Animation Loop

- Runs in the main thread (required by SDL)

- Receives continuous sensor data

- Renders the animated visual output

- Publishes frames to Flask via shared memory (latest_frame)

Both are synchronized using a thread-safe frame_lock.

#### Connect Parts & Sensors 怎么连接的

#### Tech Demo (Functional Checkoff) 功能测试视频

#### Make the the mood board and construct device （mood board制作过程以及连接设备）



## Video Demo
最终展示视频

## Reflections on Process


## Group Work Distribution
### Joy
Joy focused primarily on the visual language and aesthetic foundation of the project. She designed the color schemes, textures, and particle styles for all six elemental themes, and iterated extensively on the visual patterns using Python, Pygame, Processing, p5.py, and OpenGL-based tools. She also created the full mood board, final visual poster, and produced a set of ten physical “Energy Element Cards.”  

**Deliverables:**
- `animation_engine.py`
- Energy Element Cards (×10)
- Element Visual Style Sheets
- Final Exhibition Poster


### Hester
Hester was responsible for the interaction logic and sensing pipeline. This included selecting and integrating the elemental sensor (or icon-based interaction), implementing dynamic pattern transitions based on gestures, sound volume, and distance inputs, and setting up the projector/monitor display system. She also contributed to the creation of ten physical “Energy Element Cards” and participated in the visual presentation materials.  

**Deliverables:**
- `sensor.py`
- Energy Element Cards (×10)


### Sandy
Sandy managed logistics, documentation, and user-facing presentation. She coordinated equipment (projector, backdrop, and decorative materials), prepared the mood board and final visual layout, conducted user testing (facilitation, observation, and interviews), and collected all required images and materials for the README. She also recorded and edited the final demo video and compiled the full project README.  

**Deliverables:**
- `README.md`
- User testing notes and documentation
- Demo video

