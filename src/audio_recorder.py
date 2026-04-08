"""
audio_recorder.py — handles mic input from start to file.

Uses sounddevice to stream audio from the default microphone into a numpy buffer.
A threading.Event controls the recording lifecycle — set to stop, clear to record.
When recording stops the buffer gets written to a temp .wav file via soundfile.
"""

import os
import threading
import numpy as np
import sounddevice as sd
import soundfile as sf
from src import config

# Audio chunks accumulate here while recording is in flight
_audio_buffer: list = []

# Stops the InputStream callback from accepting new frames
_stop_event = threading.Event()

# The active sounddevice stream — kept so stop_recording() can close it
_stream: sd.InputStream | None = None

def start_recording():
    """
    Opens the microphone and starts buffering audio in the background.

    Clears any leftover data from a previous recording, opens a sounddevice
    InputStream, and starts accumulating frames. Returns immediately — the
    stream runs in its own thread until stop_recording() is called.

    Raises:
        RuntimeError: if the mic can't be opened (no device, permissions denied)
    """
    global _audio_buffer, _stream

    _audio_buffer = []
    _stop_event.clear()

    def _callback(indata, frames, time_info, status):
        # status carries things like input overflow — not fatal, just log it
        if status:
            print(f"[audio] {status}")
        if not _stop_event.is_set():
            _audio_buffer.append(indata.copy())

    try:
        _stream = sd.InputStream(
            samplerate=config.AUDIO_SAMPLERATE,
            channels=config.AUDIO_CHANNELS,
            dtype="float32",
            callback=_callback,
        )
        _stream.start()
    except sd.PortAudioError as e:
        raise RuntimeError(
            f"[audio] Couldn't open microphone: {e}\n"
            "  → Check System Settings → Privacy & Security → Microphone\n"
            "     and make sure Terminal (or your IDE) is allowed."
        )


def stop_recording() -> np.ndarray:
    """
    Stops the microphone stream and returns the captured audio as a numpy array.

    The buffer is left intact after this call — save_audio() can read it.
    Returns an empty array if nothing was recorded (e.g. tap instead of hold).
    """
    global _stream

    _stop_event.set()

    if _stream is not None:
        _stream.stop()
        _stream.close()
        _stream = None

    if not _audio_buffer:
        return np.array([], dtype="float32")

    audio_data = np.concatenate(_audio_buffer, axis=0)
    duration = len(audio_data) / config.AUDIO_SAMPLERATE
    print(f"[audio] Captured {duration:.1f}s of audio.")
    return audio_data


def save_audio(audio_data: np.ndarray) -> str:
    """
    Writes a numpy audio array to the temp .wav file defined in config.

    The file is overwritten on every call so there's only ever one temp file
    on disk. The directory is created if it doesn't exist yet.

    Args:
        audio_data: float32 numpy array from stop_recording()

    Returns:
        Absolute path to the saved .wav file.

    Raises:
        RuntimeError: if audio_data is empty (nothing to save)
    """
    if audio_data is None or len(audio_data) == 0:
        raise RuntimeError(
            "[audio] Nothing to save — recording was empty.\n"
            "  → Hold the hotkey a bit longer next time."
        )

    os.makedirs(os.path.dirname(config.TEMP_AUDIO_PATH), exist_ok=True)
    sf.write(config.TEMP_AUDIO_PATH, audio_data, config.AUDIO_SAMPLERATE)
    print(f"[audio] Saved to {config.TEMP_AUDIO_PATH}")
    return config.TEMP_AUDIO_PATH
