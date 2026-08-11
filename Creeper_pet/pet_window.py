"""
The DesktopCreeper window: your creeper artwork pinned to a screen
corner, with small eye "glints" that shift toward your mouse cursor
so it looks like it's watching you.
"""

import tkinter as tk
import math
import os

from . import config
from . import face_data

ASSETS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets"
)


class DesktopCreeper:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)          # no titlebar / border
        self.root.attributes("-topmost", True)     # always on top

        image_path = os.path.join(ASSETS_DIR, face_data.IMAGE_FILE)
        self.image = tk.PhotoImage(file=image_path)
        self.width = self.image.width()
        self.height = self.image.height()

        x, y = self._corner_position()
        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")

        # Transparent background so only the creeper shows (see README
        # for platform notes -- this works best on Windows).
        self.root.config(bg=config.TRANSPARENT_KEY)
        self.root.attributes("-transparentcolor", config.TRANSPARENT_KEY)

        self.canvas = tk.Canvas(
            self.root, width=self.width, height=self.height,
            bg=config.TRANSPARENT_KEY, highlightthickness=0
        )
        self.canvas.pack()

        # Right-click or Escape to quit. Left-click drag to reposition
        # (overrides the configured corner for the rest of the session).
        self.canvas.bind("<ButtonPress-1>", self._start_drag)
        self.canvas.bind("<B1-Motion>", self._do_drag)
        self.canvas.bind("<Button-3>", lambda e: self.root.destroy())
        self.root.bind("<Escape>", lambda e: self.root.destroy())

        self._animate()

    def _corner_position(self):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        m = config.MARGIN

        if config.CORNER == "top-left":
            return m, m
        elif config.CORNER == "top-right":
            return sw - self.width - m, m
        elif config.CORNER == "bottom-left":
            return m, sh - self.height - m
        else:  # "bottom-right" (default)
            return sw - self.width - m, sh - self.height - m

    def _start_drag(self, event):
        self._drag_start = (event.x, event.y)

    def _do_drag(self, event):
        dx, dy = self._drag_start
        x = self.root.winfo_pointerx() - dx
        y = self.root.winfo_pointery() - dy
        self.root.geometry(f"+{x}+{y}")

    def _draw(self, pupil_offset=(0, 0)):
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.image)

        ox, oy = pupil_offset
        r = face_data.PUPIL_RADIUS
        for (ex, ey) in face_data.EYE_CENTERS:
            gx, gy = ex + ox, ey + oy
            self.canvas.create_oval(
                gx - r, gy - r, gx + r, gy + r,
                fill=face_data.PUPIL_COLOR, outline=""
            )

    def _animate(self):
        wx = self.root.winfo_x() + self.width / 2
        wy = self.root.winfo_y() + self.height / 2
        mx = self.root.winfo_pointerx()
        my = self.root.winfo_pointery()

        angle = math.atan2(my - wy, mx - wx)
        shift = config.EYE_MAX_SHIFT
        offset = (math.cos(angle) * shift, math.sin(angle) * shift)

        self._draw(pupil_offset=offset)
        self.root.after(int(1000 / config.FPS), self._animate)

    def run(self):
        self.root.mainloop()
