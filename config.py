from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
SOUNDS_DIR = ASSETS_DIR / "sounds"
MUSIC_DIR = ASSETS_DIR / "music"

WINDOW_WIDTH = 1365
WINDOW_HEIGHT = 768
FPS = 60
TITLE = "Математический остров"

COLORS = {
    "sky_top": (48, 142, 255),
    "sky_bottom": (131, 214, 255),
    "water": (70, 190, 225),
    "button_main": (255, 185, 20),
    "button_shadow": (185, 95, 20),
    "text_light": (245, 248, 255),
}
