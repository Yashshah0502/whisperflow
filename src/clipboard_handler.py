"""
clipboard_handler.py — puts text where the user's cursor is.

Two-step approach: copy the transcribed text to the system clipboard with
pyperclip, then simulate Cmd+V with pyautogui to paste it into whatever app
currently has focus. Works in any app that accepts paste — Slack, browser,
VS Code, Terminal, Notes, you name it.

Note: requires Accessibility permissions on macOS. Without them, pyautogui
can see the screen but can't send key events. The app will prompt on first run.
"""

import time
import pyperclip
import pyautogui


def paste_text(text: str):
    """
    Copies text to the clipboard then pastes it at the current cursor position.

    There's a small intentional delay between copy and paste to give the OS
    time to register the clipboard change before we fire the keyboard shortcut.
    Without it, the paste occasionally picks up the previous clipboard content.

    Args:
        text (str): the transcribed text to paste. If empty, does nothing.

    Returns:
        None

    TODO: guard against empty/whitespace-only text — return early if so
    TODO: pyperclip.copy(text)
    TODO: time.sleep(0.1) — give the clipboard time to settle
    TODO: pyautogui.hotkey("command", "v")  ← macOS paste shortcut
    TODO: optionally restore the previous clipboard content after pasting
    TODO: handle pyautogui.FailSafeException if mouse is in the corner
    """
    pass
