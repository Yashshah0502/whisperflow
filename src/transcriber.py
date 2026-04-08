"""
transcriber.py — sends audio to OpenAI and gets text back.

Thin wrapper around the OpenAI audio transcription API. Takes a path to a .wav
file and returns the transcribed string. That's it — no pre-processing, no
post-processing, just audio in, text out.
"""

from openai import OpenAI

from src import config


# Reuse a single client for the whole session — no point recreating it each call
_client: OpenAI | None = None


def _get_client() -> OpenAI:
    """
    Returns the shared OpenAI client, creating it on first call.

    TODO: initialise _client with config.OPENAI_API_KEY if it's None
    TODO: return _client
    """
    pass


def transcribe(audio_path: str) -> str:
    """
    Transcribes a .wav file using the OpenAI transcription API.

    Opens the audio file, ships it off to OpenAI's transcription endpoint,
    and returns the plain text result. The temp file is NOT deleted here —
    cleanup is the caller's responsibility (or just let the next recording
    overwrite it).

    Args:
        audio_path (str): path to the .wav file to transcribe

    Returns:
        str: the transcribed text, stripped of leading/trailing whitespace.
             Returns an empty string if the API gives back nothing.

    Raises:
        FileNotFoundError: if audio_path doesn't exist
        openai.APIError:   if the API call fails (network issue, bad key, etc.)

    TODO: validate that audio_path exists — raise FileNotFoundError if not
    TODO: open the file in binary mode
    TODO: call client.audio.transcriptions.create() with config.TRANSCRIPTION_MODEL
    TODO: return response.text.strip()
    TODO: add basic retry logic for transient network errors (optional, phase 2)
    """
    pass
