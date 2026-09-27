"""Render the Kalvi image-motion review with the original channel audio."""

import json
import math
import subprocess
from pathlib import Path

import imageio_ffmpeg
import numpy as np
from PIL import Image


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
AUDIO = ROOT / "source/youtube/_Ceq0AzIQ9c.m4a"
OUTPUT = HERE / "KALVI-CINEMATIC-v3-UNIQUE-IMAGES.mp4"
LOGO = HERE / "channel-emblem.png"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
W, H, FPS = 1280, 720, 24
FRAMES = 8718  # 363.25 s; source container reports 363.26 s.

# Every shot uses its own artwork. Opening/closing geography frames the arc.
SHOTS = [
    ("KV13-wide-orchestral-opening.png", .50, .51, 1.02, "wide orchestral opening"),
    ("KV01-learning-courtyard.png", .50, .53, 1.04, "courtyard gathering"),
    ("KV03-learning-tools.png", .48, .55, 1.05, "learning materials"),
    ("KV14-pebble-counting.png", .50, .52, 1.05, "counting pebbles"),
    ("KV02-measurement.png", .50, .51, 1.05, "patient measurement"),
    ("KV15-measuring-cord.png", .51, .52, 1.05, "measuring cord"),
    ("KV07-sand-geometry.png", .50, .56, 1.05, "drawing in sand"),
    ("KV16-palm-reading.png", .52, .51, 1.05, "reading palm leaf"),
    ("KV08-learning-veranda.png", .52, .51, 1.05, "reading together"),
    ("KV17-stylus-craft.png", .51, .52, 1.05, "artisan teaches"),
    ("KV05-water-model.png", .50, .53, 1.05, "demonstration model"),
    ("KV06-sand-water.png", .51, .54, 1.05, "water and sand metaphor"),
    ("KV18-irrigation-lesson.png", .51, .54, 1.05, "irrigation lesson"),
    ("KV04-practical-craft.png", .51, .51, 1.05, "practice in craft"),
    ("KV19-workshop-inspection.png", .51, .51, 1.05, "workshop inspection"),
    ("KV11-tools-detail.png", .50, .56, 1.06, "useful tools"),
    ("KV20-water-channel.png", .50, .55, 1.05, "water channel"),
    ("KV09-student-explains.png", .51, .51, 1.05, "learner explains"),
    ("KV21-market-measurement.png", .51, .52, 1.05, "community craft"),
    ("KV10-irrigation-practice.png", .51, .53, 1.05, "knowledge in use"),
    ("KV22-seed-counting.png", .51, .53, 1.05, "teaching onward"),
    ("KV23-teaching-blocks.png", .50, .54, 1.05, "teaching materials"),
    ("KV12-community-learning.png", .51, .51, 1.05, "community learning"),
    ("KV24-wide-closing.png", .50, .51, 1.03, "wide closing"),
]


def choose_cuts():
    pcm = subprocess.check_output([FFMPEG, "-loglevel", "error", "-i", str(AUDIO),
                                   "-ac", "1", "-ar", "8000", "-f", "f32le", "pipe:1"])
    samples = np.frombuffer(pcm, dtype="<f4")
    points = [0]
    for index in range(1, len(SHOTS)):
        nominal = round(index * FRAMES / len(SHOTS))
        lo = max(points[-1] + 220, nominal - 30)
        hi = min(FRAMES - (len(SHOTS) - index) * 220, nominal + 30)
        def score(frame):
            center = int(frame * 8000 / FPS)
            window = samples[max(0, center - 700):min(len(samples), center + 700)]
            return float(np.mean(window * window)) + .000002 * abs(frame - nominal)
        points.append(min(range(lo, hi + 1), key=score))
    return points + [FRAMES]


def camera(source, spec, local, duration, index):
    _, cx, cy, base, _ = spec
    t = local / max(duration - 1, 1)
    zoom = base + (.042 * t if index % 2 == 0 else .042 * (1 - t))
    sw, sh = source.size
    cw = min(sw / zoom, sh * W / H / zoom)
    ch = cw * H / W
    drift = (t - .5) * .028 * sw * (1 if index % 2 == 0 else -1)
    x = min(max(cx * sw - cw / 2 + drift, 0), sw - cw)
    y = min(max(cy * sh - ch / 2, 0), sh - ch)
    return source.crop((round(x), round(y), round(x + cw), round(y + ch))).resize(
        (W, H), Image.Resampling.BICUBIC)


def main():
    assert AUDIO.is_file() and AUDIO.stat().st_size > 1_000_000
    assert all((HERE / shot[0]).is_file() for shot in SHOTS)
    assert len({shot[0] for shot in SHOTS}) == len(SHOTS), "image repeated"
    assert LOGO.is_file()
    points = choose_cuts()
    manifest = {
        "sourceVideoId": "_Ceq0AzIQ9c", "sourceAudio": str(AUDIO.relative_to(ROOT)),
        "fps": FPS, "targetFrames": FRAMES, "imageDerived": True,
        "cutRule": "nearby low-energy points; human lyric and music timing unverified",
        "shots": [dict(image=spec[0], role=spec[4], inFrame=points[i],
                       outFrame=points[i + 1], center=[spec[1], spec[2]],
                       baseZoom=spec[3]) for i, spec in enumerate(SHOTS)],
    }
    (HERE / "review-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    images = {name: Image.open(HERE / name).convert("RGB") for name, *_ in SHOTS}
    logo = Image.open(LOGO).convert("RGBA")
    command = [FFMPEG, "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo",
               "-pixel_format", "rgb24", "-video_size", f"{W}x{H}", "-framerate", str(FPS),
               "-i", "pipe:0", "-i", str(AUDIO), "-map", "0:v:0", "-map", "1:a:0",
               "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
               "-c:a", "copy", "-movflags", "+faststart", str(OUTPUT)]
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    try:
        for i, spec in enumerate(SHOTS):
            duration = points[i + 1] - points[i]
            print(f"shot {i + 1}/{len(SHOTS)} {spec[0]} {duration} frames", flush=True)
            for local in range(duration):
                frame = camera(images[spec[0]], spec, local, duration, i)
                frame.paste(logo, (24, H - 24 - logo.height), logo)
                process.stdin.write(frame.tobytes())
    finally:
        process.stdin.close()
    if process.wait() != 0:
        raise RuntimeError("FFmpeg encode failed")
    print(OUTPUT)


if __name__ == "__main__":
    main()
