"""faceless_generator.py — Cali Faceless Video Generator Standalone.

Generates high-retention faceless videos, trend explainers, and educational shorts
from markdown scripts or JSON storyboards without requiring talking-head avatars.

CLI Usage:
    python faceless_generator.py --script script.txt --broll broll_folder/ --output faceless_short.mp4
"""
import sys
import argparse
import subprocess
from pathlib import Path


def generate_faceless_clip(image_or_video: Path, text_line: str, duration: float, out_clip: Path):
    out_clip = Path(out_clip)
    out_clip.parent.mkdir(parents=True, exist_ok=True)

    # Render with centered subtitle text overlay
    vf = (
        "scale=720:1280:force_original_aspect_ratio=decrease,"
        "pad=720:1280:(ow-iw)/2:(oh-ih)/2:color='#070d17',"
        f"drawtext=text='{text_line}':fontcolor=white:fontsize=36:x=(w-text_w)/2:y=h-240:"
        "box=1:boxcolor='#0c1a2e@0.85':boxborderw=16"
    )

    cmd = [
        "ffmpeg", "-v", "error", "-y",
        "-loop", "1", "-i", str(image_or_video),
        "-t", str(duration),
        "-vf", vf,
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "24",
        str(out_clip)
    ]
    subprocess.run(cmd, check=True)
    return out_clip


def main():
    parser = argparse.ArgumentParser(description="Cali Faceless Video Generator — Automated B-Roll Reels")
    parser.add_argument("--image", "-i", required=True, help="Background graphic or b-roll image")
    parser.add_argument("--caption", "-c", required=True, help="Subtitle / hook caption line")
    parser.add_argument("--duration", "-d", type=float, default=5.0, help="Scene duration in seconds")
    parser.add_argument("--output", "-o", default="faceless_scene.mp4", help="Output MP4 path")

    args = parser.parse_args()
    generate_faceless_clip(Path(args.image), args.caption, args.duration, Path(args.output))
    print(f"[Cali Faceless] Rendered scene -> {args.output}")


if __name__ == "__main__":
    main()
