"""Assemble a full-length Vaan Sirappu REVIEW from v15 and image motion.

Pillow, NumPy, and imageio-ffmpeg are required. This renderer creates 20
distinct, unlooped image-based shots after 161.25 seconds of prior selected
moving footage. It does not certify the result for publication.
"""

import json
import math
import random
import subprocess
from pathlib import Path

import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
AUDIO = ROOT / "source/youtube/tX4JtRSOuxE.m4a"
PRIOR = HERE.parent / "VAAN-BATCH-REVIEW-v15.mp4"
TAIL = HERE / "VAAN-image-motion-tail-151s.mp4"
OUTPUT = HERE / "VAAN-FULL-LENGTH-IMAGE-MOTION-REVIEW-v1.mp4"
MANIFEST = HERE / "full-review-manifest.json"
W, H, FPS = 1280, 720, 24
PRIOR_FRAMES, TOTAL_FRAMES = 3870, 7501
TAIL_FRAMES = TOTAL_FRAMES - PRIOR_FRAMES
SHOTS = [
    "VS40-monsoon-valley.png", "VS41-rain-fed-paddy.png",
    "VS42-temple-tank.png", "VS43-rain-watershed.png",
    "VS44-granite-stream.png", "VS45-banana-grove.png",
    "VS46-irrigation-sluice.png", "VS47-tank-overflow.png",
    "VS48-rooted-rice.png", "VS49-mature-paddy.png",
    "VS50-sheltered-grain.png", "VS51-communal-food.png",
    "VS52-water-vessel.png", "VS54-dhoopam-burner.png",
    "VS55-lingam.png", "VS56b-gratitude-offering.png",
    "VS57-village-fields.png", "VS58-river-valley.png",
    "VS59-temple-tank-dusk.png", "VS60-living-watershed.png",
]
# Shot-local bounds for weather. The dry interiors and post-rain shots are left
# clear. Values are output-pixel coordinates and only guide atmospheric layers.
RAIN = {
    0: (80, 70, 700, 330), 1: (0, 0, 1280, 720),
    2: (560, 0, 1270, 555), 3: (540, 60, 1250, 400),
    4: (0, 0, 1280, 720), 5: (0, 0, 1280, 720),
    6: (0, 0, 1280, 720), 7: (150, 0, 1250, 500),
    8: (400, 70, 1250, 600), 10: (860, 0, 1270, 510),
    11: (730, 0, 1260, 460), 12: (250, 0, 1280, 680),
    13: (750, 0, 1270, 540), 14: (755, 0, 1140, 480),
    15: (880, 0, 1190, 470), 18: (0, 0, 1280, 600),
}
WATER = {
    1: (300, 450, 1220, 700), 2: (650, 395, 1220, 615),
    4: (280, 330, 1240, 700), 6: (270, 455, 1050, 680),
    7: (180, 430, 1190, 670), 8: (610, 465, 1230, 690),
    12: (510, 410, 1070, 690), 18: (180, 350, 1230, 690),
}


def music_cuts():
    """Pick nearby quiet instants; do not claim lyric or phrase alignment."""
    audio = subprocess.check_output([
        FFMPEG, "-loglevel", "error", "-ss", str(PRIOR_FRAMES / FPS),
        "-t", str(TAIL_FRAMES / FPS), "-i", str(AUDIO), "-ac", "1",
        "-ar", "8000", "-f", "f32le", "pipe:1",
    ])
    samples = np.frombuffer(audio, dtype="<f4")
    rms = np.zeros(TAIL_FRAMES + 1)
    for frame in range(TAIL_FRAMES + 1):
        center = int(frame * 8000 / FPS)
        block = samples[max(0, center - 650):min(len(samples), center + 650)]
        rms[frame] = math.sqrt(float(np.mean(block * block))) if len(block) else 0
    median = max(float(np.median(rms)), 1e-5)
    boundaries = [0]
    for index in range(1, len(SHOTS)):
        nominal = round(index * TAIL_FRAMES / len(SHOTS))
        candidates = range(max(boundaries[-1] + 144, nominal - 26), min(TAIL_FRAMES - (len(SHOTS) - index) * 144, nominal + 26) + 1)
        chosen = min(candidates, key=lambda f: rms[f] / median + 0.16 * abs(f - nominal) / 26)
        boundaries.append(chosen)
    boundaries.append(TAIL_FRAMES)
    return boundaries


