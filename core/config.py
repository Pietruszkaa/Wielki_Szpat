import json
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

if not DISCORD_TOKEN:
    raise RuntimeError("DISCORD_TOKEN not set")


_CONFIG = None
_CONFIG_PATH = Path("config/config.json")


def load_config() -> dict:
    global _CONFIG
    with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
        _CONFIG = json.load(f)
    return _CONFIG


def get_config() -> dict:
    if _CONFIG is None:
        raise RuntimeError("Config not loaded")
    return _CONFIG
