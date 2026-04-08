"""
main.py — entry point for whisperflow.

Run this directly: python main.py
Keep it alive with: python main.py (it blocks on the hotkey listener)

Right now it's just bootstrapping — actual listen/record/transcribe loop
gets wired up in Phase 2.
"""

import sys

# Pull in all the modules to make sure nothing's broken at import time
from src import config
from src.hotkey_listener import start_listener, stop_listener
from src.audio_recorder import start_recording, stop_recording, save_audio
from src.transcriber import transcribe
from src.clipboard_handler import paste_text


def main():
    # Make sure the .env is loaded and OPENAI_API_KEY is present
    # before we get anywhere near the mic or hotkeys
    try:
        config.validate()
    except EnvironmentError as e:
        print(f"[config error] {e}")
        sys.exit(1)

    print("App initialized successfully")

    # TODO (Phase 2): start the hotkey listener here
    # TODO (Phase 2): wire up on_press → start_recording, on_release → stop + transcribe + paste
    # TODO (Phase 2): block on listener.join() so the process stays alive


if __name__ == "__main__":
    main()
