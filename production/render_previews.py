from __future__ import annotations

import math
import subprocess
from pathlib import Path

import imageio_ffmpeg


ROOT = Path(__file__).resolve().parents[1]
FFMPEG = Path(imageio_ffmpeg.get_ffmpeg_exe())
VISUALS = ROOT / "production" / "visuals"
SOURCES = ROOT / "source" / "youtube"
OUT = ROOT / "renders" / "previews"
OUT.mkdir(parents=True, exist_ok=True)

JOBS = [
    ("thiruppavai1", "RDcw0Bol-cE", 331.046),
    ("maasil-veenaiyum", "cKyT1Cv7zEA", 273.0),
    ("tamil-thai-vazhthu", "ETELjf0OTi4", 252.0),
    ("namo-narayanam", "4vZEVROZIx8", 455.0),
]


def find_audio(video_id: str) -> Path:
    matches = list(SOURCES.glob(f"{video_id}-*.m4a"))
    if len(matches) != 1:
        raise RuntimeError(f"Expected one audio file for {video_id}, found {matches}")
    return matches[0]


def render(name: str, video_id: str, duration: float) -> None:
    images = sorted((VISUALS / name).glob("*.png"))
    if not images:
        raise RuntimeError(f"No images found for {name}")

    seconds_per_image = 12
    count = math.ceil(duration / seconds_per_image)
    sequence = [images[i % len(images)] for i in range(count)]
    concat = OUT / f"{name}.concat.txt"
    lines: list[str] = []
    for image in sequence:
        escaped = image.as_posix().replace("'", "'\\''")
        lines.extend([f"file '{escaped}'", f"duration {seconds_per_image}"])
    lines.append(f"file '{sequence[-1].as_posix()}'")
    concat.write_text("\n".join(lines) + "\n", encoding="utf-8")

    output = OUT / f"{name}-cinematic-preview.mp4"
    command = [
        str(FFMPEG), "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat),
        "-i", str(find_audio(video_id)),
        "-t", str(duration),
        "-vf",
        "scale=1344:756:force_original_aspect_ratio=increase,"
        "crop=1280:720,zoompan=z='min(zoom+0.0002,1.06)':"
        "x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=288:s=1280x720:fps=24,"
        "format=yuv420p",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
        "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
        "-movflags", "+faststart", "-shortest", str(output),
    ]
    print(f"Rendering {output.name}", flush=True)
    subprocess.run(command, check=True)


if __name__ == "__main__":
    for job in JOBS:
        render(*job)
