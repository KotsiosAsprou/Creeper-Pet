"""
Eye calibration tool.

If the pupils look off, run this. It opens the creeper image zoomed in
so you can click precisely: first the LEFT eye, then the RIGHT eye.
Your clicks are saved to assets/eye_config.json, and main.py picks
them up automatically the next time you run it.

    python calibrate.py
"""

import tkinter as tk
import json
import os

ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
IMAGE_PATH = os.path.join(ASSETS_DIR, "creeper.png")
CONFIG_PATH = os.path.join(ASSETS_DIR, "eye_config.json")

ZOOM = 5  # how much to zoom in, for easier/more precise clicking


class Calibrator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Creeper Eye Calibration")

        original = tk.PhotoImage(file=IMAGE_PATH)
        self.image = original.zoom(ZOOM, ZOOM)  # keep a reference, or Tk will garbage-collect it

        self.label = tk.Label(
            self.root,
            text="Click the LEFT eye, then the RIGHT eye",
            font=("Segoe UI", 12), pady=8
        )
        self.label.pack()

        self.canvas = tk.Canvas(
            self.root, width=self.image.width(), height=self.image.height()
        )
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor="nw", image=self.image)
        self.canvas.bind("<Button-1>", self.on_click)

        self.clicks = []
        self.root.mainloop()

    def on_click(self, event):
        # convert the zoomed-in click position back to original image coordinates
        x, y = round(event.x / ZOOM, 1), round(event.y / ZOOM, 1)
        self.clicks.append((x, y))

        r = 6
        self.canvas.create_oval(
            event.x - r, event.y - r, event.x + r, event.y + r,
            outline="red", width=2
        )

        if len(self.clicks) == 1:
            self.label.config(text="Got it. Now click the RIGHT eye")
        elif len(self.clicks) == 2:
            self.save()
            self.label.config(text="Saved! Close this window and run main.py")
            self.canvas.unbind("<Button-1>")

    def save(self):
        with open(CONFIG_PATH, "w") as f:
            json.dump({"eyes": self.clicks}, f, indent=2)
        print("Saved eye coordinates to", CONFIG_PATH, "->", self.clicks)


if __name__ == "__main__":
    Calibrator()
