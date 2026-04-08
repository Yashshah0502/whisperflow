"""
config.py — all the knobs in one place.

Priority for every setting:
  1. Environment variable   (highest — good for CI / secrets)
  2. whisperflow.json       (user's persistent config)
  3. Hardcoded default      (fallback if nothing else is set)

Edit whisperflow.json to change hotkey, model, language, etc.
Only OPENAI_API_KEY needs to be in .env — it's a secret.
"""

import os
from dotenv import load_dotenv
from src import config_manager

load_dotenv()

# Load the user's JSON config (creates the file with defaults on first run)
_cfg = config_manager.load_config()


# ── API ───────────────────────────────────────────────────────────────────────

OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

# Override the model via env var or whisperflow.json
MODEL: str = os.getenv("TRANSCRIPTION_MODEL") or _cfg["model"]

# ── Hotkey ────────────────────────────────────────────────────────────────────

HOTKEY: str = os.getenv("HOTKEY") or _cfg["hotkey"]

# ── Audio ─────────────────────────────────────────────────────────────────────

AUDIO_SAMPLERATE: int = _cfg["samplerate"]
AUDIO_CHANNELS: int = _cfg["channels"]
AUDIO_FORMAT: str = "wav"

_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMP_AUDIO_PATH: str = os.path.join(_project_root, "temp", "recording.wav")

# ── Transcription language ────────────────────────────────────────────────────

# None = let OpenAI auto-detect (works great for most cases).
# Set to an ISO-639-1 code in whisperflow.json to force a language:
#   "language": "en"   → English
#   "language": "hi"   → Hindi
#   "language": "gu"   → Gujarati
LANGUAGE: str | None = _cfg.get("language") or None

# ── Sanity check ─────────────────────────────────────────────────────────────

def validate():
    """Raises EnvironmentError if OPENAI_API_KEY is missing."""
    if not OPENAI_API_KEY:
        raise EnvironmentError(
            "OPENAI_API_KEY is not set.\n"
            "  → Add it to your .env file: OPENAI_API_KEY=sk-..."
        )
