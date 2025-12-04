from flask import Flask, Response
import threading
import time
import numpy as np
import cv2

from animation.animation_engine import AnimationEngine
from sensors.sensor_manager import SensorManager

app = Flask(__name__)

engine = AnimationEngine()
sensors = SensorManager()

latest_frame = None
frame_lock = threading.Lock()

print("System Started (Web Mode). Running Pygame in MAIN thread.")


# ---------------------------------------------------------
# MJPEG STREAM
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

            # yield MJPEG frame
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" +
                jpeg.tobytes() + b"\r\n"
            )
            time.sleep(0.03)

    return Response(gen(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


# ---------------------------------------------------------
# FLASK BACKGROUND THREAD
# ---------------------------------------------------------
def start_flask():
    app.run(host="0.0.0.0", port=8080, debug=False, threaded=True)


# ---------------------------------------------------------
# MAIN PYGAME LOOP
# ---------------------------------------------------------
def pygame_loop():
    global latest_frame

    while True:
        # read sensors
        data = sensors.update()

        element = data.get("element")
        gesture = data.get("gesture")
        cam_frame = data.get("frame")
        profile = data.get("profile")
        proximity = data.get("proximity")

        # update animation
        engine.update(profile=profile,
                      element=element,
                      gesture=gesture,
                      proximity=proximity,
                      frame=cam_frame)

        # read pygame screen → numpy array
        surf = engine.get_frame_surface()
        if surf is not None:
            frame = np.transpose(surf, (1, 0, 2))
            bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            # store for flask
            with frame_lock:
                latest_frame = bgr

        time.sleep(0.01)


# ---------------------------------------------------------
# START
# ---------------------------------------------------------
if __name__ == "__main__":
    threading.Thread(target=start_flask, daemon=True).start()
    pygame_loop()  # must be main thread
