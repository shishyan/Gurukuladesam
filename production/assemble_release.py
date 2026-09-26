from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import imageio_ffmpeg


ROOT = Path(__file__).resolve().parents[1]
FFMPEG = Path(imageio_ffmpeg.get_ffmpeg_exe())
DURATION_RE = re.compile(r"Duration: (\d+):(\d+):(\d+(?:\.\d+)?)")


def duration(path: Path) -> float:
    result = subprocess.run(
        [str(FFMPEG), "-hide_banner", "-i", str(path)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    match = DURATION_RE.search(result.stderr)
    if not match:
        raise RuntimeError(f"Could not read duration: {path}")
    hours, minutes, seconds = match.groups()
    return int(hours) * 3600 + int(minutes) * 60 + float(seconds)


def load_manifest(path: Path) -> tuple[Path, list[Path], float]:
    data = json.loads(path.read_text(encoding="utf-8"))
    audio = (ROOT / data["audio"]).resolve()
    clips = [(ROOT / item).resolve() for item in data["clips"]]
    fade = float(data.get("dissolve_seconds", 0.5))
    if not audio.is_file():
        raise FileNotFoundError(f"Audio missing: {audio}")
    if len(clips) < 2:
        raise ValueError("At least two approved clips are required")
    missing = [str(item) for item in clips if not item.is_file()]
    if missing:
        raise FileNotFoundError("Approved clips missing:\n" + "\n".join(missing))
    if not 0.0 < fade <= 1.5:
        raise ValueError("dissolve_seconds must be greater than 0 and at most 1.5")
    return audio, clips, fade


def build_filter(clip_lengths: list[float], fade: float) -> tuple[str, str, float]:
    parts: list[str] = []
    labels: list[str] = []
    for index, clip_length in enumerate(clip_lengths):
        label = f"v{index}"
        parts.append(
            f"[{index}:v]scale=1920:1080:force_original_aspect_ratio=increase,"
            "crop=1920:1080,fps=24,settb=AVTB,setsar=1,format=yuv420p,setpts=PTS-STARTPTS,"
            f"fade=t=in:st=0:d={fade:.3f},"
            f"fade=t=out:st={max(0.0, clip_length - fade):.3f}:d={fade:.3f}[{label}]"
        )
        labels.append(f"[{label}]")
    parts.append("".join(labels) + f"concat=n={len(labels)}:v=1:a=0[outv]")
    return ";".join(parts), "outv", sum(clip_lengths)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Assemble approved motion clips with soft dissolves and untouched AAC source audio."
    )
    parser.add_argument("manifest", type=Path, help="JSON manifest relative to the current directory")
    parser.add_argument("output", type=Path, help="New MP4 output path; an existing file is never overwritten")
    args = parser.parse_args()

    manifest = args.manifest.resolve()
    output = args.output.resolve()
    if output.exists():
        raise FileExistsError(f"Refusing to overwrite existing output: {output}")
    audio, clips, fade = load_manifest(manifest)
    audio_length = duration(audio)
    clip_lengths = [duration(item) for item in clips]
    filtergraph, video_label, assembled_length = build_filter(clip_lengths, fade)
    if assembled_length + 0.05 < audio_length:
        raise RuntimeError(
            f"Approved footage is incomplete: {assembled_length:.3f}s available after dissolves, "
            f"but audio is {audio_length:.3f}s (short by {audio_length - assembled_length:.3f}s)"
        )

    output.parent.mkdir(parents=True, exist_ok=True)
    command = [str(FFMPEG), "-hide_banner", "-loglevel", "error", "-nostdin", "-n"]
    for clip in clips:
        command.extend(["-i", str(clip)])
    command.extend(["-i", str(audio), "-filter_complex", filtergraph])
    command.extend(
        [
            "-map", f"[{video_label}]", "-map", f"{len(clips)}:a:0",
            "-t", f"{audio_length:.3f}", "-c:v", "libx264", "-preset", "slow",
            "-crf", "17", "-pix_fmt", "yuv420p", "-r", "24", "-c:a", "copy",
            "-movflags", "+faststart", str(output),
        ]
    )
    subprocess.run(command, check=True)
    print(f"Created: {output}")
    print(f"Audio copied without re-encoding: {audio}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
