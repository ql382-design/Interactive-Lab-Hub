import time
import board
import busio
import adafruit_mpr121

class TouchElementSelector:
    def __init__(self, oled=None):
        i2c = board.I2C()
        self.mpr121 = adafruit_mpr121.MPR121(i2c)
        self.oled = oled

        self.element_map = {
            0: "Fire",
            1: "Water",
            2: "Wind",
            3: "Earth",
            4: "Light",
            5: "Shadow",
        }

        self.selected = []      # user-selected 3 elements
        self.selection_done = False

        print("[Touch] Element selector initialized.")

    def update(self):
        """Check MPR121 touch and collect up to 3 unique elements."""
        if self.selection_done:
            return None  # no more selection

        for i in range(6):
            if self.mpr121[i].value:   # touched
                elem = self.element_map[i]

                if elem not in self.selected:
                    self.selected.append(elem)
                    print(f"[Touch] Selected: {elem}")

                    # update OLED
                    if self.oled:
                        self.oled.show_element_list(self.selected)

                time.sleep(0.4)  # debounce

                if len(self.selected) == 3:
                    self.selection_done = True
                    print(f"[Touch] Final profile selected → {self.selected}")
                    return self.selected

        return None
