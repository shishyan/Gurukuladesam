"""Render a full-length, unpublished Gana Natha Om image-motion review.

Uses 15 generated artworks in 30 distinct framings. Requires Pillow, NumPy,
and imageio-ffmpeg. Original channel AAC is copied unchanged.
"""

import json
import math
import random
import subprocess
import sys
from pathlib import Path

import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
AUDIO = ROOT / "source/youtube/GydxHEmyDPc.m4a"
OUTPUT = HERE / "GANA-NATHA-OM-FULL-IMAGE-MOTION-REVIEW-v1.mp4"
BRANDED_OUTPUT = HERE / "GANA-NATHA-OM-CINEMATIC-v2.mp4"
CHANNEL_LOGO = HERE / "channel-avatar-reference.jpg"
MANIFEST = HERE / "review-manifest.json"
W, H, FPS, TARGET_FRAMES = 1280, 720, 24, 5472

# (asset, center-x, center-y, base zoom, creative role)
SHOTS = [
    ("GN02-temple-exterior.png", .50, .52, 1.05, "blue-hour exterior"),
    ("GN07-banyan-garden.png", .62, .49, 1.08, "rooted temple garden"),
    ("GN15-temple-road.png", .50, .53, 1.07, "approach"),
    ("GN03-temple-bell.png", .46, .45, 1.08, "bell and distant sanctum"),
    ("GN06-lamp-corridor.png", .51, .52, 1.06, "lamp-lined mandapam"),
    ("GN01-sanctum-master.png", .50, .49, 1.04, "first complete deity reveal"),
    ("GN04-offerings.png", .60, .55, 1.08, "modakam and durva"),
    ("GN05-mouse-vahana.png", .47, .55, 1.07, "mouse vahana"),
    ("GN10-idol-close.png", .50, .47, 1.05, "coherent four-arm close view"),
    ("GN08-temple-tank.png", .50, .56, 1.04, "tank and dawn light"),
    ("GN13-lotus-tank.png", .50, .56, 1.05, "rooted lotus"),
    ("GN12-sunrise-courtyard.png", .51, .51, 1.05, "courtyard morning"),
    ("GN11-incense.png", .47, .49, 1.06, "source-connected incense"),
    ("GN09-garland.png", .47, .53, 1.08, "flower garland"),
    ("GN14-deepam.png", .47, .52, 1.08, "sheltered deepam"),
    ("GN02-temple-exterior.png", .50, .57, 1.38, "entrance detail"),
    ("GN06-lamp-corridor.png", .26, .52, 1.42, "lamp detail"),
    ("GN04-offerings.png", .62, .61, 1.38, "offering detail"),
    ("GN01-sanctum-master.png", .51, .49, 1.43, "sanctum closer view"),
    ("GN08-temple-tank.png", .60, .67, 1.38, "tank reflection"),
    ("GN07-banyan-garden.png", .71, .55, 1.36, "garden to temple"),
    ("GN11-incense.png", .29, .48, 1.40, "burner detail"),
    ("GN05-mouse-vahana.png", .32, .57, 1.37, "vahana detail"),
    ("GN12-sunrise-courtyard.png", .59, .48, 1.34, "gopuram detail"),
    ("GN13-lotus-tank.png", .29, .56, 1.38, "lotus detail"),
    ("GN14-deepam.png", .24, .46, 1.39, "flame detail"),
    ("GN09-garland.png", .25, .60, 1.36, "garland detail"),
    ("GN10-idol-close.png", .45, .43, 1.34, "blessing hand and face"),
    ("GN15-temple-road.png", .53, .53, 1.35, "open path to temple"),
    ("GN01-sanctum-master.png", .50, .49, 1.05, "final sanctum return"),
]


def choose_cuts():
    pcm = subprocess.check_output([FFMPEG, "-loglevel", "error", "-i", str(AUDIO),
                                   "-ac", "1", "-ar", "8000", "-f", "f32le", "pipe:1"])
    samples = np.frombuffer(pcm, dtype="<f4")
    rms = np.zeros(TARGET_FRAMES + 1)
    for frame in range(TARGET_FRAMES + 1):
        c = int(frame * 8000 / FPS)
        window = samples[max(0, c - 650):min(len(samples), c + 650)]
        rms[frame] = math.sqrt(float(np.mean(window * window))) if len(window) else 0
    median = max(float(np.median(rms)), 1e-5)
    points = [0]
    for index in range(1, len(SHOTS)):
        nominal = round(index * TARGET_FRAMES / len(SHOTS))
        lo = max(points[-1] + 144, nominal - 22)
        hi = min(TARGET_FRAMES - (len(SHOTS) - index) * 144, nominal + 22)
        points.append(min(range(lo, hi + 1), key=lambda f: rms[f] / median + .2 * abs(f-nominal)/22))
    points.append(TARGET_FRAMES)
    return points


