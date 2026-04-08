"""
config.py — all the knobs in one place.

Loads environment variables and defines the constants used across the app.
Anything that might change between machines (API keys, hotkey combos, audio
settings) lives here so the rest of the code never has to think about it.
"""

import os
from dotenv import load_dotenv

# Pull in whatever's in .env (ignored in prod if vars are already set)
load_dotenv()


# ── API ───────────────────────────────────────────────────────────────────────
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

# gpt-4o-mini-transcribe: fast, accurate, cheap. upgrade to gpt-4o-transcribe
# if you need better accuracy on accents or noisy environments.
MODEL: str = os.getenv("TRANSCRIPTION_MODEL", "gpt-4o-mini-transcribe")

# ── Hotkey ────────────────────────────────────────────────────────────────────

# The key combo that triggers recording. Hold to record, release to transcribe.
# Stored as a plain string — hotkey_listener.py parses it into pynput keys.
HOTKEY: str = os.getenv("HOTKEY", "ctrl+shift+space")


# ── Audio ─────────────────────────────────────────────────────────────────────

AUDIO_SAMPLERATE: int = 44100   # 44.1kHz — CD quality, plenty for speech
AUDIO_CHANNELS: int = 1         # mono is fine for transcription
AUDIO_FORMAT: str = "wav"       # whisper handles wav without any extra steps

# Absolute path to the temp recording file — overwritten on each use
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMP_AUDIO_PATH: str = os.path.join(_project_root, "temp", "recording.wav")


# ── Sanity check ─────────────────────────────────────────────────────────────

def validate():
    """
    Confirms the minimum required config is present before the app starts.
    Raises EnvironmentError if OPENAI_API_KEY is missing.
    """
    if not OPENAI_API_KEY:
        raise EnvironmentError(
            "OPENAI_API_KEY is not set.\n"
            "  → Add it to your .env file: OPENAI_API_KEY=sk-..."
        )
