"""Render one distinct-image Guru Kula Desam film from a batch manifest."""

import argparse
import json
import math
import subprocess
from pathlib import Path

import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
FPS, W, H = 12, 1280, 720


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--ritual-effects", action="store_true")
    args = parser.parse_args()
    manifest_path = args.manifest.resolve()
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    folder = manifest_path.parent
    shots = data["shots"]
    assert len(shots) >= 12, "film needs sufficient unique coverage"
    names = [shot["image"] for shot in shots]
    assert len(names) == len(set(names)), "repeated image file"
    assert all((folder / name).is_file() for name in names)
    audio = (ROOT / "source" / f"{data['sourceId']}.m4a").resolve()
    assert audio.stat().st_size > 500_000
    logo = Image.open(ROOT.parent / "kalvi-image-motion/channel-emblem.png").convert("RGBA")
    ritual = Image.open(ROOT / "dheepam-agarbaththi-corners.png").convert("RGBA") if args.ritual_effects else None
    if ritual:
        ritual = ritual.resize((W, round(ritual.height * W / ritual.width)), Image.Resampling.LANCZOS)
        ritual = ritual.crop((0, ritual.height - H, W, ritual.height))
        inset = Image.new("RGBA", (W, H))
        inset.alpha_composite(ritual.crop((0, 0, W // 2, H)), (125, 0))
        inset.alpha_composite(ritual.crop((W // 2, 0, W, H)), (W // 2, 0))
        ritual = inset
    raw = subprocess.check_output([FFMPEG, "-loglevel", "error", "-i", str(audio),
                                   "-ac", "1", "-ar", "8000", "-f", "f32le", "pipe:1"])
    samples = np.frombuffer(raw, dtype="<f4")
    frames = round(len(samples) * FPS / 8000)
    cuts = [0]
    n = len(shots)
    for i in range(1, n):
        nominal = round(i * frames / n)
        low = max(cuts[-1] + 36, nominal - 24)
        high = min(frames - (n - i) * 36, nominal + 24)
        def score(f):
            c = round(f * 8000 / FPS)
            w = samples[max(0, c - 650):min(len(samples), c + 650)]
            return float(np.mean(w * w)) + .000002 * abs(f - nominal)
        cuts.append(min(range(low, high + 1), key=score))
    cuts.append(frames)
    data["fps"] = FPS
    data["targetFrames"] = frames
    data["imageDerived"] = True
    data["cutRule"] = "near even spacing at low audio energy; lyric timing requires review"
    for i, shot in enumerate(shots):
        shot["inFrame"], shot["outFrame"] = cuts[i], cuts[i + 1]
    manifest_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    images = {name: Image.open(folder / name).convert("RGB") for name in names}
    output = folder / data["output"]
    command = [FFMPEG, "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo",
               "-pixel_format", "rgb24", "-video_size", f"{W}x{H}", "-framerate", str(FPS),
               "-i", "pipe:0", "-i", str(audio), "-map", "0:v:0", "-map", "1:a:0",
               "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
               "-c:a", "copy", "-movflags", "+faststart", str(output)]
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    try:
        for i, shot in enumerate(shots):
            source = images[shot["image"]]
            sw, sh = source.size
            duration = cuts[i + 1] - cuts[i]
            cx, cy = shot.get("center", [.5, .52])
            base = shot.get("zoom", 1.045)
            print(f"{i + 1}/{n} {shot['image']} {duration} frames", flush=True)
            for local in range(duration):
                t = local / max(duration - 1, 1)
                zoom = base + (.04 * t if i % 2 == 0 else .04 * (1 - t))
                cw = min(sw / zoom, sh * W / H / zoom)
                ch = cw * H / W
                drift = (t - .5) * .028 * sw * (1 if i % 2 == 0 else -1)
                x = min(max(cx * sw - cw / 2 + drift, 0), sw - cw)
                y = min(max(cy * sh - ch / 2, 0), sh - ch)
                frame = source.crop((round(x), round(y), round(x + cw), round(y + ch)))
                frame = frame.resize((W, H), Image.Resampling.BICUBIC)
                if ritual:
                    frame = frame.convert("RGBA")
                    frame.alpha_composite(ritual)
                    # Incense smoke drifts upward on several slow, unequal cycles.
                    mist = Image.new("RGBA", (W // 4, H // 4))
                    draw = ImageDraw.Draw(mist)
                    seconds = (cuts[i] + local) / FPS
                    for side, origins in enumerate(((315, 350, 372, 389), (1020, 1042, 1070, 1092))):
                        for strand, origin in enumerate(origins):
                            points = []
                            for j in range(22):
                                rise = j * 5.1
                                drift = 9 * math.sin(seconds * .37 + j * .21 + strand * 1.8)
                                drift += 4 * math.sin(seconds * .19 + j * .39 + strand)
                                points.append(((origin + drift) / 4,
                                               (H - 275 - rise - (seconds * 8 % 32)) / 4))
                            for j in range(len(points) - 1):
                                opacity = round((120 - strand * 8) * (1 - j / (len(points) - 1)) ** 1.4)
                                draw.line((points[j], points[j + 1]), fill=(220, 222, 220, opacity), width=2)
                    mist = mist.filter(ImageFilter.GaussianBlur(1.0)).resize((W, H), Image.Resampling.BILINEAR)
                    frame.alpha_composite(mist)
                    # Weather appears only on selected middle passages.
                    if i in data.get("rainShots", []):
                        weather = Image.new("RGBA", (W, H))
                        rain = ImageDraw.Draw(weather)
                        for drop in range(45):
                            x0 = (drop * 557 + (cuts[i] + local) * 9) % (W + 100) - 50
                            y0 = (drop * 313 + (cuts[i] + local) * 17) % (H + 100) - 50
                            rain.line((x0, y0, x0 - 5, y0 + 17), fill=(195, 215, 235, 28), width=1)
                        frame.alpha_composite(weather)
                        phase = local / FPS
                        if i in data.get("lightningShots", []) and any(abs(phase - flash) < .09 for flash in (7.5, 7.69)):
                            frame = Image.blend(frame, Image.new("RGBA", (W, H), (225, 235, 255, 255)), .12)
                    frame.paste(logo, (18, H - 24 - logo.height), logo)
                    frame = frame.convert("RGB")
                else:
                    frame.paste(logo, (24, H - 24 - logo.height), logo)
                process.stdin.write(frame.tobytes())
    finally:
        process.stdin.close()
    if process.wait() != 0:
        raise RuntimeError("FFmpeg encode failed")
    print(output)


if __name__ == "__main__":
    main()



