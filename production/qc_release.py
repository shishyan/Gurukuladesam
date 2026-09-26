from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import imageio_ffmpeg


FFMPEG = Path(imageio_ffmpeg.get_ffmpeg_exe())
DURATION_RE = re.compile(r"Duration: (\d+):(\d+):(\d+(?:\.\d+)?)")
VIDEO_RE = re.compile(r"Video: ([^,]+).*?, (\d{2,5})x(\d{2,5}).*?, ([\d.]+) fps")
AUDIO_RE = re.compile(r"Audio: ([^,]+), (\d+) Hz, ([^,]+)")
BLACK_RE = re.compile(r"black_start:([\d.]+).*?black_end:([\d.]+)")


def inspect(path: Path) -> tuple[str, float]:
    result = subprocess.run(
        [str(FFMPEG), "-hide_banner", "-i", str(path)],
        stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True,
        encoding="utf-8", errors="replace",
    )
    match = DURATION_RE.search(result.stderr)
    if not match:
        raise RuntimeError("FFmpeg could not identify the file")
    h, m, s = match.groups()
    return result.stderr, int(h) * 3600 + int(m) * 60 + float(s)


def main() -> int:
    parser = argparse.ArgumentParser(description="Non-destructive upload-readiness QC for a release MP4")
    parser.add_argument("video", type=Path)
    parser.add_argument("--expected-audio", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    video = args.video.resolve()
    if not video.is_file():
        raise FileNotFoundError(video)

    metadata, video_duration = inspect(video)
    video_match = VIDEO_RE.search(metadata)
    audio_match = AUDIO_RE.search(metadata)
    failures: list[str] = []
    warnings: list[str] = []
    if not video_match:
        failures.append("No readable video stream")
        video_data = None
    else:
        codec, width, height, fps = video_match.groups()
        video_data = {"codec": codec.strip(), "width": int(width), "height": int(height), "fps": float(fps)}
        if (int(width), int(height)) != (1920, 1080):
            failures.append(f"Frame size is {width}x{height}, expected 1920x1080")
        if abs(float(fps) - 24.0) > 0.02:
            failures.append(f"Frame rate is {fps}, expected 24 fps")
    if not audio_match:
        failures.append("No readable audio stream")
        audio_data = None
    else:
        codec, rate, layout = audio_match.groups()
        audio_data = {"codec": codec.strip(), "sample_rate": int(rate), "layout": layout.strip()}
        if not codec.strip().lower().startswith("aac"):
            failures.append(f"Audio codec is {codec.strip()}, expected AAC")

    expected_duration = None
    if args.expected_audio:
        _, expected_duration = inspect(args.expected_audio.resolve())
        drift = abs(video_duration - expected_duration)
        if drift > 0.10:
            failures.append(f"Duration differs from source audio by {drift:.3f}s")

    decode = subprocess.run(
        [str(FFMPEG), "-hide_banner", "-nostdin", "-v", "error", "-i", str(video), "-f", "null", "-"],
        stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True,
        encoding="utf-8", errors="replace",
    )
    if decode.returncode or decode.stderr.strip():
        failures.append("Decode/frame-integrity errors detected")

    black = subprocess.run(
        [str(FFMPEG), "-hide_banner", "-nostdin", "-i", str(video), "-vf",
         "blackdetect=d=0.5:pix_th=0.05", "-an", "-f", "null", "-"],
        stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True,
        encoding="utf-8", errors="replace",
    )
    black_segments = [{"start": float(a), "end": float(b)} for a, b in BLACK_RE.findall(black.stderr)]
    if black_segments:
        warnings.append("Black segments of at least 0.5s detected; review opening/end intent")

    report = {
        "status": "PASS" if not failures else "FAIL",
        "file": str(video), "duration_seconds": video_duration,
        "expected_audio_duration_seconds": expected_duration,
        "video": video_data, "audio": audio_data,
        "decode_errors": decode.stderr.strip(), "black_segments": black_segments,
        "failures": failures, "warnings": warnings,
    }
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    print(rendered)
    if args.report:
        report_path = args.report.resolve()
        if report_path.exists():
            raise FileExistsError(f"Refusing to overwrite report: {report_path}")
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(rendered + "\n", encoding="utf-8")
    return 0 if not failures else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
