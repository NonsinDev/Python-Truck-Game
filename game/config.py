import json

DEFAULT_CONFIG_FILE = "default_config.json"


def load_game_modes():
    with open(DEFAULT_CONFIG_FILE, "r") as f:
        return json.load(f)


GAME_MODES = load_game_modes()
