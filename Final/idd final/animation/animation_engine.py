# animation/animation_engine.py

import pygame
import math
import random

try:
    import cv2
    import numpy as np
except ImportError:
    cv2 = None
    np = None

from animation.set_profile import get_spectrum_style


class AnimationEngine:
    def __init__(self, width=1280, height=720):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Inner Constellation")
        self.clock = pygame.time.Clock()

        # Profile / element state
        self.current_element = None
        self.current_profile = None
        self.spectrum_name = "None"

        # Style from set_profile
        self.style = get_spectrum_style([])

        # Energy scale and temperature
        self.scale = 1.0
        self.temp_shift = 0.0

        # Time & Energy
        self.time = 0.0
        self.motion_level = 0.0
        self.proximity_level = 0.0

        # Camera motion analysis
        self.prev_gray = None
        self.downsample_size = (64, 36)

        # Persistent orbs
        self.orbs = []

        # Gesture display
        self.last_gesture = None

        # Base single-element colors
        self.element_colors = {
            "Fire": [(255, 120, 60), (255, 200, 90)],
            "Water": [(60, 140, 255), (110, 220, 255)],
            "Wind": [(190, 230, 255), (150, 210, 255)],
            "Earth": [(90, 160, 100), (170, 220, 150)],
            "Light": [(255, 255, 255), (255, 240, 210)],
            "Shadow": [(120, 70, 160), (60, 30, 100)],
        }

    # ------------------------------------------------------------------
    def update(self, profile=None, element=None, gesture=None, proximity=None, frame=None):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

        # Profile / element
        if profile is not None and profile != self.current_profile:
            self.current_profile = profile
            self.current_element = None
            self.style = get_spectrum_style(profile)
            self.spectrum_name = self.style.get("name", "Spectrum")
            self.orbs.clear()
            print(f"[Animation] Spectrum profile -> {self.spectrum_name}")

        if self.current_profile is None and element is not None and element != self.current_element:
            self.current_element = element
            self.spectrum_name = element
            self.style = get_spectrum_style([element])
            self.orbs.clear()
            print(f"[Animation] Element -> {element}")

        # Gestures
        if gesture:
            self.last_gesture = gesture
            if gesture == "expand":
                self.scale = min(3.0, self.scale + 0.1)
            elif gesture == "shrink":
                self.scale = max(0.5, self.scale - 0.1)
            elif gesture == "cooler":
                self.temp_shift = max(-1.0, self.temp_shift - 0.05)
            elif gesture == "warmer":
                self.temp_shift = min(1.0, self.temp_shift + 0.05)

        # Proximity
        if proximity is not None:
            self.proximity_level = 0.8 * self.proximity_level + 0.2 * proximity

        # Time
        dt_ms = self.clock.get_time()
        dt = dt_ms / 1000.0 if dt_ms > 0 else 1.0 / 60.0
        self.time += dt

        # Camera motion
        if frame is not None and cv2 is not None and np is not None:
            self._update_motion_energy(frame)

        # Breathing & scale
        breath_from_motion = 1.0 + 0.7 * self.motion_level
        breath_from_proximity = 1.0 + 0.9 * self.proximity_level
        breathing_wave = 1.0 + 0.22 * math.sin(self.time * 2.0 * math.pi * 0.4)

        self.scale *= 0.99
        self.scale = max(0.7, min(2.7, self.scale))

        self.render_scale = self.scale * breath_from_motion * breath_from_proximity * breathing_wave

        # Draw frame
        self._draw_frame(frame, dt)
        pygame.display.flip()
        self.clock.tick(60)

    # ------------------------------------------------------------------
    def _update_motion_energy(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_small = cv2.resize(gray, self.downsample_size)

        if self.prev_gray is None:
            self.prev_gray = gray_small
            self.motion_level = 0.0
            return

        diff = cv2.absdiff(gray_small, self.prev_gray)
        self.prev_gray = gray_small

        mean_diff = diff.mean() / 255.0
        self.motion_level = 0.85 * self.motion_level + 0.15 * min(1.0, mean_diff * 8.0)

    # ------------------------------------------------------------------
    def _draw_frame(self, frame, dt):
        if self.current_profile is not None or self.current_element is not None:
            base_colors = self.style.get("base_colors", [(255, 255, 255), (200, 200, 200)])
        else:
            base_colors = [(255, 255, 255), (200, 200, 200)]

        warm = (255, 190, 90)
        cold = (70, 150, 255)
        temp_tint = self._lerp_color(cold, warm, (self.temp_shift + 1) / 2)
        bg = self._lerp_color((0, 0, 0), temp_tint, 0.18)
        self.screen.fill(bg)

        if frame is not None and cv2 is not None:
            self._blit_camera(frame)

        pattern_type = self.style.get("pattern_type", "pillar_orbs")

        if pattern_type == "pillar_orbs":
            self._pattern_pillar_orbs(base_colors, dt)
        elif pattern_type == "ring_waves":
            self._pattern_ring_waves(base_colors)
        elif pattern_type == "radial_rays":
            self._pattern_radial_rays(base_colors)
        elif pattern_type == "galaxy":
            self._pattern_galaxy(base_colors)
        elif pattern_type == "double_pillar":
            self._pattern_double_pillar(base_colors)
        elif pattern_type == "vertical_ribbons":
            self._pattern_vertical_ribbons(base_colors)
        elif pattern_type == "grid_pulse":
            self._pattern_grid_pulse(base_colors)
        elif pattern_type == "starfield":
            self._pattern_starfield(base_colors)
        elif pattern_type == "vortex":
            self._pattern_vortex(base_colors)
        elif pattern_type == "cross_waves":
            self._pattern_cross_waves(base_colors)
        else:
            self._pattern_pillar_orbs(base_colors, dt)

        self._draw_label()

   
    # ------------------------------------------------------------------
    def _blit_camera(self, frame):
        try:
            h, w = frame.shape[:2]
        except Exception:
            return

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        scale = min(self.width / w, self.height / h)
        new_size = (int(w * scale), int(h * scale))
        frame_resized = cv2.resize(frame_rgb, new_size)

        surf = pygame.surfarray.make_surface(frame_resized.swapaxes(0, 1))
        surf.set_alpha(70)
        x = (self.width - new_size[0]) // 2
        y = (self.height - new_size[1]) // 2
        self.screen.blit(surf, (x, y))

    # ------------------------------------------------------------------
    def _draw_label(self):
        font = pygame.font.SysFont("arial", 26)
        title = f"Energy Field: {self.spectrum_name}"
        self.screen.blit(font.render(title, True, (245, 245, 245)), (20, 18))

        if self.current_profile:
            elements_str = " · ".join(self.current_profile)
        elif self.current_element:
            elements_str = self.current_element
        else:
            elements_str = "None"

        sub_font = pygame.font.SysFont("arial", 22)
        self.screen.blit(sub_font.render(f"Elements: {elements_str}", True, (230, 230, 230)), (20, 50))

        gesture_str = self.last_gesture if self.last_gesture else "none"
        self.screen.blit(sub_font.render(f"Gesture: {gesture_str}", True, (230, 230, 230)), (20, 80))

        debug_font = pygame.font.SysFont("arial", 16)
        self.screen.blit(debug_font.render(f"Energy(cam): {self.motion_level:.2f}", True, (220, 220, 220)), (20, 108))
        self.screen.blit(debug_font.render(f"Energy(hand): {self.proximity_level:.2f}", True, (220, 220, 220)), (20, 128))

    # ------------------------------------------------------------------
    def _lerp_color(self, c1, c2, t):
        t = max(0.0, min(1.0, t))
        return (
            int(c1[0] + (c2[0] - c1[0]) * t),
            int(c1[1] + (c2[1] - c1[1]) * t),
            int(c1[2] + (c2[2] - c1[2]) * t),
        )

    # ------------------------------------------------------------------
    def reset_profile(self):
        self.current_profile = None
        self.current_element = None
        self.spectrum_name = "None"
        self.style = get_spectrum_style([])
        self.orbs.clear()
        self.last_gesture = None
        print("[Animation] Profile cleared. Waiting for new selection.")

    # ------------------------------------------------------------------
    def get_frame_surface(self):
        """Return the current pygame surface as an RGB image (numpy array)."""
        import pygame
        surface = pygame.display.get_surface()
        if surface is None:
            return None
        return pygame.surfarray.array3d(surface)
