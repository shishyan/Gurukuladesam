"""Encode full-length image-motion scenes with FFmpeg, then add ritual layers."""

import argparse
import json
import math
import os
import subprocess
from pathlib import Path

import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = Path(__file__).resolve().parent
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
FPS, W, H = 24, 1280, 720


def make_overlays():
    out = HERE / "overlays"
    out.mkdir(exist_ok=True)
    combined = out / "ritual-logo.png"
    if not combined.exists():
        ritual = Image.open(HERE / "dheepam-agarbaththi-corners.png").convert("RGBA")
        ritual = ritual.resize((W, round(ritual.height * W / ritual.width)), Image.Resampling.LANCZOS)
        ritual = ritual.crop((0, ritual.height - H, W, ritual.height))
        layer = Image.new("RGBA", (W, H))
        layer.alpha_composite(ritual.crop((0, 0, W // 2, H)), (125, 0))
        layer.alpha_composite(ritual.crop((W // 2, 0, W, H)), (W // 2, 0))
        logo = Image.open(HERE.parent / "kalvi-image-motion/channel-emblem.png").convert("RGBA")
        layer.alpha_composite(logo, (18, H - 24 - logo.height))
        layer.save(combined)
    smoke = out / "smoke"
    smoke.mkdir(exist_ok=True)
    if not (smoke / "095.png").exists():
        for f in range(96):
            t = f / 12
            img = Image.new("RGBA", (W // 2, H // 2))
            draw = ImageDraw.Draw(img)
            for origins in ((315, 350, 372, 389), (1020, 1042, 1070, 1092)):
                for strand, origin in enumerate(origins):
                    pts = []
                    for j in range(23):
                        rise = j * 5.1
                        drift = 9 * math.sin(t * .37 + j * .21 + strand * 1.8)
                        drift += 4 * math.sin(t * .19 + j * .39 + strand)
                        pts.append(((origin + drift) / 2,
                                    (H - 275 - rise - (t * 8 % 32)) / 2))
                    for j in range(len(pts) - 1):
                        opacity = round((104 - strand * 8) * (1 - j / (len(pts) - 1)) ** 1.4)
                        draw.line((pts[j], pts[j+1]), fill=(220, 222, 220, opacity), width=2)
            img = img.filter(ImageFilter.GaussianBlur(.8))
            img.save(smoke / f"{f:03d}.png")
    rain = out / "rain"
    rain.mkdir(exist_ok=True)
    if not (rain / "095.png").exists():
        for f in range(96):
            img = Image.new("RGBA", (W // 2, H // 2))
            draw = ImageDraw.Draw(img)
            for drop in range(55):
                x = (drop * 557 + f * 18) % (W + 100) - 50
                y = (drop * 313 + f * 34) % (H + 100) - 50
                draw.line((x / 2, y / 2, (x - 5) / 2, (y + 17) / 2),
                          fill=(195, 215, 235, 34), width=1)
            img.save(rain / f"{f:03d}.png")
    return combined, smoke, rain


def run(command):
    subprocess.run(command, check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest", type=Path)
    args = ap.parse_args()
    path = args.manifest.resolve()
    data = json.loads(path.read_text(encoding="utf-8"))
    folder = path.parent
    shots = data["shots"]
    assert len(shots) == 12 and len({s["image"] for s in shots}) == 12
    audio = HERE / "source" / f"{data['sourceId']}.m4a"
    raw = subprocess.check_output([FFMPEG, "-v", "error", "-i", str(audio),
                                   "-ac", "1", "-ar", "8000", "-f", "f32le", "pipe:1"])
    samples = np.frombuffer(raw, dtype="<f4")
    frames = round(len(samples) * FPS / 8000)
    cuts = [0]
    for i in range(1, 12):
        nominal = round(i * frames / 12)
        low = max(cuts[-1] + 180, nominal - 24)
        high = min(frames - (12 - i) * 180, nominal + 24)
        def score(f):
            c = round(f * 8000 / FPS)
            w = samples[max(0, c-650):min(len(samples), c+650)]
            return float(np.mean(w*w)) + .000002 * abs(f-nominal)
        cuts.append(min(range(low, high+1), key=score))
    cuts.append(frames)
    data.update({"fps": FPS, "targetFrames": frames, "imageDerived": True,
                 "cutRule": "near even spacing at low audio energy; lyric timing requires review"})
    for i, shot in enumerate(shots):
        shot.update({"inFrame": cuts[i], "outFrame": cuts[i+1]})
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

    inputs = []
    filters = []
    labels = []
    for i, shot in enumerate(shots):
        image = folder / shot["image"]
        assert image.is_file()
        inputs.extend(["-i", str(image)])
        duration = cuts[i+1] - cuts[i]
        # Small opposing push/pull and lateral drift; 12 cuts match audio valleys.
        z = "min(1.04+on*0.000035,1.085)" if i % 2 == 0 else "max(1.085-on*0.000035,1.04)"
        x = "iw/2-iw/zoom/2+on*0.015" if i % 2 == 0 else "iw/2-iw/zoom/2-on*0.015"
        filters.append(f"[{i}:v]zoompan=z='{z}':x='{x}':y='ih/2-ih/zoom/2':d={duration}:s={W}x{H}:fps={FPS},setsar=1,format=yuv420p[v{i}]")
        labels.append(f"[v{i}]")
    filters.append("".join(labels)+"concat=n=12:v=1:a=0,format=yuv420p[v]")
    base = folder / "base-motion.mp4"
    if not base.is_file() or base.stat().st_size < 1_000_000:
        run([FFMPEG, "-hide_banner", "-loglevel", "error", "-y", *inputs,
             "-filter_complex", ";".join(filters), "-map", "[v]", "-an", "-c:v", "libx264",
             "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p", str(base)])

    ritual, smoke, rain = make_overlays()
    start, end = cuts[8]/FPS, cuts[9]/FPS
    graph = "[1:v]format=rgba[rit];[0:v][rit]overlay=0:0:shortest=1[a];"
    graph += "[2:v]fps=24,scale=1280:720,format=rgba[sm];[a][sm]overlay=0:0:shortest=1[b];"
    graph += "[3:v]fps=24,scale=1280:720,format=rgba[rn];"
    graph += f"[b][rn]overlay=0:0:shortest=1:enable='between(t,{start:.3f},{end:.3f})'[c]"
    if data.get("lightningShots"):
        graph += f";[c]drawbox=x=0:y=0:w=iw:h=ih:color=white@0.08:t=fill:enable='between(t,{start+7.5:.3f},{start+7.68:.3f})'[v]"
    else:
        graph += ";[c]null[v]"
    output = folder / data["output"]
    run([FFMPEG, "-hide_banner", "-loglevel", "error", "-stats_period", "60", "-progress", "pipe:2", "-y", "-i", str(base),
         "-loop", "1", "-i", str(ritual), "-stream_loop", "-1", "-framerate", "12", "-i", str(smoke / "%03d.png"),
         "-stream_loop", "-1", "-framerate", "12", "-i", str(rain / "%03d.png"),
         "-i", str(audio), "-filter_complex", graph, "-map", "[v]", "-map", "4:a:0",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
         "-c:a", "copy", "-frames:v", str(frames), "-movflags", "+faststart", str(output)])
    # A frame-limited encode can drop the final AAC packet. Remux the entire
    # original audio after rendering so decoded audio remains bit-for-bit exact.
    complete = folder / "full-audio.mp4"
    run([FFMPEG, "-hide_banner", "-loglevel", "error", "-y", "-i", str(output),
         "-i", str(audio), "-map", "0:v:0", "-map", "1:a:0", "-c", "copy",
         "-movflags", "+faststart", str(complete)])
    os.replace(complete, output)
    print(output, flush=True)


if __name__ == "__main__":
    main()
