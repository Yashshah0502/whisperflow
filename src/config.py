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

# Model used for transcription. gpt-4o-mini-transcribe is fast and cheap.
TRANSCRIPTION_MODEL: str = os.getenv("TRANSCRIPTION_MODEL", "gpt-4o-mini-transcribe")


# ── Hotkey ────────────────────────────────────────────────────────────────────

# The key combo that starts/stops recording.
# Default: Right Option (alt_r). Change this to whatever feels natural.
# TODO: make this configurable via .env or a small config file
HOTKEY: str = os.getenv("HOTKEY", "<alt_r>")


# ── Audio ─────────────────────────────────────────────────────────────────────

SAMPLE_RATE: int = 16_000       # 16kHz — good enough for speech, not overkill
CHANNELS: int = 1               # mono, we don't need stereo for voice
AUDIO_FORMAT: str = "wav"       # whisper is fine with wav

# Where temp recordings land before being sent off and deleted
TEMP_AUDIO_DIR: str = os.path.join(os.path.dirname(__file__), "..", "temp")
TEMP_AUDIO_FILE: str = os.path.join(TEMP_AUDIO_DIR, "recording.wav")


# ── Sanity check ─────────────────────────────────────────────────────────────

def validate():
    """
    Makes sure the minimum required config is present before the app starts.
    Right now that's just the OpenAI key — everything else has a default.

    Raises:
        EnvironmentError: if OPENAI_API_KEY is missing from the environment.

    TODO: add more validation as more config is added (e.g. valid hotkey format)
    """
    if not OPENAI_API_KEY:
        raise EnvironmentError(
            "OPENAI_API_KEY is not set. Add it to your .env file or environment."
        )
