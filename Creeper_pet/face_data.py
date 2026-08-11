"""
Data describing the creeper sprite: which image file to use, and
where its eyes sit so the pet window knows where to draw the moving
"watching" pupils.

Eye positions are loaded from assets/eye_config.json if it exists
(created by running calibrate.py), otherwise these defaults are used.
"""

import json
import os

IMAGE_FILE = "creeper.png"

_DEFAULT_EYE_CENTERS = [(24.2, 51.1), (40.2, 59.3)]

_ASSETS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets"
)
_CONFIG_PATH = os.path.join(_ASSETS_DIR, "eye_config.json")


def _load_eye_centers():
    try:
        with open(_CONFIG_PATH) as f:
            data = json.load(f)
        return [tuple(point) for point in data["eyes"]]
    except (FileNotFoundError, KeyError, ValueError):
        return _DEFAULT_EYE_CENTERS


EYE_CENTERS = _load_eye_centers()

# Softer, smaller pupil -- a plain pale dot reads more natural inside
# such a small eye hole than a hard-outlined circle.
PUPIL_COLOR = "#F2FFEE"
PUPIL_RADIUS = 1.5
