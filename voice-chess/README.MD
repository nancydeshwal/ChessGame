# ♟️ Voice-Controlled Explainable Chess AI

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/Deployed-Live-00C853?style=for-the-badge&logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/XAI-Enabled-blueviolet?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Voice-Controlled-orange?style=for-the-badge&logo=google&logoColor=white"/>
</p>

<p align="center">
  <b>🎙️ Speak your move. ♟️ Watch the AI think. 🧠 Understand why.</b><br/>
  A fully voice-driven chess system powered by Minimax search, Alpha-Beta pruning and human-readable XAI explanations.
</p>

<p align="center">
  <a href="https://voice-chess-xai-8lyqt26kzcyatpuxhrkm68.streamlit.app/" target="_blank">
    <img src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg" alt="Open in Streamlit"/>
  </a>
</p>

---

## 🌐 Live Demo

> **[🚀 Open App → voice-chess-xai-8lyqt26kzcyatpuxhrkm68.streamlit.app](https://voice-chess-xai-8lyqt26kzcyatpuxhrkm68.streamlit.app/)**

---

## 📌 Overview

**Voice Chess XAI** is an intelligent, accessible chess system that lets you play chess entirely through voice commands — no mouse or keyboard needed. After every AI move, the system generates a **plain-English explanation** of *why* that move was chosen, covering threat analysis, positional advantages, piece safety, and alternative comparisons.

This project sits at the intersection of:
- 🎙️ **Speech Recognition** — browser-native audio input to SpeechRecognition
- ♟️ **AI Search** — Minimax with Alpha-Beta pruning + neural network board evaluation
- 🧠 **Explainable AI (XAI)** — human-readable move justifications after every decision
- 🖥️ **Interactive UI** — real-time Streamlit chess board with full game logging

---

## ✨ Features

| Feature | Description |
|---|---|
| 🎙️ **Voice Input** | Speak moves naturally — e.g. *"move knight to F3"* — captured via `st.audio_input` |
| ♟️ **AI Engine** | Minimax + Alpha-Beta pruning with configurable search depth |
| 💡 **XAI Explanations** | Post-move reasoning covering checks, captures, development, and positional control |
| 📋 **Game Log** | Full move-by-move history with AI rationale recorded in real time |
| 🖥️ **Interactive Board** | Visual chess board rendered directly in Streamlit |
| 🔊 **Speech Feedback** | Audio confirmation of recognized moves and AI responses |
| ☁️ **Cloud Deployed** | Fully live on Streamlit Community Cloud — no local setup needed |

---

## 🏗️ Project Architecture

```
voice-chess-xai/
│
├── app.py           # Streamlit UI — board rendering, game flow, session state
├── engine.py        # AI engine — Minimax, Alpha-Beta pruning, move generation
├── explain.py       # XAI module — human-readable move explanation generation
├── voice.py         # Voice module — audio capture, speech-to-text, move parsing
└── requirements.txt # All dependencies
```

### Module Breakdown

**`app.py`** — Orchestrates the full application. Handles board visualization, player/AI turn management, voice input triggering, and XAI log display via Streamlit components.

**`engine.py`** — The AI brain. Implements Minimax with Alpha-Beta pruning for efficient tree search. Supports optional neural network evaluation for more accurate board scoring beyond traditional piece-value heuristics.

**`explain.py`** — The transparency layer. After each AI move, generates a structured natural language explanation including threat detection, positional improvement score, captures, checks, and development reasoning.

**`voice.py`** — The voice pipeline. Captures microphone audio via `st.audio_input`, passes it through `SpeechRecognition`, and maps spoken natural language (e.g. *"bishop to C5"*) to valid UCI/SAN chess notation.

---

## 🎯 Core Objectives

1. **Voice-First Accessibility** — Play chess hands-free through accurate real-time speech-to-move conversion.
2. **Strong AI with Search Optimization** — Minimax + Alpha-Beta pruning ensures efficient, high-quality move computation at configurable depths.
3. **Explainability by Design** — Every AI move comes with a transparent, human-readable justification — not just a move, but a *reason*.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend / UI | Streamlit |
| Language | Python 3.10+ |
| Voice Recognition | `SpeechRecognition`, `st.audio_input` |
| Chess Logic | `python-chess` |
| AI Search | Minimax + Alpha-Beta Pruning |
| Board Evaluation | Heuristic + Optional Neural Network |
| XAI | Custom rule-based explanation engine (`explain.py`) |
| Deployment | Streamlit Community Cloud |

---

## 🚀 Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/sonikadeshwal/voice-chess-xai.git
cd voice-chess-xai

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the app
streamlit run app.py
```

> The app will open at `http://localhost:8501`. Allow microphone access when prompted.

---

## 🎙️ How to Play

1. Open the live app or run locally.
2. It's your turn — click the **🎙️ Speak Move** button.
3. Say your move aloud — e.g. *"pawn to E4"*, *"knight to F3"*, *"castle kingside"*.
4. The system recognizes your speech, validates the move, and updates the board.
5. The AI computes its response and plays its move.
6. Read the **XAI explanation** below the board to understand the AI's reasoning.
7. Continue until checkmate, draw, or resignation.

---

## 💡 What Makes It Different

Most chess engines are opaque — they play strong moves but give you nothing. This system adds a **transparency layer** directly into the gameplay loop:

```
AI selects move
      ↓
explain.py analyzes:
  - Was a piece captured?
  - Is this a check or checkmate threat?
  - Does it improve center control or piece activity?
  - What alternatives were considered?
      ↓
Human-readable explanation shown instantly
```

This makes the project relevant not just as a chess tool, but as a demonstration of **Explainable AI principles** applied to a real-time game system.

---

## 📈 Future Enhancements

- [ ] Full neural network integration (trained on large chess databases)
- [ ] Multilingual voice support
- [ ] ELO difficulty selector (Beginner / Intermediate / Expert)
- [ ] Game export (PGN format)
- [ ] Mobile-optimized UI

---







