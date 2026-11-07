# Open-Source Voice Synthesis Guide

Cali Video Studio is designed to integrate with high-performance, open-source neural TTS systems that run locally without recurring subscription fees.

---

## 1. Piper TTS

Piper is an ultra-fast, local neural text-to-speech engine optimized for CPU and edge devices:
* **Models:** High-quality VITS onnx models (e.g. `en_GB-jenny_dioco-medium.onnx`, `en_GB-northern_english_male-medium.onnx`).
* **Performance:** Real-time factor (RTF) > 5x on standard multi-core CPUs.
* **Usage:**
  ```bash
  echo "Welcome to Cali Video Studio." | piper --model en_GB-jenny_dioco-medium.onnx --output_file speech.wav
  ```

---

## 2. Kokoro ONNX

Kokoro is an open-source 82M-parameter TTS model that generates remarkably natural English speech:
* **Quality:** Authentic inflection, smooth breathing, and realistic pacing.
* **Format:** Single ONNX model running via `kokoro-onnx` on CPU or GPU.
* **Target Loudness:** Must be passed to `audio_master.py` to achieve `-16 LUFS`.
