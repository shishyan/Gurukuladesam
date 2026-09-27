"""Crop saved imagegen contact sheets into twelve independent film scenes."""

import argparse
import json
import shutil
from pathlib import Path

from PIL import Image


HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("slug")
    args = parser.parse_args()
    films = json.loads((HERE / "batch.json").read_text(encoding="utf-8"))["films"]
    film = next(f for f in films if f["slug"] == args.slug)
    if len(film["sheets"]) != 3:
        raise ValueError("Three four-frame contact sheets required")
    folder = HERE / film["slug"]
    folder.mkdir(exist_ok=True)
    shots = []
    for group, image_path in enumerate(film["sheets"]):
        local_sheet = folder / f"sheet{group + 1}.png"
        if not local_sheet.is_file():
            shutil.copy2(image_path, local_sheet)
        sheet = Image.open(local_sheet).convert("RGB")
        width, height = sheet.size
        for quad in range(4):
            col, row = quad % 2, quad // 2
            left = col * width // 2 + (5 if col else 0)
            top = row * height // 2 + (5 if row else 0)
            right = (col + 1) * width // 2 - (5 if col == 0 else 0)
            bottom = (row + 1) * height // 2 - (5 if row == 0 else 0)
            scene = sheet.crop((left, top, right, bottom))
            scene = scene.resize((1280, 720), Image.Resampling.LANCZOS)
            name = f"S{len(shots) + 1:02d}.png"
            scene.save(folder / name)
            shots.append({"image": name, "role": f"scene {len(shots) + 1}"})
    manifest = {
        "sourceId": film["sourceId"], "title": film["title"],
        "output": film["slug"].upper() + "-CINEMATIC-v1.mp4",
        "rainShots": film["rainShots"], "shots": shots,
    }
    (folder / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Prepared {film['slug']}: {len(shots)} scenes")


if __name__ == "__main__":
    main()
