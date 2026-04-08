# whisperflow

Hold a key. Talk. Let go. Text appears wherever your cursor is.

whisperflow is a lightweight macOS background app that records your voice while
you hold a hotkey, transcribes it via OpenAI, and pastes the result directly
into whatever app you're currently in — Slack, VS Code, browser, Notes, anything.

No UI. No window. Just a key combo and your voice.

---

## What it does

1. You hold **Right Option (⌥)** — recording starts instantly
2. You speak
3. You release the key — audio ships off to OpenAI's transcription API
4. Transcribed text is pasted at your cursor, wherever it is

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/Yashshah0502/whisperflow.git
cd whisperflow
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your OpenAI API key

```bash
cp .env.example .env
```

Open `.env` and fill in your key:

```
OPENAI_API_KEY=sk-...
```

Get a key at [platform.openai.com/api-keys](https://platform.openai.com/api-keys).

---

## How to run

```bash
source venv/bin/activate
python main.py
```

The app runs in the background. Hold **Right Option (⌥)**, speak, release — done.

To quit, hit `Ctrl+C` in the terminal.

---

## macOS permissions

macOS will block two things on first run. You need to allow both:

**Microphone access**
> System Settings → Privacy & Security → Microphone → enable for Terminal (or your IDE)

**Accessibility access** (needed to simulate Cmd+V)
> System Settings → Privacy & Security → Accessibility → enable for Terminal (or your IDE)

Without Accessibility, the app can record and transcribe but can't paste.

---

## Project structure

```
whisperflow/
├── src/
│   ├── config.py            ← env vars + constants (hotkey, audio settings)
│   ├── hotkey_listener.py   ← global key listener via pynput
│   ├── audio_recorder.py    ← mic recording via sounddevice
│   ├── transcriber.py       ← OpenAI transcription API wrapper
│   └── clipboard_handler.py ← paste via pyperclip + pyautogui
├── temp/                    ← temp audio files (auto-created, gitignored)
├── main.py                  ← entry point
├── requirements.txt
├── .env.example
└── Readme.md
```

---

## Tech stack

| Library | Purpose |
|---|---|
| `openai` | Transcription via gpt-4o-mini-transcribe |
| `pynput` | Global hotkey listener |
| `sounddevice` | Microphone capture |
| `soundfile` | Writing .wav files |
| `numpy` | Audio buffer handling |
| `pyperclip` | Clipboard access |
| `pyautogui` | Simulating Cmd+V |
| `python-dotenv` | .env file loading |

---

## Roadmap

- [x] Phase 1 — project skeleton and module stubs
- [ ] Phase 2 — wire up hotkey → record → transcribe → paste loop
- [ ] Phase 3 — status indicator (menubar icon or sound cue)
- [ ] Phase 4 — configurable hotkey via .env
