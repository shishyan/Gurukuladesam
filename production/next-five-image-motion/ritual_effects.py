"""Add restrained lamp, incense, smoke and selected storm effects to a finished film.

Audio is copied bit for bit from the input container. The input video is never replaced.
"""

import argparse
import json
import math
import random
import subprocess
from pathlib import Path

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parent
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
W, H, FPS = 1280, 720, 24
ASSETS = ROOT / "ritual-assets"


def isolated(path, box, size):
    image = Image.open(path).convert("RGBA").crop(box)
    bounds = image.getchannel("A").getbbox()
    if not bounds:
        raise ValueError(f"Asset lacks alpha content: {path}")
    image = image.crop(bounds)
    image.thumbnail(size, Image.Resampling.LANCZOS)
    return image


def smoke_layer(frame_number, origins):
    # Small, translucent layer keeps the effect soft and inexpensive to animate.
    layer = Image.new("RGBA", (W // 4, H // 4))
    draw = ImageDraw.Draw(layer)
    time = frame_number / FPS
    for x, y in origins:
        sx, sy = x / 4, y / 4
        for strand in range(2):
            phase = strand * 1.9 + x * .013
            points = []
            for step in range(27):
                rise = step * 2.3
                bend = min(1.0, rise / 18)
                drift = bend * (4.5 * math.sin(time * .57 + rise * .08 + phase)
                                + 2.0 * math.sin(time * .31 + rise * .19 + phase * 2))
                points.append((sx + drift + strand * 1.2, sy - rise))
            for segment in range(len(points) - 1):
                # Soft density waves travel upward while the root stays attached to the ember.
                wave = .58 + .42 * math.sin(segment * .39 - time * 1.05 + phase)
                fade = max(.15, 1 - segment / 32)
                alpha = round((56 if strand == 0 else 30) * wave * fade)
                draw.line((points[segment], points[segment + 1]),
                          fill=(231, 231, 227, alpha), width=3 if strand == 0 else 2)
    layer = layer.filter(ImageFilter.GaussianBlur(1.0))
    return layer.resize((W, H), Image.Resampling.BILINEAR)


def rain_layer(frame_number):
    layer = Image.new("RGBA", (W, H))
    draw = ImageDraw.Draw(layer)
    rng = random.Random(frame_number * 1171 + 23)
    for _ in range(38):
        x, y = rng.randrange(W), rng.randrange(H)
        length = rng.randrange(9, 19)
        draw.line((x, y, x - 3, y + length), fill=(211, 225, 239, rng.randrange(10, 25)), width=1)
    return layer


def shot_for_frame(shots, frame):
    for number, shot in enumerate(shots, 1):
        if shot["inFrame"] <= frame < shot["outFrame"]:
            return number, frame - shot["inFrame"], shot["outFrame"] - shot["inFrame"]
    return len(shots), 0, 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--rain-shots", default="", help="Comma-separated 1-based outdoor shot numbers")
    parser.add_argument("--preview-frames", type=int, default=0)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    folder = args.manifest.parent
    source = folder / manifest["output"]
    target = folder / source.name.replace("-v1.mp4", "-ritual-v2.mp4")
    rain_shots = {int(s) for s in args.rain_shots.split(",") if s.strip()}
    if not source.is_file() or not rain_shots.issubset(range(1, len(manifest["shots"]) + 1)):
        raise ValueError("Missing source or invalid rain shot")

    lamp = isolated(ASSETS / "dheepam.png", (0, 0, 1200, 1200), (90, 110))
    incense = isolated(ASSETS / "agarbatti.png", (0, 0, 1024, 1536), (105, 145))
    positions = [(127, H - 15 - lamp.height), (1104, H - 15 - lamp.height)]
    incense_pos = [(225, H - 15 - incense.height), (950, H - 15 - incense.height)]
    smoke_origins = [(x + round(incense.width * p), y + round(incense.height * q))
                     for x, y in incense_pos
                     for p, q in ((.21, .15), (.40, .07), (.64, .12), (.82, .18))]
    glows = []
    for strength in range(6, 24):
        glow = Image.new("RGBA", (64, 70))
        ImageDraw.Draw(glow).ellipse((18, 10, 46, 55), fill=(255, 198, 82, strength))
        glows.append(glow.filter(ImageFilter.GaussianBlur(9)))
    decoder = subprocess.Popen([FFMPEG, "-hide_banner", "-loglevel", "error", "-i", str(source),
                                "-map", "0:v:0", "-f", "rawvideo", "-pix_fmt", "rgb24", "pipe:1"],
                               stdout=subprocess.PIPE)
    output = target if not args.preview_frames else folder / "ritual-preview.mp4"
    encoder = subprocess.Popen([FFMPEG, "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo",
                                "-pix_fmt", "rgb24", "-video_size", f"{W}x{H}", "-framerate", str(FPS),
                                "-i", "pipe:0", "-i", str(source), "-map", "0:v:0", "-map", "1:a:0",
                                "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p",
                                "-c:a", "copy", "-movflags", "+faststart", str(output)], stdin=subprocess.PIPE)
    count = 0
    frame_size = W * H * 3
    try:
        while True:
            raw = decoder.stdout.read(frame_size)
            if not raw:
                break
            if len(raw) != frame_size:
                raise RuntimeError("Incomplete decoded frame")
            frame = Image.frombytes("RGB", (W, H), raw).convert("RGBA")
            shot_no, local, duration = shot_for_frame(manifest["shots"], count)
            if shot_no in rain_shots:
                frame.alpha_composite(rain_layer(count))
                # Two short cloud flashes in the storm passage, without a hard zigzag graphic.
                if any(abs(local - round(duration * p)) <= 1 for p in (.33, .77)):
                    flash = Image.new("RGBA", (W, H), (202, 220, 247, 43))
                    frame.alpha_composite(flash)
            for side, (x, y) in enumerate(positions):
                frame.alpha_composite(lamp, (x, y))
                # Flame halo changes gently at an irrational cadence, avoiding a looping blink.
                flicker = 13 + round(5 * math.sin(count * .19 + side * 1.3) + 3 * math.sin(count * .071))
                frame.alpha_composite(glows[max(6, min(23, flicker)) - 6],
                                      (x + lamp.width // 2 - 32, y - 10))
            for x, y in incense_pos:
                frame.alpha_composite(incense, (x, y))
            frame.alpha_composite(smoke_layer(count, smoke_origins))
            encoder.stdin.write(frame.convert("RGB").tobytes())
            count += 1
            if count % 1000 == 0:
                print(f"{count} frames", flush=True)
            if args.preview_frames and count >= args.preview_frames:
                break
    finally:
        decoder.stdout.close()
        encoder.stdin.close()
    if encoder.wait() != 0:
        raise RuntimeError("Effect encoding failed")
    if not args.preview_frames and decoder.wait() != 0:
        raise RuntimeError("Source decoding failed")
    print(output)


if __name__ == "__main__":
    main()
