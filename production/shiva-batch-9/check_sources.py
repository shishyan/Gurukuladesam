"""Reject source uploads with changing picture before deriving image-motion films."""

import subprocess
from pathlib import Path

import imageio_ffmpeg
import numpy as np


FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
HERE = Path(__file__).resolve().parent


def main():
    for path in sorted((HERE / "source").glob("*-cover.mp4")):
        raw = subprocess.check_output([
            FFMPEG, "-v", "error", "-i", str(path),
            "-vf", "fps=1/30,scale=64:64,format=gray",
            "-f", "rawvideo", "pipe:1",
        ])
        frames = np.frombuffer(raw, dtype=np.uint8).reshape(-1, 64, 64).astype(np.int16)
        deviations = [float(np.abs(frame - frames[0]).mean()) for frame in frames]
        maximum = max(deviations)
        print(path.name, "samples", len(frames), "max_mean_pixel_difference", round(maximum, 2))
        if maximum > 2:
            raise ValueError(f"Changing source picture: {path}")


if __name__ == "__main__":
    main()
