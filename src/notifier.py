"""
notifier.py — native macOS notifications via rumps.

One function, one job: pop a notification. Everything else stays out of here.
Requires the rumps app to be running (it always is when whisperflow is up).
"""

import rumps


def notify(title: str, message: str):
    """
    Sends a native macOS notification.

    Args:
        title:   bold top line (usually "WhisperFlow")
        message: the body text
    """
    try:
        rumps.notification(title=title, subtitle="", message=message)
    except Exception:
        # Notifications are best-effort — never let them crash the pipeline
        pass
