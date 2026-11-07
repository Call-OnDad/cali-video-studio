# Cali Voice Studio (Standalone Module)

Offline neural voice synthesis & EBU R128 (`-16 LUFS`) loudness mastering.

## Features
- Single-command voice synthesis via Piper TTS and Kokoro ONNX.
- Broadcast loudness normalization (`-16 LUFS` integrated, `-1.5 dBTP` peak ceiling).
- Standalone REST API microservice running on port `8791`.

## Quick Start

```bash
# Run standalone microservice
python voice_studio.py --serve --port 8791

# Or run one-shot via CLI
python voice_studio.py --text "Safety first at Cali Media." -o safety.wav
```
