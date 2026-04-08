# whisperflow

Hold a key. Talk. Let go. Text appears wherever your cursor is.

whisperflow is a lightweight macOS background app that records your voice while
you hold a hotkey, transcribes it via OpenAI, and pastes the result directly
into whatever app you're currently in — Slack, VS Code, browser, Notes, anything.

Lives in your menu bar as 🎙. No window, no UI, just a key combo and your voice.

---

## What it does

1. You hold **Ctrl+Shift+Space** — recording starts, menu bar shows 🔴
2. You speak
3. You release — text ships to OpenAI, menu bar shows ⚡
4. Transcribed text is pasted at your cursor, macOS notification pops up ✅

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

The 🎙 icon appears in your menu bar. Hold **Ctrl+Shift+Space**, speak, release — done.

To quit: click 🎙 → Quit, or press `Ctrl+C` in the terminal.

---

## Configuration

On first run, whisperflow creates **`whisperflow.json`** in the project root:

```json
{
  "hotkey": "ctrl+shift+space",
  "model": "gpt-4o-mini-transcribe",
  "samplerate": 44100,
  "channels": 1,
  "language": null
}
```

Edit this file to change settings. You can also open it from the menu bar: 🎙 → **Open Config File**.

| Key | Default | Description |
|---|---|---|
| `hotkey` | `ctrl+shift+space` | Key combo that triggers recording |
| `model` | `gpt-4o-mini-transcribe` | OpenAI transcription model |
| `samplerate` | `44100` | Mic sample rate (Hz) |
| `channels` | `1` | Audio channels (1 = mono) |
| `language` | `null` | ISO-639-1 code (`"en"`, `"hi"`, `"gu"`) or `null` for auto-detect |

---

## macOS permissions

macOS will ask for two permissions on first run. Both are required:

**Microphone**
> System Settings → Privacy & Security → Microphone → enable for Terminal (or your IDE)

**Accessibility** (needed to simulate Cmd+V)
> System Settings → Privacy & Security → Accessibility → enable for Terminal (or your IDE)

whisperflow will show a native notification if either permission is missing.

---

## Project structure

```
whisperflow/
├── src/
│   ├── config.py            ← loads .env + whisperflow.json, exposes all constants
│   ├── config_manager.py    ← reads/writes whisperflow.json
│   ├── hotkey_listener.py   ← global key listener, orchestrates the pipeline
│   ├── audio_recorder.py    ← mic recording via sounddevice
│   ├── transcriber.py       ← OpenAI transcription API wrapper
│   ├── clipboard_handler.py ← paste via pyperclip + pyautogui
│   ├── menu_bar.py          ← rumps menu bar app (🎙 icon + status)
│   └── notifier.py          ← native macOS notifications via rumps
├── temp/                    ← temp audio files (auto-created, gitignored)
├── main.py                  ← entry point
├── whisperflow.json         ← user config (auto-created on first run)
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
| `rumps` | macOS menu bar app + native notifications |
| `python-dotenv` | .env file loading |

---

## Roadmap

- [x] Phase 1 — project skeleton and module stubs
- [x] Phase 2 — hotkey → record → transcribe → paste
- [x] Phase 3 — menu bar icon, native notifications, JSON config, language support
- [ ] Phase 4 — custom icon, launch at login, recording sound cue
