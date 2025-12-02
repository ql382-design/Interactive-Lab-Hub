from sensors.sensor_manager import SensorManager
from animation.animation_engine import AnimationEngine
import time

def main():
    sensors = SensorManager()
    engine = AnimationEngine()

    print("System Started. Waiting for interactions...")

    user_profile_locked = False
    user_profile = None

    while True:
        data = sensors.update()

        # -------------------------------
        # 1. Profile (chosen 3 elements)
        # -------------------------------
        if not user_profile_locked and data["profile"] is not None:
            user_profile_locked = True
            user_profile = data["profile"]
            print(f"[Main] Profile locked: {user_profile}")

            # Pass the 3-element profile to animation engine
            try:
                engine.set_profile(user_profile)
                print("[Main] Animation engine profile applied.")
            except Exception as e:
                print(f"[Main] Error passing profile to engine: {e}")

        # -------------------------------------
        # 2. Element (only used BEFORE profile)
        # -------------------------------------
        element = None
        if not user_profile_locked:
            element = data["element"]     # still allow single-element mode

        # -------------------------------------
        # 3. Gesture + Camera frame
        # -------------------------------------
        gesture = data["gesture"]
        frame = data["frame"]

        # -------------------------------------
        # 4. Send to animation engine
        # -------------------------------------
        try:
            engine.update(
                element=element,  # only active before profile locked
                gesture=gesture,
                frame=frame
            )
        except Exception as e:
            print(f"[Main] Animation update error: {e}")

        time.sleep(0.01)


if __name__ == "__main__":
    main()
