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

    Passes config.LANGUAGE to the API if set — otherwise OpenAI auto-detects.
    Set "language" in whisperflow.json to an ISO-639-1 code (e.g. "en", "hi",
    "gu") to force a specific language and slightly improve accuracy.

    Args:
        audio_path: path to the .wav file produced by audio_recorder.save_audio()

    Returns:
        Transcribed text, stripped of whitespace. Empty string if API returns nothing.

    Raises:
        FileNotFoundError: if audio_path doesn't exist on disk
        RuntimeError:      on API or network errors
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(
            f"[transcriber] Audio file not found: {audio_path}"
        )

    lang_note = f" (language: {config.LANGUAGE})" if config.LANGUAGE else ""
    print(f"[transcriber] Sending to OpenAI{lang_note}...")

    try:
        with open(audio_path, "rb") as audio_file:
            kwargs: dict = {
                "model": config.MODEL,
                "file": audio_file,
                "response_format": "text",
            }
            if config.LANGUAGE:
                kwargs["language"] = config.LANGUAGE

            response = _get_client().audio.transcriptions.create(**kwargs)

    except APIError as e:
        raise RuntimeError(
            f"[transcriber] OpenAI API error: {e}\n"
            "  → Check your OPENAI_API_KEY and internet connection."
        )

    text = response if isinstance(response, str) else response.text
    result = text.strip() if text else ""

    if result:
        print(f"[transcriber] Got: \"{result}\"")
    else:
        print("[transcriber] Got empty response from API.")

    return result
