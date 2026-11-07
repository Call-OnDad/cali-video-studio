# Cali Video Studio: Standalone Native Modules 🧩

Each module in this directory can be run **completely independently** without installing or running the entire monolithic suite. They serve as lightweight tools for specific tasks and robust, zero-dependency fallbacks if your local server or homelab equipment is ever offline.

---

## 📦 The 5 Standalone Modules

| Module Directory | Standalone Program | Description | 1-Click Launcher |
| :--- | :--- | :--- | :--- |
| **[`01-voice-studio/`](01-voice-studio/)** | `voice_studio.py` | Offline neural TTS (Piper/Kokoro) + EBU R128 (`-16 LUFS`) loudness mastering | `Launch-Voice-Studio.cmd` |
| **[`02-lipsync-animator/`](02-lipsync-animator/)** | `lipsync_runner.py` | Direct audio-driven neural talking-head animation (SadTalker / MuseTalk) | `Launch-LipSync.cmd` |
| **[`03-card-studio/`](03-card-studio/)** | `card_studio.py` | 9:16 vertical presentation cards with contain scaling (no head/feet cropping) | `Launch-Card-Studio.cmd` |
| **[`04-video-nle/`](04-video-nle/)** | `video_assembler.py` | Multi-track timeline compositor (hooks, cards, bumpers, audio multiplexing) | `Launch-Video-NLE.cmd` |
| **[`05-faceless-generator/`](05-faceless-generator/)** | `faceless_generator.py` | Automated faceless b-roll shorts and educational reels with text overlays | `Launch-Faceless.cmd` |

---

## 🛠️ Offline & Equipment Fallback Mode

If your dedicated rendering server (CT127 / local workstation) is ever unavailable:
1. **Cloud GPU Fallback:** Use the Google Colab quickstart notebook in [`../colab/`](../colab/) for heavy neural mesh lip-sync generation on free cloud GPUs.
2. **Local CPU Fallback:** Run `01-voice-studio` and `03-card-studio` locally on any standard laptop or PC without GPU hardware.
3. **Assemble:** Stitch the generated talking head and scene cards using `04-video-nle`.
