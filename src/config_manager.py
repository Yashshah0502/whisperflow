"""
config_manager.py — persistent user config via whisperflow.json.

Reads and writes a JSON file in the project root so settings survive restarts.
On first run the file is created with defaults. config.py loads from here so
users can tweak things without touching code or environment variables.
"""

import json
import os


_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(_PROJECT_ROOT, "whisperflow.json")

DEFAULTS: dict = {
    "hotkey": "ctrl+shift+space",
    "model": "gpt-4o-mini-transcribe",
    "samplerate": 44100,
    "channels": 1,
    "language": None,
}


def load_config() -> dict:
    """
    Reads whisperflow.json and returns its contents merged with defaults.

    Creates the file with defaults if it doesn't exist yet (first run).
    Unknown keys in the file are preserved — useful for future settings.

    Returns:
        dict with all config keys, falling back to DEFAULTS for anything missing.
    """
    if not os.path.exists(CONFIG_PATH):
        save_config({})  # write defaults on first run

    with open(CONFIG_PATH, "r") as f:
        data = json.load(f)

    return {**DEFAULTS, **data}


def save_config(updates: dict) -> dict:
    """
    Merges updates into the current config and writes it back to disk.

    Safe to call with an empty dict — just writes defaults if the file is new.

    Args:
        updates: keys/values to add or overwrite

    Returns:
        The full config dict after merging.
    """
    current: dict = {}
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            current = json.load(f)

    merged = {**DEFAULTS, **current, **updates}

    with open(CONFIG_PATH, "w") as f:
        json.dump(merged, f, indent=2)
        f.write("\n")  # trailing newline — editors appreciate it

    return merged
