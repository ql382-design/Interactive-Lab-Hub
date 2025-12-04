from flask import Flask, Response
import threading
import time
import numpy as np
import cv2

from animation.animation_engine import AnimationEngine
from sensors.sensor_manager import SensorManager

# ---------------------------------------------------------
# GLOBAL INITIALIZATION
# ---------------------------------------------------------
app = Flask(__name__)

engine = AnimationEngine()
sensors = SensorManager()

latest_frame = None
frame_lock = threading.Lock()

print("System Started (Web Mode). Running Pygame in MAIN thread.")


# ---------------------------------------------------------
# FLASK ROUTE - MJPEG STREAM
# ---------------------------------------------------------
@app.route("/frame")
def frame_feed():
    """Returns MJPEG stream from pygame animation."""
    def gen():
        global latest_frame
        while True:
            with frame_lock:
                if latest_frame is None:
                    time.sleep(0.05)
                    continue
                ret, jpeg = cv2.imencode(".jpg", latest_frame)
                if not ret:
                    continue
            yield (b"--frame\r\n"
                   b"Content-Type: image/jpeg\r\n\r\n" +
                   jpeg.tobytes() + b"\r\n")
            time.sleep(0.03)

    return Response(gen(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


# ---------------------------------------------------------
# FLASK THREAD
# ---------------------------------------------------------
def start_flask():
    app.run(host="0.0.0.0", port=8080, debug=False, threaded=True)


# ---------------------------------------------------------
# MAIN PYGAME LOOP (must run in MAIN THREAD)
# ---------------------------------------------------------
def pygame_loop():
    global latest_frame

    while True:
        # Sensor update
        data = sensors.update()
        element = data.get("element")
        gesture = data.get("gesture")
        cam_frame = data.get("frame")

        # Update animation
        engine.update(element=element, gesture=gesture, frame=cam_frame)

        # Convert pygame surface to numpy array
        surf = engine.get_frame_surface()
        if surf is not None:
            # pygame surface: (W, H, 3) → transpose to (H, W, 3)
            frame = np.transpose(surf, (1, 0, 2))
            bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            with frame_lock:
                latest_frame = bgr

        time.sleep(0.01)


# ---------------------------------------------------------
# EXECUTION START
# ---------------------------------------------------------
if __name__ == "__main__":
    # Start Flask server in background thread
    threading.Thread(target=start_flask, daemon=True).start()

    # Run Pygame animation in MAIN THREAD
    pygame_loop()
