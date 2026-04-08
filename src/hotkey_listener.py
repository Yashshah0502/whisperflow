"""
hotkey_listener.py — watches for the magic key combo.

Uses pynput to listen globally across all apps. When the user holds the hotkey,
recording starts. When they release it, recording stops and transcription kicks off.
This runs in its own thread so it doesn't block the main process.
"""

from pynput import keyboard


# The listener instance — kept here so stop_listener() can reach it
_listener = None


def start_listener(on_press_callback, on_release_callback):
    """
    Starts a global keyboard listener in the background.

    Calls on_press_callback when the configured hotkey is pressed, and
    on_release_callback when it's released. Both callbacks receive no arguments —
    the hotkey matching is handled internally.

    Args:
        on_press_callback (callable):   fired when the hotkey goes down
        on_release_callback (callable): fired when the hotkey comes up

    Returns:
        None

    TODO: read the target hotkey from config.HOTKEY
    TODO: parse the hotkey string into a pynput Key or KeyCode
    TODO: create a pynput.keyboard.Listener and start it in a daemon thread
    TODO: store the listener in _listener so stop_listener() can kill it later
    TODO: handle the case where another app has grabbed the key (rare but possible)
    """
    pass


def stop_listener():
    """
    Stops the global keyboard listener cleanly.

    Safe to call even if the listener was never started — just a no-op.

    TODO: check if _listener is not None
    TODO: call _listener.stop()
    TODO: set _listener back to None
    """
    pass
