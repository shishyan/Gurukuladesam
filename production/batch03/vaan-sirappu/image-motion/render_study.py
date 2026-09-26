"""Render an 18-second Vaan Sirappu image-motion study with original audio.

Requires Pillow and imageio-ffmpeg. Images are generated film artwork; weather
and camera motion are deterministic composites, not generated video footage.
"""

from pathlib import Path
import math
import random
import subprocess

from PIL import Image, ImageDraw, ImageEnhance
import imageio_ffmpeg


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SOURCES = [HERE / x for x in (
    "VS40-monsoon-valley.png", "VS41-rain-fed-paddy.png", "VS42-temple-tank.png"
)]
AUDIO = ROOT / "source/youtube/tX4JtRSOuxE.m4a"
OUTPUT = HERE / "VAAN-image-motion-study-18s.mp4"
W, H, FPS, SHOT_SECONDS = 1280, 720, 24, 6


def camera_frame(source: Image.Image, scene: int, local_frame: int) -> Image.Image:
    t = local_frame / (FPS * SHOT_SECONDS - 1)
    # A measured dolly with a slight lateral truck. Source overscan prevents edges.
    zoom = (1.035 + 0.065 * t) if scene != 1 else (1.105 - 0.05 * t)
    sw, sh = source.size
    aspect = W / H
    crop_w = sw / zoom
    crop_h = crop_w / aspect
    if crop_h > sh:
        crop_h = sh / zoom
        crop_w = crop_h * aspect
    lateral = [0.48 + 0.13 * t, 0.48 - 0.10 * t, 0.51 + 0.08 * t][scene]
    vertical = [0.43 + 0.03 * t, 0.55 - 0.04 * t, 0.49 + 0.02 * t][scene]
    x = max(0, min(sw - crop_w, (sw - crop_w) * lateral))
    y = max(0, min(sh - crop_h, (sh - crop_h) * vertical))
    return source.crop((round(x), round(y), round(x + crop_w), round(y + crop_h))).resize((W, H), Image.Resampling.LANCZOS)


def add_weather(frame: Image.Image, scene: int, global_frame: int) -> Image.Image:
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, "RGBA")
    rng = random.Random(2003 + global_frame * 7919)
    if scene == 0:
        bounds, count, alpha = (90, 75, 720, 350), 55, 25
    elif scene == 1:
        bounds, count, alpha = (0, 0, W, H), 125, 35
    else:
        bounds, count, alpha = (475, 0, W, 565), 115, 38
    x0, y0, x1, y1 = bounds
    for _ in range(count):
        x = rng.randrange(x0, x1)
        y = rng.randrange(y0, y1)
        length = rng.randrange(10, 32)
        draw.line((x, y, x - 3, min(y1, y + length)), fill=(204, 222, 232, alpha), width=1)

    if scene in (1, 2):
        # Water impacts grow and fade over several frames; no regular ripple grid.
        region = (90, 465, 1210, 700) if scene == 1 else (625, 400, 1210, 625)
        rx0, ry0, rx1, ry1 = region
        for impact_time in range(global_frame - 18, global_frame + 1, 3):
            if impact_time < 0:
                continue
            irng = random.Random(8017 + impact_time * 9973)
            for _ in range(4):
                cx, cy = irng.randrange(rx0, rx1), irng.randrange(ry0, ry1)
                age = global_frame - impact_time
                radius = 2 + age * 1.45
                opacity = round(45 * (1 - age / 20))
                if opacity > 0:
                    draw.ellipse((cx-radius, cy-radius*0.27, cx+radius, cy+radius*0.27), outline=(220, 233, 238, opacity), width=1)

    return Image.alpha_composite(frame.convert("RGBA"), layer).convert("RGB")


def main() -> None:
    images = [Image.open(path).convert("RGB") for path in SOURCES]
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    command = [ffmpeg, "-hide_banner", "-loglevel", "error", "-y",
               "-f", "rawvideo", "-pixel_format", "rgb24", "-video_size", f"{W}x{H}",
               "-framerate", str(FPS), "-i", "pipe:0", "-ss", "161.25", "-t", "18",
               "-i", str(AUDIO), "-map", "0:v:0", "-map", "1:a:0",
               "-c:v", "libx264", "-preset", "medium", "-crf", "19",
               "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
               "-movflags", "+faststart", "-shortest", str(OUTPUT)]
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    try:
        for index in range(FPS * SHOT_SECONDS * len(images)):
            scene, local = divmod(index, FPS * SHOT_SECONDS)
            frame = camera_frame(images[scene], scene, local)
            frame = add_weather(frame, scene, index)
            process.stdin.write(frame.tobytes())
    finally:
        process.stdin.close()
    if process.wait() != 0:
        raise RuntimeError("ffmpeg render failed")
    print(OUTPUT)


if __name__ == "__main__":
    main()