def camera(source, spec, local, duration, index):
    _, cx, cy, base, _ = spec
    t = local / max(duration - 1, 1)
    zoom = base + (0.045 * t if index % 2 == 0 else 0.045 * (1 - t))
    sw, sh = source.size
    cw = min(sw / zoom, sh * W / H / zoom)
    ch = cw * H / W
    drift = (t - .5) * .035 * sw * (1 if index % 2 == 0 else -1)
    x = min(max(cx * sw - cw/2 + drift, 0), sw - cw)
    y = min(max(cy * sh - ch/2, 0), sh - ch)
    return source.crop((round(x), round(y), round(x+cw), round(y+ch))).resize((W, H), Image.Resampling.BICUBIC)


def environment(frame, image_name, global_frame):
    # Only the tank frames receive moving surface impacts. Sparse suspended
    # motes belong to exterior morning light and are never used as rain.
    tank = image_name in ("GN08-temple-tank.png", "GN13-lotus-tank.png")
    garden = image_name in ("GN07-banyan-garden.png", "GN12-sunrise-courtyard.png", "GN15-temple-road.png")
    if not tank and not garden:
        return frame
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay, "RGBA")
    if tank:
        for born in range(global_frame - 20, global_frame + 1, 4):
            if born < 0:
                continue
            rng = random.Random(5731 + born * 2311)
            for _ in range(3):
                x, y = rng.randrange(300, 1200), rng.randrange(420, 695)
                age = global_frame - born
                radius = 2 + 1.25 * age
                opacity = round(35 * (1 - age / 22))
                if opacity > 0:
                    draw.ellipse((x-radius, y-radius*.25, x+radius, y+radius*.25), outline=(224, 235, 228, opacity), width=1)
    if garden:
        rng = random.Random(9029)
        for _ in range(24):
            sx, sy = rng.randrange(120, 1110), rng.randrange(110, 625)
            speed = rng.uniform(.07, .22)
            phase = rng.uniform(0, 6.28)
            x = sx + math.sin(global_frame*.013 + phase)*10
            y = (sy - global_frame*speed) % H
            draw.ellipse((x-1, y-1, x+1, y+1), fill=(246, 211, 143, 22))
    return Image.alpha_composite(frame.convert("RGBA"), overlay).convert("RGB")


def main():
    branded = "--branded" in sys.argv[1:]
    if branded and not CHANNEL_LOGO.is_file():
        raise FileNotFoundError(CHANNEL_LOGO)
    assert all((HERE / spec[0]).is_file() for spec in SHOTS)
    points = choose_cuts()
    payload = {"sourceVideoId": "GydxHEmyDPc", "sourceAudio": str(AUDIO.relative_to(ROOT)),
               "fps": FPS, "targetFrames": TARGET_FRAMES,
               "cutRule": "nearby RMS minima; human musical and lyric timing unverified",
               "imageDerived": True,
               "shots": [dict(image=spec[0], role=spec[4], inFrame=points[i], outFrame=points[i+1],
                              center=[spec[1], spec[2]], baseZoom=spec[3]) for i, spec in enumerate(SHOTS)]}
    MANIFEST.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    images = {name: Image.open(HERE / name).convert("RGB") for name, *_ in SHOTS}
    logo = None
    if branded:
        source_logo = Image.open(CHANNEL_LOGO).convert("RGB").resize((102, 102), Image.Resampling.LANCZOS)
        logo = Image.new("RGBA", (102, 102), (0, 0, 0, 0))
        mask = Image.new("L", (102, 102), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, 101, 101), fill=255)
        logo.paste(source_logo, (0, 0), mask)
    filter_text = "drawtext=text='GANA NATHA OM - IMAGE MOTION REVIEW':x=12:y=10:fontsize=18:fontcolor=white:box=1:boxcolor=black@0.45"
    command = [FFMPEG, "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo",
               "-pixel_format", "rgb24", "-video_size", f"{W}x{H}", "-framerate", str(FPS),
               "-i", "pipe:0", "-i", str(AUDIO)]
    if not branded:
        command += ["-vf", filter_text]
    command += [
               "-map", "0:v:0", "-map", "1:a:0", "-c:v", "libx264", "-preset", "veryfast",
               "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart",
               str(BRANDED_OUTPUT if branded else OUTPUT)]
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    try:
        for i, spec in enumerate(SHOTS):
            duration = points[i+1] - points[i]
            print(f"shot {i+1}/{len(SHOTS)} {spec[0]} {duration} frames", flush=True)
            for local in range(duration):
                image = camera(images[spec[0]], spec, local, duration, i)
                image = environment(image, spec[0], points[i] + local)
                if logo is not None:
                    image.paste(logo, (24, H - 24 - logo.height), logo)
                process.stdin.write(image.tobytes())
    finally:
        process.stdin.close()
    if process.wait() != 0:
        raise RuntimeError("ffmpeg encode failed")
    print(BRANDED_OUTPUT if branded else OUTPUT)


if __name__ == "__main__":
    main()
