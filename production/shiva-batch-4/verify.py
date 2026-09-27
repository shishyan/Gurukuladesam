"""Verify the five final Shiva films against their original source audio."""

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import imageio_ffmpeg


HERE = Path(__file__).resolve().parent
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()


def audio_hash(path):
    raw = subprocess.check_output([
        FFMPEG, "-v", "error", "-i", str(path), "-map", "0:a:0",
        "-f", "s16le", "-acodec", "pcm_s16le", "pipe:1",
    ])
    return hashlib.sha256(raw).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("slug")
    args = parser.parse_args()
    folder = HERE / args.slug
    data = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
    images = [folder / shot["image"] for shot in data["shots"]]
    assert len(images) == 12 and all(image.is_file() for image in images)
    hashes = [hashlib.sha256(image.read_bytes()).hexdigest() for image in images]
    assert len(set(hashes)) == len(hashes), "repeated scene image"
    source = HERE / "source" / f"{data['sourceId']}.m4a"
    film = folder / data["output"]
    assert film.is_file()
    assert audio_hash(source) == audio_hash(film), "original audio changed"
    subprocess.run([FFMPEG, "-v", "error", "-i", str(film), "-f", "null", "NUL"], check=True)
    print(f"PASS {args.slug}: 12 distinct scenes; exact decoded audio; full media decode; {film.stat().st_size} bytes")


if __name__ == "__main__":
    main()
