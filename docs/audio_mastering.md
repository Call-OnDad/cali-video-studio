# EBU R128 Audio Loudness Mastering

Consistent audio loudness is crucial for broadcast quality and viewer retention.

---

## 1. Loudness Standards Explained

* **Integrated Loudness (`I`):** The average loudness across the entire duration. Our studio standard is `-16.0 LUFS` (optimal for dialogue-focused mobile and desktop viewing).
* **True Peak (`TP`):** Peak acoustic level. Limited to `-1.5 dBTP` to prevent inter-sample clipping during codec compression (AAC/Opus).
* **Loudness Range (`LRA`):** Dynamic range span. Standardized to `11.0 LU` to keep quiet speech intelligible without loud shouting spikes.

---

## 2. CLI Execution

Use the included `audio_master.py` utility:

```bash
# Normalize dialogue track
python tools/audio_master.py -i raw_voice.wav -o mastered_voice.wav --target-lufs -16.0

# Mix with background music (auto-ducking speech)
python tools/audio_master.py -i raw_voice.wav -o final_mix.wav --music background_bed.wav --music-gain -21.0
```
