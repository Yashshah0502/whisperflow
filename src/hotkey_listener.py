"""
hotkey_listener.py — watches for the magic key combo and runs the full pipeline.

Uses pynput to listen globally across all apps. Tracks which modifier keys are
currently held so we can detect the full combo (ctrl+shift+space) on press and
trigger the transcription pipeline on release.

The record → save → transcribe → paste flow runs in a background thread so the
keyboard listener stays responsive while OpenAI is thinking.
"""

import threading
from pynput import keyboard
from src import config
from src import audio_recorder, transcriber, clipboard_handler, notifier


# ── Internal state ────────────────────────────────────────────────────────────

_listener: keyboard.Listener | None = None

# The menu bar app — set by start_listener() so we can update status icons
_app = None

# Keys currently held down
_pressed: set = set()

# Guards against starting a new recording while one is already in flight
_is_recording: bool = False
_lock = threading.Lock()

# ── Key matching helpers ──────────────────────────────────────────────────────

def _is_ctrl(key) -> bool:
    return key in (keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r)


def _is_shift(key) -> bool:
    return key in (keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r)


def _is_space(key) -> bool:
    return key == keyboard.Key.space or (
        hasattr(key, "char") and key.char == " "
    )


def _combo_active() -> bool:
    return (
        any(_is_ctrl(k) for k in _pressed)
        and any(_is_shift(k) for k in _pressed)
        and any(_is_space(k) for k in _pressed)
    )


# ── Pipeline (runs in a background thread on release) ────────────────────────

def _run_pipeline():
    global _app

    try:
        audio_data = audio_recorder.stop_recording()

        if audio_data is None or len(audio_data) == 0:
            print("[whisperflow] Recording too short — nothing to transcribe.")
            if _app:
                _app.set_status_idle()
            return

        if _app:
            _app.set_status_transcribing()

        audio_path = audio_recorder.save_audio(audio_data)
        text = transcriber.transcribe(audio_path)

        if text:
            clipboard_handler.paste_text(text)
        else:
            notifier.notify("WhisperFlow", "Transcription came back empty.")

        print("[whisperflow] Done.\n")

    except RuntimeError as e:
        print(e)
        notifier.notify("WhisperFlow", "Transcription failed. Check terminal.")

    except Exception as e:
        print(f"[whisperflow] Unexpected error: {e}")
        notifier.notify("WhisperFlow", "Something went wrong. Check terminal.")

    finally:
        if _app:
            _app.set_status_idle()


# ── pynput callbacks ──────────────────────────────────────────────────────────

def _on_press(key):
    global _is_recording

    _pressed.add(key)

    with _lock:
        if _combo_active() and not _is_recording:
            _is_recording = True
            if _app:
                _app.set_status_recording()
            print("\n[whisperflow] Recording... (release ctrl+shift+space to stop)")
            try:
                audio_recorder.start_recording()
            except RuntimeError as e:
                print(e)
                notifier.notify(
                    "WhisperFlow",
                    "Mic access denied. Check System Settings → Privacy → Microphone",
                )
                _is_recording = False
                if _app:
                    _app.set_status_idle()


def _on_release(key):
    global _is_recording

    was_full_combo = _combo_active()
    _pressed.discard(key)

    with _lock:
        if was_full_combo and _is_recording:
            _is_recording = False
            threading.Thread(target=_run_pipeline, daemon=True).start()


# ── Public API ────────────────────────────────────────────────────────────────

def start_listener(app=None):
    """
    Starts the global keyboard listener in a background daemon thread.

    Args:
        app: optional WhisperFlowApp instance — if provided, its status
             items are updated as the pipeline moves through each stage.
    """
    global _listener, _app
    _app = app

    print(f"[whisperflow] Listening for hotkey: {config.HOTKEY}")

    _listener = keyboard.Listener(on_press=_on_press, on_release=_on_release)
    _listener.daemon = True
    _listener.start()


def stop_listener():
    """Stops the keyboard listener cleanly. Safe to call if never started."""
    global _listener

    if _listener is not None:
        _listener.stop()
        _listener = None
