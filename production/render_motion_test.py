"""Render a short motion/atmosphere proof without touching Batch 02 previews.

The old preview renderer drives zoompan at delivery resolution.  zoompan rounds
its crop origin to whole source pixels, so a very slow pan repeatedly sticks and
jumps by one pixel.  This proof renders motion at 2x and downsamples, uses a
cosine ease, and builds restrained rain and incense haze procedurally.
"""
from __future__ import annotations

import subprocess
import argparse
from pathlib import Path

import imageio_ffmpeg


ROOT = Path(__file__).resolve().parents[1]
FFMPEG = Path(imageio_ffmpeg.get_ffmpeg_exe())
DEFAULT_IMAGE = ROOT / "production" / "visuals" / "thiruppavai1" / "01-street.png"
DEFAULT_OUTPUT = ROOT / "renders" / "tests" / "fluid-motion-rain-dhoopam-proof.mp4"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", type=Path, default=DEFAULT_IMAGE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--rain-opacity", type=float, default=0.075,
        help="Rain overlay opacity (0 disables rain for dry interiors).",
    )
    args = parser.parse_args()
    image = args.image.resolve()
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    frames = 12 * 24
    ease = f"(0.5-0.5*cos(PI*on/{frames - 1}))"
    graph = (
        # Oversampling makes zoompan's integer crop steps sub-pixel at delivery.
        f"[0:v]scale=2688:1512:force_original_aspect_ratio=increase,"
        f"crop=2688:1512,zoompan=z='1+0.035*{ease}':"
        f"x='iw/2-iw/zoom/2+18*{ease}':"
        f"y='ih/2-ih/zoom/2-10*{ease}':d=1:s=2560x1440:fps=24,"
        "scale=1280:720:flags=lanczos,format=yuv420p[base];"
        # Soft, warm Perlin haze: slow upward drift, confined to lower frame.
        "[1:v]format=gray,scroll=v=-0.0015,gblur=sigma=24,"
        "lut='val*0.60',format=yuv420p,colorchannelmixer=rr=1.10:gg=0.95:bb=0.78[smoke];"
        "[base][smoke]blend=all_mode=screen:all_opacity=0.10[atmo];"
        # Fine rain texture, vertically elongated and kept subtle.
        "[2:v]format=gray,scale=320:720,gblur=sigma=0.5:steps=1,"
        "lut='if(gte(val,205),255,0)',scroll=v=0.075,"
        "scale=1280:720:flags=bilinear,format=yuv420p[rain];"
        f"[atmo][rain]blend=all_mode=screen:all_opacity={args.rain_opacity},"
        "eq=saturation=0.96:contrast=1.015,format=yuv420p[out]"
    )
    command = [
        str(FFMPEG), "-y",
        "-loop", "1", "-framerate", "24", "-t", "12", "-i", str(image),
        "-f", "lavfi", "-i",
        "perlin=s=1280x720:r=24:octaves=5:persistence=0.55:"
        "xscale=0.006:yscale=0.010:tscale=0.10:random_mode=seed:seed=71",
        "-f", "lavfi", "-i",
        "perlin=s=80x720:r=24:octaves=2:persistence=0.35:"
        "xscale=0.12:yscale=0.012:tscale=2.2:random_mode=seed:seed=29",
        "-filter_complex", graph, "-map", "[out]", "-t", "12", "-an",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        "-r", "24", "-movflags", "+faststart", str(output),
    ]
    subprocess.run(command, check=True)
    print(output)


if __name__ == "__main__":
    main()
