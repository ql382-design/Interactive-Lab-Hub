from flask import Flask, Response
import pygame
import numpy as np
import io
from PIL import Image

from animation.animation_engine import AnimationEngine
from sensors.sensor_manager import SensorManager
import time

app = Flask(__name__)

engine = AnimationEngine()
sensors = SensorManager()

print("System Started (Web Mode).")

@app.route("/frame")
def frame_feed():
    """Returns latest frame as JPEG."""
    frame = engine.get_frame_surface()

    # pygame array is (width, height, 3), convert to (height, width, 3)
    frame = np.transpose(frame, (1, 0, 2))

    img = Image.fromarray(frame)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=80)
    buf.seek(0)

    return Response(buf.read(), mimetype="image/jpeg")


def main_loop():
    """Runs animation in background while Flask serves frames."""
    while True:
        data = sensors.update()
        element = data["element"]
        gesture = data["gesture"]
        frame = data["frame"]

        engine.update(element=element, gesture=gesture, frame=frame)
        time.sleep(0.01)


if __name__ == "__main__":
    import threading

    # Run animation loop in background
    t = threading.Thread(target=main_loop)
    t.daemon = True
    t.start()

    # Run Flask Web Server
    app.run(host="0.0.0.0", port=8080, debug=False, threaded=True)

