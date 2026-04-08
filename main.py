"""
main.py — entry point for whisperflow.

Run it: python main.py
Stop it: Ctrl+C
"""

import sys
import time
from src import config
from src import hotkey_listener

def main():
    # Validate config before touching the mic or keyboard
    try:
        config.validate()
    except EnvironmentError as e:
        print(e)
        sys.exit(1)

    print(f"WhisperFlow running | Hotkey: {config.HOTKEY} | Model: {config.MODEL}")
    print("Hold the hotkey to record. Release to transcribe and paste.")
    print("Press Ctrl+C to quit.\n")

    hotkey_listener.start_listener()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        hotkey_listener.stop_listener()
        print("\nWhisperFlow stopped.")


if __name__ == "__main__":
    main()
