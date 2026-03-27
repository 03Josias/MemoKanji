
import json
import os

CONFIG_PATH = "config.json"

def load_config():
    """Carga el archivo config o crea uno nuevo si no existe."""
    if not os.path.exists(CONFIG_PATH):
        default_config = {
            "tutorial_visto": False,
            "sound_enabled": True
        }
        save_config(default_config)
        return default_config

    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def save_config(data: dict):
    """Guarda los valores en config.json."""
    with open(CONFIG_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def get_sound_enabled():
    config = load_config()
    return config.get("sound_enabled", True)

def set_tutorial(value: bool):
    config = load_config()
    config["tutorial_visto"] = value
    save_config(config)

def set_sound_enabled(value: bool):
    config = load_config()
    config["sound_enabled"] = value
    save_config(config)


def toggle_sound():
    config = load_config()
    new_value = not config.get("sound_enabled", True)
    config["sound_enabled"] = new_value
    save_config(config)
    return new_value