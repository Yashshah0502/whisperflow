"""
clipboard_handler.py — puts text where the user's cursor is.

Two-step: copy to clipboard with pyperclip, then fire Cmd+V with pyautogui.
Works in any app that accepts paste — Slack, VS Code, browser, Notes, etc.

Requires Accessibility permissions on macOS. Without them pyautogui can't send
key events. The OS will prompt on first run — just click Allow.
"""

import time
import pyperclip
import pyautogui


# Silence pyautogui's "move mouse to corner to abort" failsafe — it's annoying
# in a background app. Remove this line if you want the safety net back.
pyautogui.FAILSAFE = False


def paste_text(text: str):
    """
    Copies text to the system clipboard then simulates Cmd+V to paste it.

    The 0.1s delay between copy and paste is intentional — without it, macOS
    occasionally pastes the previous clipboard content because the OS hasn't
    finished registering the new value yet.

    Args:
        text: the transcribed string to paste. Does nothing if empty.
    """
    if not text or not text.strip():
        print("[clipboard] Nothing to paste — transcription was empty.")
        return

    try:
        pyperclip.copy(text)
        time.sleep(0.1)  # let the OS catch up before we fire the shortcut
        pyautogui.hotkey("command", "v")
        print(f"[clipboard] Pasted: \"{text}\"")
    except pyautogui.FailSafeException:
        # Mouse was in the top-left corner — shouldn't happen with FAILSAFE=False
        # but just in case someone re-enables it
        print("[clipboard] Paste aborted (pyautogui failsafe triggered).")
    except Exception as e:
        print(
            f"[clipboard] Paste failed: {e}\n"
            "  → Check System Settings → Privacy & Security → Accessibility\n"
            "     and make sure Terminal (or your IDE) has permission."
        )