def camera(source, scene, local, duration):
    t = local / max(duration - 1, 1)
    zoom = 1.05 + 0.06 * t if scene % 3 != 1 else 1.12 - 0.06 * t
    sw, sh = source.size
    cw = sw / zoom
    ch = cw * H / W
    if ch > sh:
        ch = sh / zoom
        cw = ch * W / H
    drift = (0.44 + 0.13 * t) if scene % 2 == 0 else (0.56 - 0.13 * t)
    x = max(0, min(sw - cw, (sw - cw) * drift))
    y = max(0, min(sh - ch, (sh - ch) * (0.45 + 0.06 * t)))
    return source.crop((round(x), round(y), round(x + cw), round(y + ch))).resize((W, H), Image.Resampling.BICUBIC)


def atmosphere(frame, scene, global_frame):
    if scene not in RAIN and scene not in WATER:
        return frame
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, "RGBA")
    if scene in RAIN:
        x0, y0, x1, y1 = RAIN[scene]
        rng = random.Random(1447 + 8831 * global_frame)
        count = 65 if scene in (0, 3, 13, 14, 15) else 115
        for _ in range(count):
            x, y = rng.randrange(x0, x1), rng.randrange(y0, y1)
            length = rng.randrange(9, 28)
            draw.line((x, y, x - 3, min(y1, y + length)), fill=(203, 221, 235, 30), width=1)
    if scene in WATER:
        x0, y0, x1, y1 = WATER[scene]
        for start in range(global_frame - 18, global_frame + 1, 4):
            if start < 0:
                continue
            rng = random.Random(5011 + start * 6917)
            for _ in range(3):
                x, y = rng.randrange(x0, x1), rng.randrange(y0, y1)
                age = global_frame - start
                radius = 2 + age * 1.3
                alpha = round(39 * (1 - age / 20))
                if alpha > 0:
                    draw.ellipse((x-radius, y-radius*0.26, x+radius, y+radius*0.26), outline=(216, 234, 239, alpha), width=1)
    return Image.alpha_composite(frame.convert("RGBA"), layer).convert("RGB")


def render_tail(boundaries):
    images = [Image.open(HERE / name).convert("RGB") for name in SHOTS]
    command = [FFMPEG, "-hide_banner", "-loglevel", "error", "-y",
               "-f", "rawvideo", "-pixel_format", "rgb24", "-video_size", f"{W}x{H}",
               "-framerate", str(FPS), "-i", "pipe:0", "-an", "-c:v", "libx264",
               "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
               "-movflags", "+faststart", str(TAIL)]
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    try:
        for scene, image in enumerate(images):
            duration = boundaries[scene + 1] - boundaries[scene]
            print(f"shot {scene+1}/{len(SHOTS)}: {SHOTS[scene]} ({duration} frames)", flush=True)
            for local in range(duration):
                frame = camera(image, scene, local, duration)
                frame = atmosphere(frame, scene, boundaries[scene] + local)
                process.stdin.write(frame.tobytes())
    finally:
        process.stdin.close()
    if process.wait() != 0:
        raise RuntimeError("Tail render failed")


def assemble():
    command = [FFMPEG, "-hide_banner", "-loglevel", "error", "-y",
               "-i", str(PRIOR), "-i", str(TAIL), "-i", str(AUDIO),
               "-filter_complex", "[1:v:0]drawtext=text='VAAN SIRAPPU - IMAGE MOTION REVIEW':x=12:y=10:fontsize=18:fontcolor=white:box=1:boxcolor=black@0.45[tail];[0:v:0][tail]concat=n=2:v=1:a=0[v]",
               "-map", "[v]", "-map", "2:a:0", "-c:v", "libx264",
               "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
               "-c:a", "copy", "-movflags", "+faststart", str(OUTPUT)]
    subprocess.run(command, check=True)


def main():
    assert all((HERE / name).is_file() for name in SHOTS)
    boundaries = music_cuts()
    entries = [dict(image=name, tailInFrame=boundaries[i], tailOutFrame=boundaries[i+1],
                    filmInFrame=PRIOR_FRAMES + boundaries[i], filmOutFrame=PRIOR_FRAMES + boundaries[i+1])
               for i, name in enumerate(SHOTS)]
    MANIFEST.write_text(json.dumps(dict(sourceAudio="tX4JtRSOuxE.m4a", priorFrames=PRIOR_FRAMES,
                                        targetFrames=TOTAL_FRAMES, cutMethod="nearby audio RMS minima, not verified lyric phrases",
                                        shots=entries), indent=2) + "\n", encoding="utf-8")
    render_tail(boundaries)
    assemble()
    print(OUTPUT)


if __name__ == "__main__":
    main()
