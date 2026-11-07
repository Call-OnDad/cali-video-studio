# Cali Video NLE (Standalone Module)

Multi-track timeline compositor and automated video master assembler.

## Features
- Stitches talking-head hooks, presentation cards, and outro bumpers.
- Audio multiplexing with automatic duration matching.
- Lossless concatenation when streams match, or standard 24fps H.264/AAC re-encode.

## Usage

```bash
python video_assembler.py \
  --hook hook.mp4 \
  --card scene01.png --card-duration 5.0 \
  --audio narration.wav \
  -o final_video.mp4
```
