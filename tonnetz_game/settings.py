import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_PATH = os.path.join(BASE_DIR, "user_settings.json")

DEFAULT_SETTINGS = {
    "SCREEN_WIDTH": 800,
    "SCREEN_HEIGHT": 600,

    "PLAYER_1": 1,
    "PLAYER_2": 2,

    "P1COLOR": [0, 255, 255],
    "P2COLOR": [255, 0, 255],
    "COLOR3": [255, 255, 0],

    "P1SOUND": "celeste",
    "P2SOUND": "celeste",

    "P1MODE": "player",
    "P2MODE": "player",

    "PING_VOLUME": 0.8,
    "MUSIC_VOLUME": 0.6,

    "STARTING_POSITIONS": "balanced",
    "STARTING_PLAYER": 1,

    "VERSION" : "Beta 1.0"
}

def load_settings():
    if os.path.exists(SETTINGS_PATH):
        with open(SETTINGS_PATH, "r") as f:
            return json.load(f)
    return DEFAULT_SETTINGS.copy()

def save_settings():
    current_settings = {
        "SCREEN_WIDTH": SCREEN_WIDTH,
        "SCREEN_HEIGHT": SCREEN_HEIGHT,

        "PLAYER_1": PLAYER_1,
        "PLAYER_2": PLAYER_2,

        "P1COLOR": list(P1COLOR),
        "P2COLOR": list(P2COLOR),
        "COLOR3": list(COLOR3),

        "P1SOUND": P1SOUND,
        "P2SOUND": P2SOUND,

        "P1MODE": P1MODE,
        "P2MODE": P2MODE,

        "PING_VOLUME": PING_VOLUME,
        "MUSIC_VOLUME": MUSIC_VOLUME,

        "STARTING_POSITIONS": STARTING_POSITIONS,
        "STARTING_PLAYER": STARTING_PLAYER,

        "VERSION" : VERSION
    }

    with open(SETTINGS_PATH, "w") as f:
        json.dump(current_settings, f, indent=2)


_settings = load_settings()

SCREEN_WIDTH = _settings["SCREEN_WIDTH"]
SCREEN_HEIGHT = _settings["SCREEN_HEIGHT"]

PLAYER_1 = _settings["PLAYER_1"]
PLAYER_2 = _settings["PLAYER_2"]

P1COLOR = tuple(_settings["P1COLOR"])
P2COLOR = tuple(_settings["P2COLOR"])
COLOR3 = tuple(_settings["COLOR3"])

P1SOUND = _settings["P1SOUND"]
P2SOUND = _settings["P2SOUND"]

P1MODE = _settings["P1MODE"]
P2MODE = _settings["P2MODE"]

PING_VOLUME = _settings["PING_VOLUME"]
MUSIC_VOLUME = _settings["MUSIC_VOLUME"]

STARTING_POSITIONS = _settings["STARTING_POSITIONS"]
STARTING_PLAYER = _settings["STARTING_PLAYER"]

VERSION = _settings["VERSION"]