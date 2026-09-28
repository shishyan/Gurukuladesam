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
    process = subprocess.Popen([
        FFMPEG, "-v", "error", "-i", str(path), "-map", "0:a:0",
        "-f", "s16le", "-acodec", "pcm_s16le", "pipe:1",
    ], stdout=subprocess.PIPE)
    digest = hashlib.sha256()
    for chunk in iter(lambda: process.stdout.read(1048576), b''):
        digest.update(chunk)
    assert process.wait() == 0
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("slug")
    args = parser.parse_args()
    folder = HERE / args.slug
    data = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
    images = [folder / shot["image"] for shot in data["shots"]]
    expected = 24 if args.slug == 'natarajar_pathu' else 12
    assert len(images) == expected and all(image.is_file() for image in images)
    hashes = [hashlib.sha256(image.read_bytes()).hexdigest() for image in images]
    assert len(set(hashes)) == len(hashes), "repeated scene image"
    source = HERE / "source" / f"{data['sourceId']}.m4a"
    film = folder / data["output"]
    assert film.is_file()
    assert audio_hash(source) == audio_hash(film), "original audio changed"
    decoded = subprocess.run([FFMPEG, "-hide_banner", "-i", str(film), "-vf", "blackdetect=d=2:pix_th=0.05:pic_th=0.98", "-f", "null", "NUL"], check=True, capture_output=True, text=True)
    assert 'black_start:' not in decoded.stderr, 'long black passage detected'
    print(f"PASS {args.slug}: {expected} distinct scenes; exact decoded audio; full media decode; no long black passages; {film.stat().st_size} bytes")


if __name__ == "__main__":
    main()
