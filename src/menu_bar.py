"""
menu_bar.py — the 🎙 icon that lives in the macOS menu bar.

Built on rumps (a Pythonic wrapper around AppKit). This class IS the app —
main.py calls WhisperFlowApp().run() which hands control to the macOS event
loop and keeps the process alive.

Status updates are called from the hotkey listener's background thread.
rumps MenuItem title assignments are thread-safe on macOS in practice
(NSString assignments are atomic), so no explicit locking is needed here.
"""

import os
import rumps

from src import config
from src import config_manager


class WhisperFlowApp(rumps.App):

    def __init__(self):
        # quit_button=None so we control the Quit item ourselves
        super().__init__("🎙", quit_button=None)

        # ── Dynamic items we need to update later ────────────────────────────
        self.status_item = rumps.MenuItem("Status: ✅ Idle")
        self.hotkey_item = rumps.MenuItem(f"Hotkey: {config.HOTKEY}")

        # ── Build the menu ────────────────────────────────────────────────────
        self.menu = [
            rumps.MenuItem("WhisperFlow"),
            None,  # ── separator ──
            self.status_item,
            self.hotkey_item,
            None,
            rumps.MenuItem("Open Config File", callback=self._open_config),
            None,
            rumps.MenuItem("Quit", callback=self._quit),
        ]

    # ── Status helpers (called from hotkey_listener's background thread) ──────

    def set_status_recording(self):
        self.status_item.title = "Status: 🔴 Recording..."

    def set_status_transcribing(self):
        self.status_item.title = "Status: ⚡ Transcribing..."

    def set_status_idle(self):
        self.status_item.title = "Status: ✅ Idle"

    # ── Menu callbacks ────────────────────────────────────────────────────────

    def _open_config(self, _):
        """Opens whisperflow.json in the default editor."""
        # Make sure the file exists before trying to open it
        config_manager.load_config()
        os.system(f"open '{config_manager.CONFIG_PATH}'")

    def _quit(self, _):
        rumps.quit_application()
