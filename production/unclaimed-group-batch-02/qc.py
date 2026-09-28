"""Check shot uniqueness, full decode, and original audio in a rendered film."""

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import imageio_ffmpeg


def pcm_hash(ffmpeg, path):
    raw = subprocess.check_output([
        ffmpeg, "-v", "error", "-i", str(path), "-map", "0:a:0",
        "-f", "s16le", "-acodec", "pcm_s16le", "pipe:1",
    ])
    return hashlib.sha256(raw).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("slug")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    folder = root / args.slug
    data = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
    names = [shot["image"] for shot in data["shots"]]
    assert len(names) >= 12 and len(names) == len(set(names))
    assert all((folder / name).exists() for name in names)
    video = folder / data["output"]
    audio = root / "source" / f"{data['sourceId']}.m4a"
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    assert pcm_hash(ffmpeg, audio) == pcm_hash(ffmpeg, video)
    result = subprocess.run([ffmpeg, "-v", "info", "-i", str(video), "-vf", "blackdetect=d=0.5:pix_th=0.02", "-f", "null", "NUL"],capture_output=True,text=True)
    assert result.returncode == 0
    assert "black_start:" not in result.stderr, "Unexpected black passage"
    (folder/"technical-qc.txt").write_text(f"PASS: exact original decoded audio; full decode; no black passage >=0.5 seconds; {len(names)} unique scene files.\n",encoding="utf-8")
    print(f"PASS {args.slug}: {len(names)} unique images; original audio exact; full decode; {video.stat().st_size} bytes")


if __name__ == "__main__":
    main()
