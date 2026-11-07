"""voice_studio.py — Cali Voice Studio Standalone Engine.

Provides offline neural voice synthesis (Piper TTS / Kokoro ONNX) and EBU R128 (-16 LUFS)
loudness mastering. Can be used as a CLI utility or started as a standalone local web service.

CLI Usage:
    python voice_studio.py --text "Hello world" --output hello.wav --target-lufs -16.0
Web Server:
    python voice_studio.py --serve --port 8791
"""
import sys
import argparse
import subprocess
from pathlib import Path
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json

DEFAULT_LUFS = -16.0
DEFAULT_SAMPLE_RATE = 24000


def normalize_audio(input_file: Path, output_file: Path, target_lufs: float = DEFAULT_LUFS):
    """Normalize speech audio to EBU R128 standard (-16 LUFS integrated)."""
    input_file = Path(input_file)
    output_file = Path(output_file)
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    output_file.parent.mkdir(parents=True, exist_ok=True)
    af = f"loudnorm=I={target_lufs}:TP=-1.5:LRA=11.0"
    cmd = [
        "ffmpeg", "-v", "error", "-y",
        "-i", str(input_file),
        "-af", af,
        "-ar", str(DEFAULT_SAMPLE_RATE),
        "-ac", "1",
        "-c:a", "pcm_s16le",
        str(output_file)
    ]
    subprocess.run(cmd, check=True)
    print(f"[VoiceStudio] Mastered audio -> {output_file} ({target_lufs} LUFS)")


def synthesize_piper(text: str, output_file: Path, model_path: Path = None, speed: float = 1.0):
    """Synthesize speech using local Piper TTS binary."""
    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    raw_wav = output_file.with_suffix(".raw.wav")
    piper_cmd = ["piper", "--output_file", str(raw_wav)]
    if model_path and Path(model_path).exists():
        piper_cmd.extend(["--model", str(model_path)])

    proc = subprocess.Popen(piper_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    proc.communicate(input=text)

    if not raw_wav.exists():
        raise RuntimeError("Piper synthesis failed to output raw WAV.")

    # Master to -16 LUFS
    normalize_audio(raw_wav, output_file)
    if raw_wav.exists():
        raw_wav.unlink()
    return output_file


class VoiceHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/api/synthesize":
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length).decode("utf-8"))
            text = body.get("text", "")
            out_name = body.get("output_name", "output.wav")
            out_path = Path("exports") / out_name

            try:
                synthesize_piper(text, out_path)
                res = {"status": "success", "file": str(out_path)}
                self.send_response(200)
            except Exception as e:
                res = {"status": "error", "message": str(e)}
                self.send_response(500)

            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(res).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()


def main():
    parser = argparse.ArgumentParser(description="Cali Voice Studio — Offline TTS & Loudness Mastering")
    parser.add_argument("--text", help="Text dialogue to synthesize")
    parser.add_argument("--output", "-o", help="Output WAV path")
    parser.add_argument("--target-lufs", type=float, default=DEFAULT_LUFS, help="Target loudness (default: -16.0)")
    parser.add_argument("--model", help="Path to Piper onnx voice model")
    parser.add_argument("--serve", action="store_true", help="Start standalone HTTP API server")
    parser.add_argument("--port", type=int, default=8791, help="Port for standalone server (default: 8791)")

    args = parser.parse_args()

    if args.serve:
        server = ThreadingHTTPServer(("0.0.0.0", args.port), VoiceHandler)
        print(f"[Cali Voice Studio] Serving on http://localhost:{args.port}")
        server.serve_forever()
    elif args.text and args.output:
        synthesize_piper(args.text, Path(args.output), model_path=args.model)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
