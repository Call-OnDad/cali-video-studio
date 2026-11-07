"""video_assembler.py — Cali Video NLE Standalone Multi-Track Assembler.

Stitches video hooks, presentation cards, audio tracks, ducked music, and brand bumpers
into broadcast-ready MP4 masters.

CLI Usage:
    python video_assembler.py --hook hook.mp4 --card card.png --card-duration 5.0 --output master.mp4
"""
import sys
import argparse
import subprocess
from pathlib import Path


def assemble_story(
    hook_video: Path,
    scene_cards: list,
    output_mp4: Path,
    voice_audio: Path = None,
    bumper_video: Path = None
):
    output_mp4 = Path(output_mp4)
    output_mp4.parent.mkdir(parents=True, exist_ok=True)
    temp_dir = output_mp4.parent / "temp_nle"
    temp_dir.mkdir(parents=True, exist_ok=True)

    clip_list = []

    # 1. Hook clip
    if hook_video and Path(hook_video).exists():
        clip_list.append(str(hook_video.resolve()))

    # 2. Scene cards -> convert to short mp4 clips
    for idx, (card_img, duration) in enumerate(scene_cards):
        card_img = Path(card_img)
        if not card_img.exists():
            continue
        card_clip = temp_dir / f"card_{idx}.mp4"
        cmd = [
            "ffmpeg", "-v", "error", "-y",
            "-loop", "1", "-i", str(card_img),
            "-t", str(duration),
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-r", "24", "-vf", "scale=720:1280",
            str(card_clip)
        ]
        subprocess.run(cmd, check=True)
        clip_list.append(str(card_clip.resolve()))

    # 3. Bumper
    if bumper_video and Path(bumper_video).exists():
        clip_list.append(str(bumper_video.resolve()))

    if not clip_list:
        raise ValueError("No video clips available to assemble.")

    # Concat file
    concat_txt = temp_dir / "concat.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for c in clip_list:
            f.write(f"file '{c.replace(chr(92), '/')}'\n")

    unmuxed_video = temp_dir / "unmuxed.mp4"
    subprocess.run([
        "ffmpeg", "-v", "error", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_txt),
        "-c", "copy",
        str(unmuxed_video)
    ], check=True)

    # Multiplex audio if provided
    if voice_audio and Path(voice_audio).exists():
        subprocess.run([
            "ffmpeg", "-v", "error", "-y",
            "-i", str(unmuxed_video),
            "-i", str(voice_audio),
            "-c:v", "copy",
            "-c:a", "aac", "-b:a", "192k",
            "-shortest",
            str(output_mp4)
        ], check=True)
    else:
        unmuxed_video.replace(output_mp4)

    print(f"[Cali NLE] Assembled video master -> {output_mp4}")


def main():
    parser = argparse.ArgumentParser(description="Cali Video NLE — Standalone Multi-Track Video Assembler")
    parser.add_argument("--hook", help="Hook video clip (.mp4)")
    parser.add_argument("--card", help="Presentation card (.png)")
    parser.add_argument("--card-duration", type=float, default=5.0, help="Duration to show card in seconds")
    parser.add_argument("--audio", help="Optional synchronized master audio (.wav/.mp3)")
    parser.add_argument("--output", "-o", default="assembled_master.mp4", help="Output MP4 path")

    args = parser.parse_args()
    cards = []
    if args.card:
        cards.append((args.card, args.card_duration))

    assemble_story(
        Path(args.hook) if args.hook else None,
        cards,
        Path(args.output),
        voice_audio=Path(args.audio) if args.audio else None
    )


if __name__ == "__main__":
    main()
