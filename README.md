# 🎙️ Vaani — Indian Accent Text-to-Speech Generator

A web app that generates speech in **Indian English** and **Hindi** accents using Google TTS.

---

## ✅ Prerequisites

- Python 3.8 or higher
- Internet connection (gTTS fetches audio from Google servers)

---

## 🚀 Setup & Run (Step-by-Step)

### Step 1 — Download the project files

Place all files in a folder, e.g. `indian-tts/`:

```
indian-tts/
├── app.py
├── requirements.txt
└── templates/
    └── index.html
```

### Step 2 — Open Terminal / Command Prompt

Navigate into the project folder:

```bash
cd indian-tts
```

### Step 3 — Create a virtual environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 4 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 5 — Run the app

```bash
python app.py
```

You'll see:
```
 * Running on http://127.0.0.1:5000
```

### Step 6 — Open in browser

Go to: **http://localhost:5000**

---

## 🎛️ Features

| Feature | Details |
|---|---|
| 🇮🇳 Indian English | Uses Google's `co.in` TLD for authentic Indian accent |
| 🕉️ Hindi | Full Devanagari support |
| ⚡ Playback speed | Adjustable 0.5× to 2× in browser |
| ⬇️ Download | Save MP3 directly from the player |
| 📱 Responsive | Works on mobile and desktop |

---

## 🛠️ Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError` | Make sure venv is activated and you ran `pip install -r requirements.txt` |
| No sound / network error | Check your internet connection (gTTS needs Google access) |
| Port 5000 in use | Change port in `app.py`: `app.run(port=5001)` |
| Hindi text garbled | Make sure your editor/browser supports UTF-8 |

---

## 📦 Tech Stack

- **Flask** — Python web framework
- **gTTS** — Google Text-to-Speech library
- **HTML / CSS / JS** — Vanilla frontend (no frameworks needed)

---

## 🔒 Notes

- gTTS uses Google's TTS API under the hood (free, no API key needed)
- `tld="co.in"` tells Google to serve the Indian regional voice
- All audio is generated on-the-fly and streamed to the browser
