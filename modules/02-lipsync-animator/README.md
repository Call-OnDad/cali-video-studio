# Cali LipSync Animator (Standalone Module)

Direct audio-driven neural talking-head animation. Frame-accurate mouth closure and syllable synchronization driven directly by acoustic frequencies.

## Features
- **Say Anything Architecture:** Characters articulate any dialogue line freely.
- **100% Syllable-Locked:** Neural 3DMM phoneme tracking.
- **Zero Credit Cost:** Runs locally on NVIDIA GPU or via free Google Colab T4 GPU.

## Usage

```bash
# Local GPU Execution
python lipsync_runner.py -i portrait.png -a speech.wav -o output.mp4
```

### Free Cloud GPU Fallback (Google Colab)
If local hardware lacks an NVIDIA GPU, open [`../../colab/audio_driven_lipsync_quickstart.ipynb`](../../colab/audio_driven_lipsync_quickstart.ipynb) in Google Colab, set runtime to T4 GPU, upload your files, and click **Run All**.
