# Observant Systems

**NAMES OF COLLABORATORS HERE**


For lab this week, we focus on creating interactive systems that can detect and respond to events or stimuli in the environment of the Pi, like the Boat Detector we mentioned in lecture. 
Your **observant device** could, for example, count items, find objects, recognize an event or continuously monitor a room.

This lab will help you think through the design of observant systems, particularly corner cases that the algorithms need to be aware of.

## Prep

1.  Install VNC on your laptop if you have not yet done so. This lab will actually require you to run script on your Pi through VNC so that you can see the video stream. Please refer to the [prep for Lab 2](https://github.com/FAR-Lab/Interactive-Lab-Hub/blob/-/Lab%202/prep.md#using-vnc-to-see-your-pi-desktop).
2.  Install the dependencies as described in the [prep document](prep.md). 
3.  Read about [OpenCV](https://opencv.org/about/),[Pytorch](https://pytorch.org/), [MediaPipe](https://mediapipe.dev/), and [TeachableMachines](https://teachablemachine.withgoogle.com/).
4.  Read Belloti, et al.'s [Making Sense of Sensing Systems: Five Questions for Designers and Researchers](https://www.cc.gatech.edu/~keith/pubs/chi2002-sensing.pdf).

### For the lab, you will need:
1. Pull the new Github Repo
1. Raspberry Pi
1. Webcam 

### Deliverables for this lab are:
1. Show pictures, videos of the "sense-making" algorithms you tried.
1. Show a video of how you embed one of these algorithms into your observant system.
1. Test, characterize your interactive device. Show faults in the detection and how the system handled it.

## Overview
Building upon the paper-airplane metaphor (we're understanding the material of machine learning for design), here are the four sections of the lab activity:

A) [Play](#part-a)

B) [Fold](#part-b)

C) [Flight test](#part-c)

D) [Reflect](#part-d)

---

### Part A
### Play with different sense-making algorithms.

#### Pytorch for object recognition

For this first demo, you will be using PyTorch and running a MobileNet v2 classification model in real time (30 fps+) on the CPU. We will be following steps adapted from [this tutorial](https://pytorch.org/tutorials/intermediate/realtime_rpi.html).

![torch](Readme_files/pyt.gif)


To get started, install dependencies into a virtual environment for this exercise as described in [prep.md](prep.md).

Make sure your webcam is connected.

You can check the installation by running:

```
python -c "import torch; print(torch.__version__)"
```

If everything is ok, you should be able to start doing object recognition. For this default example, we use [MobileNet_v2](https://arxiv.org/abs/1801.04381). This model is able to perform object recognition for 1000 object classes (check [classes.json](classes.json) to see which ones.

Start detection by running  

```
python infer.py
```

The first 2 inferences will be slower. Now, you can try placing several objects in front of the camera.

Read the `infer.py` script and become familiar with the code. You can change the video resolution and frames per second (FPS). You may also use the weights of the larger pre-trained mobilenet_v3_large model, as described [here](https://pytorch.org/tutorials/intermediate/realtime_rpi.html#model-choices).

#### More classes

[PyTorch supports transfer learning](https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html), so you can fine‑tune and transfer learn models to recognize your own objects. It requires extra steps, so we won't cover it here.

For more details on transfer learning and deployment to embedded devices, see Deep Learning on Embedded Systems: A Hands‑On Approach Using Jetson Nano and Raspberry Pi (Tariq M. Arif). [Chapter 10](https://onlinelibrary.wiley.com/doi/10.1002/9781394269297.ch10) covers transfer learning for object detection on desktop, and [Chapter 15](https://onlinelibrary.wiley.com/doi/10.1002/9781394269297.ch15) describes moving models to the Pi using ONNX.

### Machine Vision With Other Tools
The following sections describe tools ([MediaPipe](#mediapipe) and [Teachable Machines](#teachable-machines)).

#### MediaPipe

A established open source and efficient method of extracting information from video streams comes out of Google's [MediaPipe](https://mediapipe.dev/), which offers state of the art face, face mesh, hand pose, and body pose detection.

![Media pipe](Readme_files/mp.gif)

To get started, install dependencies into a virtual environment for this exercise as described in [prep.md](prep.md):

Each of the installs will take a while, please be patient. After successfully installing mediapipe, connect your webcam to your Pi and use **VNC to access to your Pi**, open the terminal, and go to Lab 5 folder and run the hand pose detection script we provide:
(***it will not work if you use ssh from your laptop***)


```
(venv-ml) pi@ixe00:~ $ cd Interactive-Lab-Hub/Lab\ 5
(venv-ml) pi@ixe00:~ Interactive-Lab-Hub/Lab 5 $ python hand_pose.py
```

Try the two main features of this script: 1) pinching for percentage control, and 2) "[Quiet Coyote](https://www.youtube.com/watch?v=qsKlNVpY7zg)" for instant percentage setting. Notice how this example uses hardcoded positions and relates those positions with a desired set of events, in `hand_pose.py`. 

Consider how you might use this position based approach to create an interaction, and write how you might use it on either face, hand or body pose tracking.

(You might also consider how this notion of percentage control with hand tracking might be used in some of the physical UI you may have experimented with in the last lab, for instance in controlling a servo or rotary encoder.)



#### Moondream Vision-Language Model

[Moondream](https://www.ollama.com/library/moondream) is a lightweight vision-language model that can understand and answer questions about images. Unlike the classification models above, Moondream can describe images in natural language and answer specific questions about what it sees.

To use Moondream, first make sure Ollama is running and pull the model:
```bash
ollama pull moondream
```

Then run the simple demo script:
```bash
python moondream_simple.py
```

This will capture an image from your webcam and let you ask questions about it in natural language. Note that vision-language models are slower than classification models (responses may take up to minutes on a Raspberry Pi). There are newer models like [LFM2-VL](https://huggingface.co/LiquidAI/LFM2-VL-450M-GGUF), but many are very recent and not yet optimized for embedded devices.

**Design consideration**: Think about how slower response times change your interaction design. What kinds of observant systems benefit from thoughtful, delayed responses rather than real-time classification? Consider systems that monitor over longer time periods or provide periodic summaries rather than instant feedback.

#### Teachable Machines
Google's [TeachableMachines](https://teachablemachine.withgoogle.com/train) is very useful for prototyping with the capabilities of machine learning. We are using [a python package](https://github.com/MeqdadDev/teachable-machine-lite) with tensorflow lite to simplify the deployment process.

![Tachable Machines Pi](Readme_files/tml_pi.gif)

To get started, install dependencies into a virtual environment for this exercise as described in [prep.md](prep.md):

After installation, connect your webcam to your Pi and use **VNC to access to your Pi**, open the terminal, and go to Lab 5 folder and run the example script:
(***it will not work if you use ssh from your laptop***)


```
(venv-tml) pi@ixe00:~ Interactive-Lab-Hub/Lab 5 $ python tml_example.py
```


Next train your own model. Visit [TeachableMachines](https://teachablemachine.withgoogle.com/train), select Image Project and Standard model. The raspberry pi 4 is capable to run not just the low resource models. Second, use the webcam on your computer to train a model. *Note: It might be advisable to use the pi webcam in a similar setting you want to deploy it to improve performance.*  For each class try to have over 150 samples, and consider adding a background or default class where you have nothing in view so the model is trained to know that this is the background. Then create classes based on what you want the model to classify. Lastly, preview and iterate. Finally export your model as a 'Tensorflow lite' model. You will find an '.tflite' file and a 'labels.txt' file. Upload these to your pi (through one of the many ways such as [scp](https://www.raspberrypi.com/documentation/computers/remote-access.html#using-secure-copy), sftp, [vnc](https://help.realvnc.com/hc/en-us/articles/360002249917-VNC-Connect-and-Raspberry-Pi#transferring-files-to-and-from-your-raspberry-pi-0-6), or a connected visual studio code remote explorer).
![Teachable Machines Browser](Readme_files/tml_browser.gif)
![Tensorflow Lite Download](Readme_files/tml_download-model.png)

Include screenshots of your use of Teachable Machines, and write how you might use this to create your own classifier. Include what different affordances this method brings, compared to the OpenCV or MediaPipe options.

#### (Optional) Legacy audio and computer vision observation approaches
In an earlier version of this class students experimented with observing through audio cues. Find the material here:
[Audio_optional/audio.md](Audio_optional/audio.md). 
Teachable machines provides an audio classifier too. If you want to use audio classification this is our suggested method. 

In an earlier version of this class students experimented with foundational computer vision techniques such as face and flow detection. Techniques like these can be sufficient, more performant, and allow non discrete classification. Find the material here:
[CV_optional/cv.md](CV_optional/cv.md).

###  Part B — Construct a Simple Interaction

In this lab, I built a gesture-based lighting interaction using **MediaPipe Hands** for visual sensing and the **SparkFun Qwiic GPIO** board for physical output control on the Raspberry Pi.  
The goal was to connect a machine-learning perception model with a tangible, real-time feedback system.

At this initial stage, the LED logic was **inverted** — each LED was **ON by default** when the program started, and it **turned OFF or flickered** when gestures were detected.  
This behavior came from the Qwiic GPIO module’s **current-sinking** design:  
a `LOW` signal sinks current and lights the LED, while a `HIGH` signal releases it.  
Although the result looked reversed, this prototype helped reveal how sensing logic maps to hardware feedback.

Three gesture inputs were mapped to different LEDs:

- **Pinch Gesture** (thumb + index close) → Yellow LED (Pin 0)  
- **Open Hand** → White LED (Pin 2)  
- **Quiet Coyote Gesture** (thumb + pinky close) → Blue LED (Pin 5)

During experimentation, the LEDs responded correctly to each gesture but often stayed on or flashed quickly when the hand hovered near the detection thresholds.  
These flickers highlighted how small variations in distance or lighting could trigger rapid state changes — a useful observation that guided later improvements, such as adding a debounce delay and reversing the logic for more natural “off-by-default” behavior.

**Full interaction code:**  
👉 [mediapipe_qwiic_led.py](./mediapipe_qwiic_led.py)



**\*\*\*Describe and detail the interaction, as well as your experimentation here.\*\*\***

### Part C
### Test the interaction prototype

After building the first working version, I conducted several tests to evaluate how the gesture-controlled lighting system behaves in different real-world conditions.

### ✅ When it works well
The system performs very reliably when the lighting is slightly **dim or soft** rather than bright.  
Under these conditions, the **hand contours are clearer** and MediaPipe detects gestures with **high accuracy and very low latency**.  
The LEDs respond almost instantly when I perform the pinch, open-hand, or Quiet Coyote gestures.

### ⚠️ When it fails
The detection becomes less stable in **bright or uneven lighting** conditions — especially when sunlight or reflections hit the camera directly.  
In those cases, the contrast between the hand and the background decreases, and the system may misclassify gestures or fail to track fingers for a few frames.  
Another common problem appeared between the **Pinch** and **Quiet Coyote** gestures — because both involve two fingertips closing together, the model sometimes confused one for the other, causing the wrong LED to toggle.

### 💡 Why it fails
 failures are mostly caused by:
- Overexposed or shifting brightness in the video input.  
- Similar hand shapes between Pinch and Quiet Coyote gestures.  
- Slight jitter in landmark recognition due to movement or partial occlusion.  
- The LEDs’ state being updated every frame, causing rapid toggling when classification is uncertain.

### 🔍 Feedbacks and Suggestions from friends 
- Add a **debounce delay** (implemented in later versions) to smooth out rapid state changes.
- change the logic to use the gesture to turn on the light instead of gesture turn off the light.
- Include **lighting compensation or automatic brightness normalization** for better stability in variable environments.  
- Display a **status message or indicator** when gesture confidence is low, helping users understand the uncertainty.


**\*\*\*Think about someone using the system. Describe how you think this will work.\*\*\***

From a user’s point of view, the interaction feels **immediate and intuitive** — the lights react quickly enough to feel like real feedback.  
Most users would not notice the underlying uncertainty unless the flickering happens repeatedly.  
A misclassification would only cause a light to toggle incorrectly, which is a **minor inconvenience** rather than a critical failure.  
To improve usability, I could smooth transitions or average recognition confidence over several frames before changing the LED output.

Overall, this flight test shows that even simple vision-based sensing can create expressive, real-time physical interactions — as long as environmental conditions and system feedback are thoughtfully managed.


### Part D
### Characterize your own Observant system

After experimenting with the MediaPipe Hands + Qwiic GPIO system, I can describe its behavior as a material for interaction design — how it reacts, what it enables, and where it fails.

In this version:
- Added a **debounce delay** to smooth out flicker and avoid rapid switching.  
- Introduced a **minimum-distance threshold difference** between the thumb–index and thumb–pinky pairs to better distinguish Pinch from Quiet Coyote.  
- Reversed the LED logic so lights start **off by default**, making the interaction behavior more natural and readable.  


| Question | Reflection |
|-----------|-------------|
| **What can you use X for?** | This system can be used to create **gesture-based control** for physical devices — such as lights, motors, or interfaces — without needing touch or buttons. It demonstrates how computer-vision sensing can drive tangible feedback in real time. |
| **What is a good environment for X?** | Works best in **moderate or dim indoor lighting**, where hand contours are clear and shadows are soft. A steady camera position and a neutral background improve accuracy. |
| **What is a bad environment for X?** | Bright sunlight, reflections, or cluttered backgrounds reduce detection accuracy. Outdoor environments or moving backgrounds can confuse the model. |
| **When will X break?** | The system breaks when the **camera loses sight of the hand**, when **light changes suddenly**, or when **CPU load** on the Pi becomes too high. It may also fail if multiple hands appear in view. |
| **When it breaks, how will X break?** | LEDs may **freeze in their last state**, or **flicker** rapidly as the system struggles to classify gestures. Sometimes the camera feed lags or stops updating until restarted. |
| **What are other properties/behaviors of X?** | The system is **responsive, expressive, and scalable** — it can support additional gestures or outputs with minimal code changes. However, it is sensitive to visual noise and environmental variability. |
| **How does X feel?** | It feels **intuitive and alive** — as if the system is watching and reacting to my motion. The connection between sight and light creates a satisfying sense of feedback and presence. |


**\*\*\*Include a short video demonstrating the answers to these questions.\*\*\***


The video shows:
1. Each gesture and its corresponding LED color (Yellow – Pinch, White – Open Hand, Blue – Quiet Coyote).  
2. The smooth transitions after logic and debounce adjustments.  



### Part 2.

Following exploration and reflection from Part 1, finish building your interactive system, and demonstrate it in use with a video.

**\*\*\*Include a short video demonstrating the finished result.\*\*\***
