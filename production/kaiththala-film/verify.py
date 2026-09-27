"""Verify unique scenes, original audio, and full decode of the ritual film."""

import hashlib
import json
import subprocess
from pathlib import Path

import imageio_ffmpeg


HERE = Path(__file__).resolve().parent
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()


def audio_hash(path):
    payload = subprocess.check_output([
        FFMPEG, "-v", "error", "-i", str(path), "-map", "0:a:0",
        "-f", "s16le", "-acodec", "pcm_s16le", "pipe:1",
    ])
    return hashlib.sha256(payload).hexdigest()


def main():
    manifest = json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))
    scenes = [HERE / shot["image"] for shot in manifest["shots"]]
    assert len(scenes) == 12 and all(path.is_file() for path in scenes)
    assert len({hashlib.sha256(path.read_bytes()).hexdigest() for path in scenes}) == 12
    source = HERE / "source" / "IhE1OvdIBKs.m4a"
    film = HERE / "KAITHTHALA-NIRAIGANI-CINEMATIC-ritual-v2.mp4"
    assert audio_hash(source) == audio_hash(film), "original audio changed"
    subprocess.run([FFMPEG, "-v", "error", "-i", str(film), "-f", "null", "NUL"], check=True)
    print(f"PASS: 12 distinct scenes, exact decoded audio, full media decode, {film.stat().st_size} bytes")


if __name__ == "__main__":
    main()
