# Architecture & Pipeline Overview

Cali Video Studio provides a modern, modular architecture designed to eliminate external dependencies and cloud credit limitations.

---

## 1. Core Principles

1. **Acoustic Phoneme Lock:** Neural lip animation must derive frame-by-frame coefficients directly from speech audio acoustic frequencies, guaranteeing that mouth shapes close on pauses and match syllables.
2. **Audio-First "Say Anything":** Decoupling speech synthesis from visual generation allows creators to author dialogue without length restrictions, rendering bugs, or model hallucinations.
3. **Reproducibility & Openness:** Zero closed cloud inference APIs. The stack operates on local CPU environments or free GPU runtimes.

---

## 2. Pipeline Stages

```
[ Author Dialogue ]
         │
         ▼
[ Open Neural TTS (Piper / Kokoro) ] ──► Raw WAV
         │
         ▼
[ EBU R128 Loudness Normalization ]  ──► -16 LUFS Mastered WAV
         │
         ▼
[ Neural Talking-Head (SadTalker) ]  ──► Clean Avatar Photo + Mastered WAV
         │
         ▼
[ Frame-Accurate Video Clip ]
         │
         ▼
[ Compositing Engine ]               ──► Scene Cards + Lower Thirds + Bumper
         │
         ▼
[ Master MP4 Video ]
```

---

## 3. Recommended Hardware Configurations

* **Fast Local CPU (Procedural 2D Rigging):** 4+ cores, 8GB RAM.
* **Neural Lip-Sync Inference:** NVIDIA GPU (e.g. T4 / RTX 3060+) or Google Colab T4 GPU (free).
