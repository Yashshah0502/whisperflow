"""
hotkey_listener.py — watches for the magic key combo and runs the full pipeline.

Uses pynput to listen globally across all apps. Tracks which modifier keys are
currently held so we can detect the full combo (ctrl+shift+space) on press and
trigger the transcription pipeline on release.

The record → save → transcribe → paste flow runs in a background thread so it
doesn't block the keyboard listener while OpenAI is thinking.
"""

import threading
from pynput import keyboard
from src import config
from src import audio_recorder, transcriber, clipboard_handler


# ── Internal state ────────────────────────────────────────────────────────────

_listener: keyboard.Listener | None = None

# Keys currently held down — used to detect when the full combo is active
_pressed: set = set()

# Prevents starting a new recording while one is already in flight
_is_recording: bool = False

# Serialises access to _is_recording across the listener thread and the
# background pipeline thread
_lock = threading.Lock()


# ── Key matching helpers ──────────────────────────────────────────────────────

def _is_ctrl(key) -> bool:
    return key in (keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r)


def _is_shift(key) -> bool:
    return key in (keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r)


def _is_space(key) -> bool:
    # pynput can give us Key.space or a KeyCode with char=' ' depending on the OS
    return key == keyboard.Key.space or (
        hasattr(key, "char") and key.char == " "
    )


def _combo_active() -> bool:
    """Returns True if ctrl+shift+space are all currently held."""
    return (
        any(_is_ctrl(k) for k in _pressed)
        and any(_is_shift(k) for k in _pressed)
        and any(_is_space(k) for k in _pressed)
    )


# ── Pipeline ──────────────────────────────────────────────────────────────────

def _run_pipeline():
    """
    Runs the stop → save → transcribe → paste pipeline in a background thread.
    Fires once the hotkey combo is released.
    """
    try:
        audio_data = audio_recorder.stop_recording()

        if audio_data is None or len(audio_data) == 0:
            print("[whisperflow] Recording too short — nothing to transcribe.")
            return

        audio_path = audio_recorder.save_audio(audio_data)
        text = transcriber.transcribe(audio_path)

        if text:
            clipboard_handler.paste_text(text)

        print("[whisperflow] Done.\n")

    except RuntimeError as e:
        print(e)
    except Exception as e:
        print(f"[whisperflow] Unexpected error: {e}")


# ── pynput callbacks ──────────────────────────────────────────────────────────

def _on_press(key):
    global _is_recording

    _pressed.add(key)

    with _lock:
        if _combo_active() and not _is_recording:
            _is_recording = True
            print("\n[whisperflow] Recording... (release ctrl+shift+space to stop)")
            try:
                audio_recorder.start_recording()
            except RuntimeError as e:
                print(e)
                _is_recording = False


def _on_release(key):
    global _is_recording

    was_full_combo = _combo_active()
    _pressed.discard(key)

    with _lock:
        if was_full_combo and _is_recording:
            _is_recording = False
            # Run the pipeline off the listener thread so key events keep flowing
            threading.Thread(target=_run_pipeline, daemon=True).start()


# ── Public API ────────────────────────────────────────────────────────────────

def start_listener():
    """
    Starts the global keyboard listener in a background daemon thread.

    The listener watches every key event system-wide and fires the recording
    pipeline whenever the configured hotkey combo is held and released.

    Requires Accessibility permissions on macOS — the OS will prompt on first run.
    """
    global _listener

    print(f"[whisperflow] Listening for hotkey: {config.HOTKEY}")

    _listener = keyboard.Listener(on_press=_on_press, on_release=_on_release)
    _listener.daemon = True
    _listener.start()


def stop_listener():
    """
    Stops the global keyboard listener cleanly. Safe to call even if it was
    never started.
    """
    global _listener

    if _listener is not None:
        _listener.stop()
        _listener = None
