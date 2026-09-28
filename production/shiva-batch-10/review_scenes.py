"""Build compact contact sheets for visual quality review of each film."""

import json
import sys
from pathlib import Path

from PIL import Image


HERE = Path(__file__).resolve().parent

for film in json.loads((HERE / "batch.json").read_text(encoding="utf-8"))["films"]:
    if len(sys.argv) > 1 and film['slug'] != sys.argv[1]:
        continue
    folder = HERE / film["slug"]
    count = len(film['sheets']) * 4
    board = Image.new("RGB", (1280, 180 * ((count + 3) // 4)))
    for i in range(count):
        name = film.get('sceneOverrides', {}).get(str(i + 1), f"S{i + 1:02d}.png")
        frame = Image.open(folder / name).convert("RGB")
        frame.thumbnail((320, 180), Image.Resampling.LANCZOS)
        board.paste(frame, ((i % 4) * 320, (i // 4) * 180))
    board.save(folder / "scene-review.jpg", quality=90)
    print(folder / "scene-review.jpg")
