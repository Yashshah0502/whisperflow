"""
transcriber.py — sends audio to OpenAI and gets text back.

Thin wrapper around the OpenAI audio transcription API. Takes a path to a .wav
file and returns the transcribed string. Audio in, text out — nothing else.
"""

import os
from openai import OpenAI, APIError

from src import config


# Single client instance reused for the whole session
_client: OpenAI | None = None


def _get_client() -> OpenAI:
    """Returns the shared OpenAI client, creating it on the first call."""
    global _client
    if _client is None:
        _client = OpenAI(api_key=config.OPENAI_API_KEY)
    return _client


def transcribe(audio_path: str) -> str:
    """
    Transcribes a .wav file using the OpenAI transcription API.

    Opens the file, ships it to the API, and returns the plain text result.
    The temp file is NOT deleted here — it gets overwritten on the next recording.

    Args:
        audio_path: path to the .wav file produced by audio_recorder.save_audio()

    Returns:
        Transcribed text, stripped of leading/trailing whitespace.
        Empty string if the API returns nothing useful.

    Raises:
        FileNotFoundError: if audio_path doesn't exist on disk
        RuntimeError:      on API or network errors (with a human-readable message)
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(
            f"[transcriber] Audio file not found: {audio_path}"
        )

    print("[transcriber] Sending to OpenAI...")

    try:
        with open(audio_path, "rb") as audio_file:
            response = _get_client().audio.transcriptions.create(
                model=config.MODEL,
                file=audio_file,
                response_format="text",
            )
    except APIError as e:
        raise RuntimeError(
            f"[transcriber] OpenAI API error: {e}\n"
            "  → Check your OPENAI_API_KEY and internet connection."
        )

    # response_format="text" returns a plain string directly
    text = response if isinstance(response, str) else response.text
    result = text.strip() if text else ""

    if result:
        print(f"[transcriber] Got: \"{result}\"")
    else:
        print("[transcriber] Got empty response from API.")

    return result
