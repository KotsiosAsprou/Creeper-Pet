# Desktop Creeper

A small version of your creeper artwork that sits in the corner of your
screen and watches your mouse cursor with two tiny moving eye-glints.
Built with Python's standard library only (`tkinter`) -- no dependencies
to install.

## Run it

```bash
python main.py
```

## Controls

- **Left-click + drag** -- move the creeper (overrides its corner for this session)
- **Right-click** -- quit
- **Escape** -- quit

## Project structure

```
desktop_creeper/
├── main.py                    # entry point
├── calibrate.py                # eye calibration tool
├── assets/
│   └── creeper.png             # the creeper artwork, pre-sized
├── creeper_pet/
│   ├── __init__.py
│   ├── config.py               # corner, margin, speed
│   ├── face_data.py            # image filename + eye coordinates
│   └── pet_window.py           # the window + animation logic
└── README.md
```

## If the eyes look off

Run the calibration tool:

```bash
python calibrate.py
```

A zoomed-in window opens. Click the left eye, then the right eye. Your
clicks are saved to `assets/eye_config.json`, and `main.py` will use
them automatically from then on -- no need to edit any code.

## Customize it

All the knobs live in `creeper_pet/config.py`:

| Setting          | What it does                                      |
|-------------------|---------------------------------------------------|
| `CORNER`          | `"top-left"`, `"top-right"`, `"bottom-left"`, `"bottom-right"` |
| `MARGIN`          | distance from the screen edge, in pixels          |
| `FPS`             | animation refresh rate                            |
| `EYE_MAX_SHIFT`   | how far the glints travel inside the eyes         |

### Using your own image

Replace `assets/creeper.png` with any transparent PNG. You'll then need
to re-measure where its eyes are and update `EYE_CENTERS` in
`creeper_pet/face_data.py` -- those are pixel coordinates `(x, y)` on the
image, measured from its top-left corner. If you're not sure how to find
them, open the image in any image editor that shows a pixel cursor
position (like Paint, GIMP, or Preview) and hover over each eye.

### Changing the size

Resize `assets/creeper.png` itself (e.g. in an image editor, or with
Python's Pillow library: `Image.open(...).resize((w, h))`), then re-measure
and update `EYE_CENTERS` to match the new size, since the coordinates
scale with the image.

## Ideas to extend this project

- **Idle animation**: add a periodic "wiggle" or hiss-shake even when the
  mouse isn't moving, using `root.after` on a timer.
- **Click reaction**: bind a quick `<Button-1>` click (not drag) to flash
  the sprite white for a frame, like a creeper about to explode.
- **Multiple pets**: instantiate more than one `DesktopCreeper`, each
  with its own `Tk()` root (or `Toplevel` if sharing one root).
- **Follow-then-rest behavior**: have it walk to a random spot along the
  screen edge every so often instead of staying fixed in one corner.
- **System tray icon**: pair with a library like `pystray` to add a
  right-click tray menu (pause, change corner, quit).

## Platform notes on transparency

- **Windows**: works out of the box -- `-transparentcolor` makes the
  magenta background fully invisible.
- **macOS**: `-transparentcolor` isn't supported by Tk. Use
  `root.attributes("-alpha", 0.0)` tricks, or consider a
  `pygame`/`pyglet` window with an alpha channel for a cleaner result.
- **Linux**: depends on your window manager's compositor. With a
  compositing WM (most modern ones), try
  `root.attributes("-alpha", <0-1>)` for whole-window transparency.
  A `pygame`-based version with a colorkey tends to be more portable
  if Tk transparency misbehaves on your WM.
