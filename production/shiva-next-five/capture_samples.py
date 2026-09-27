"""Extract one representative frame per completed film for visual review."""

import json
import subprocess
from pathlib import Path

import imageio_ffmpeg


HERE = Path(__file__).resolve().parent
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()


def main():
    films = json.loads((HERE / "batch.json").read_text(encoding="utf-8"))["films"]
    for film in films:
        folder = HERE / film["slug"]
        manifest = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
        source = folder / manifest["output"].replace("-v1.mp4", "-ritual-v2.mp4")
        if not source.is_file():
            continue
        index = film["rainShots"][0] - 1 if film["rainShots"] else 4
        shot = manifest["shots"][index]
        seconds = (shot["inFrame"] + shot["outFrame"]) / (2 * manifest["fps"])
        destination = folder / "review.jpg"
        subprocess.run([
            FFMPEG, "-y", "-v", "error", "-ss", str(seconds), "-i", str(source),
            "-frames:v", "1", str(destination),
        ], check=True)
        print(destination)


if __name__ == "__main__":
    main()
