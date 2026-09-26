"""Build a clean, channel-branded Vaan Sirappu cut from selected shots.

Requires Git LFS media for every file in batch-v15.json, Pillow, NumPy,
and imageio-ffmpeg. Preserves the exact source AAC stream.
"""

import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw

import render_full_review as review


HERE = Path(__file__).resolve().parent
BATCH = HERE.parent
ROOT = HERE.parents[3]
FFMPEG = review.FFMPEG
PRIOR = HERE / "VAAN-clean-selected-161s.mp4"
LOGO = HERE / "channel-logo-overlay.png"
SOURCE_LOGO = ROOT / "production/gananatha-om/channel-avatar-reference.jpg"
OUTPUT = HERE / "VAAN-SIRAPPU-CINEMATIC-v2.mp4"


def render_prior():
    manifest = json.loads((BATCH / "batch-v15.json").read_text(encoding="utf-8"))
    shots = manifest["shots"]
    assert sum(s["outFrame"] - s["inFrame"] for s in shots) == review.PRIOR_FRAMES
    args = [FFMPEG, "-hide_banner", "-loglevel", "error", "-y"]
    filters = []
    for i, shot in enumerate(shots):
        source = BATCH / shot["file"]
        if source.stat().st_size < 1_000:
            raise RuntimeError(f"Git LFS source not materialized: {source}")
        args += ["-i", str(source)]
        filters.append(
            f"[{i}:v]fps=24,trim=start_frame={shot['inFrame']}:end_frame={shot['outFrame']},"
            f"setpts=PTS-STARTPTS,fps=24,scale=1280:720:force_original_aspect_ratio=decrease,"
            f"pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1[v{i}]"
        )
    filters.append("".join(f"[v{i}]" for i in range(len(shots))) + f"concat=n={len(shots)}:v=1:a=0[v]")
    args += ["-filter_complex", ";".join(filters), "-map", "[v]", "-an", "-c:v", "libx264",
             "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(PRIOR)]
    subprocess.run(args, check=True)


def prepare_logo():
    source = Image.open(SOURCE_LOGO).convert("RGB").resize((102, 102), Image.Resampling.LANCZOS)
    mask = Image.new("L", (102, 102), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, 101, 101), fill=255)
    logo = Image.new("RGBA", (102, 102), (0, 0, 0, 0))
    logo.paste(source, (0, 0), mask)
    logo.save(LOGO)


def assemble():
    subprocess.run([
        FFMPEG, "-hide_banner", "-loglevel", "error", "-y",
        "-i", str(PRIOR), "-i", str(review.TAIL), "-i", str(review.AUDIO),
        "-loop", "1", "-i", str(LOGO),
        "-filter_complex", "[0:v][1:v]concat=n=2:v=1:a=0[j];"
        "[j][3:v]overlay=x=24:y=H-h-24:format=auto[v]",
        "-map", "[v]", "-map", "2:a:0", "-frames:v", str(review.TOTAL_FRAMES),
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
        "-c:a", "copy", "-movflags", "+faststart", str(OUTPUT),
    ], check=True)


def main():
    render_prior()
    print(f"clean prior: {PRIOR}", flush=True)
    review.render_tail(review.music_cuts())
    print(f"image-motion tail: {review.TAIL}", flush=True)
    prepare_logo()
    assemble()
    print(OUTPUT)


if __name__ == "__main__":
    main()
