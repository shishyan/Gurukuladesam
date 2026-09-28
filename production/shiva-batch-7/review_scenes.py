"""Build compact contact sheets for visual quality review of each film."""

import json
from pathlib import Path

from PIL import Image


HERE = Path(__file__).resolve().parent

for film in json.loads((HERE / "batch.json").read_text(encoding="utf-8"))["films"]:
    folder = HERE / film["slug"]
    board = Image.new("RGB", (1280, 540))
    for i in range(12):
        frame = Image.open(folder / f"S{i + 1:02d}.png").convert("RGB")
        frame.thumbnail((320, 180), Image.Resampling.LANCZOS)
        board.paste(frame, ((i % 4) * 320, (i // 4) * 180))
    board.save(folder / "scene-review.jpg", quality=90)
    print(folder / "scene-review.jpg")
