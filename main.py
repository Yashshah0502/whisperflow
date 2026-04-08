"""
main.py — entry point for whisperflow.
Run it: python main.py
Stop it: Ctrl+C or Quit from the menu bar icon
"""

import sys
import threading
import rumps
from src import config
from src.menu_bar import WhisperFlowApp
from src import hotkey_listener

def main():
 try:
  config.validate()
 except EnvironmentError as e:
  rumps.alert(title="Missing API Key", message=str(e))
  sys.exit(1)

 app = WhisperFlowApp()

 # Hotkey listener runs in a background thread — rumps owns the main thread
 t = threading.Thread(target=hotkey_listener.start_listener, args=(app,), daemon=True)
 t.start()

 print(f"WhisperFlow running | Hotkey: {config.HOTKEY} | Model: {config.MODEL}")
 print("Hold the hotkey to record. Release to transcribe and paste.")
 print("Quit from the 🎙 menu bar icon or press Ctrl+C.\n")

 # This blocks until the user quits from the menu bar
 app.run()

if __name__ == "__main__":
 main()