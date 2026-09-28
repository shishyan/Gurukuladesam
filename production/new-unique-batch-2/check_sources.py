"""Measure whether original YouTube visuals are still artwork or changing video."""
from pathlib import Path
import subprocess
import numpy as np
import imageio_ffmpeg

root = Path(__file__).resolve().parent / "source"
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
for path in sorted(root.glob("*-source.mp4")):
    raw = subprocess.check_output([ffmpeg, "-v", "error", "-i", str(path),
        "-vf", "fps=1/30,scale=64:36,format=gray", "-f", "rawvideo", "pipe:1"])
    frames = np.frombuffer(raw, dtype=np.uint8).reshape(-1, 36, 64).astype(np.int16)
    diffs = [float(np.abs(frame - frames[0]).mean()) for frame in frames]
    adj = [float(np.abs(frames[i] - frames[i-1]).mean()) for i in range(1, len(frames))]
    print(path.name, "samples", len(frames), "max_diff_to_first", round(max(diffs), 2),
          "median_adjacent_diff", round(float(np.median(adj)), 2), "diffs", [round(x,1) for x in diffs])
