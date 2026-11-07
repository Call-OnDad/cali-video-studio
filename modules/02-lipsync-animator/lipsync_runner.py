"""lipsync_runner.py — Cali LipSync Animator Standalone CLI.

Feeds avatar portrait base image + speech WAV directly into neural talking-head pipeline
(SadTalker / MuseTalk) for 100% syllable-locked video generation.

CLI Usage:
    python lipsync_runner.py --image avatar.png --audio speech.wav --output result.mp4
"""
import sys
import argparse
import subprocess
from pathlib import Path


def generate_lipsync(image_path: Path, audio_path: Path, output_path: Path, size: int = 256, device: str = "cuda"):
    """Runs audio-driven neural lip-sync inference."""
    image_path = Path(image_path)
    audio_path = Path(audio_path)
    output_path = Path(output_path)

    if not image_path.exists():
        raise FileNotFoundError(f"Avatar image not found: {image_path}")
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    res_dir = output_path.parent / "temp_res"
    res_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        sys.executable, "inference.py",
        "--driven_audio", str(audio_path),
        "--source_image", str(image_path),
        "--result_dir", str(res_dir),
        "--still",
        "--preprocess", "full",
        "--size", str(size)
    ]
    if device == "cpu":
        cmd.append("--cpu")

    print(f"[Cali LipSync] Running neural audio-to-video inference ({device})...")
    subprocess.run(cmd, check=True)

    # Locate generated output
    mp4s = list(res_dir.glob("**/*.mp4"))
    if mp4s:
        latest = sorted(mp4s, key=lambda p: p.stat().st_mtime)[-1]
        latest.replace(output_path)
        print(f"[Cali LipSync] Success! Master video generated -> {output_path}")
    else:
        raise RuntimeError("No output video found from inference.")


def main():
    parser = argparse.ArgumentParser(description="Cali LipSync — Direct Neural Audio-Driven Talking Head Animator")
    parser.add_argument("--image", "-i", required=True, help="Input avatar portrait image (.png/.jpg)")
    parser.add_argument("--audio", "-a", required=True, help="Input speech audio (.wav)")
    parser.add_argument("--output", "-o", required=True, help="Output MP4 path")
    parser.add_argument("--device", choices=["cuda", "cpu"], default="cuda", help="Inference device (cuda or cpu)")
    parser.add_argument("--size", type=int, default=256, help="Facial crop dimension (default: 256)")

    args = parser.parse_args()
    generate_lipsync(Path(args.image), Path(args.audio), Path(args.output), size=args.size, device=args.device)


if __name__ == "__main__":
    main()
