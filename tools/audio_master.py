"""audio_master.py — Audio mastering and EBU R128 (-16 LUFS) normalization for Cali Video Studio.

Usage via CLI:
    python audio_master.py --input raw_speech.wav --output mastered_speech.wav --target-lufs -16.0
"""
import sys
import argparse
import subprocess
from pathlib import Path

DEFAULT_LOUDNESS = dict(I=-16.0, TP=-1.5, LRA=11.0)


def normalize_voice(src: Path, dst: Path, target_lufs: float = -16.0, true_peak: float = -1.5, sample_rate: int = 24000):
    """Normalize speech audio to broadcast EBU R128 loudness target using FFmpeg loudnorm filter."""
    src = Path(src)
    dst = Path(dst)
    if not src.exists():
        raise FileNotFoundError(f"Source audio file not found: {src}")

    af = f"loudnorm=I={target_lufs}:TP={true_peak}:LRA=11.0"
    dst.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "ffmpeg", "-v", "error", "-y",
        "-i", str(src),
        "-af", af,
        "-ar", str(sample_rate),
        "-ac", "1",
        "-c:a", "pcm_s16le",
        str(dst)
    ]
    subprocess.run(cmd, check=True)
    print(f"Mastered: {src.name} -> {dst.name} ({target_lufs} LUFS, {true_peak} dBTP)")


def mix_with_music(voice: Path, music: Path, dst: Path, music_gain_db: float = -21.0, target_lufs: float = -16.0):
    """Lay ducked background music bed under voice audio and re-master to target LUFS."""
    voice = Path(voice)
    music = Path(music)
    dst = Path(dst)

    if not voice.exists() or not music.exists():
        raise FileNotFoundError("Voice or music file missing.")

    filt = (
        f"[1:a]aloop=loop=-1:size=2e9,volume={music_gain_db}dB[bed];"
        "[0:a]asplit=2[voice_out][voice_sc];"
        "[bed][voice_sc]sidechaincompress=threshold=0.04:ratio=10:attack=5:release=350:makeup=1[ducked];"
        "[voice_out][ducked]amix=inputs=2:duration=first:weights=1 1,"
        f"loudnorm=I={target_lufs}:TP=-1.5:LRA=11.0[out]"
    )
    cmd = [
        "ffmpeg", "-v", "error", "-y",
        "-i", str(voice), "-i", str(music),
        "-filter_complex", filt, "-map", "[out]",
        "-ar", "24000", "-ac", "1", "-c:a", "pcm_s16le",
        str(dst)
    ]
    subprocess.run(cmd, check=True)
    print(f"Mixed & Mastered: {dst.name}")


def main():
    parser = argparse.ArgumentParser(description="Master speech audio to -16 LUFS using FFmpeg.")
    parser.add_argument("--input", "-i", required=True, help="Input raw audio file")
    parser.add_argument("--output", "-o", required=True, help="Output mastered audio file")
    parser.add_argument("--target-lufs", type=float, default=-16.0, help="Target integrated LUFS (default: -16.0)")
    parser.add_argument("--music", help="Optional background music file to duck under voice")
    parser.add_argument("--music-gain", type=float, default=-21.0, help="Music gain in dB before ducking")

    args = parser.parse_args()

    if args.music:
        mix_with_music(Path(args.input), Path(args.music), Path(args.output), music_gain_db=args.music_gain, target_lufs=args.target_lufs)
    else:
        normalize_voice(Path(args.input), Path(args.output), target_lufs=args.target_lufs)


if __name__ == "__main__":
    main()
