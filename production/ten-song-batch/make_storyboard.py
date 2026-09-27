"""Split three unique four-scene image sheets into one film manifest."""

import argparse
import json
from pathlib import Path

from PIL import Image


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("slug")
    parser.add_argument("source_id")
    parser.add_argument("output")
    parser.add_argument("title")
    parser.add_argument("sheets", nargs=3, type=Path)
    args = parser.parse_args()
    folder = Path(__file__).resolve().parent / args.slug
    folder.mkdir(exist_ok=True)
    shots = []
    for sheet_number, path in enumerate(args.sheets):
        with Image.open(path) as image:
            image = image.convert("RGB")
            width, height = image.size
            for panel in range(4):
                col, row = panel % 2, panel // 2
                x0, y0 = col * (width // 2), row * (height // 2)
                x1 = width if col else width // 2
                y1 = height if row else height // 2
                name = f"S{sheet_number * 4 + panel + 1:02d}.png"
                image.crop((x0, y0, x1, y1)).save(folder / name)
                shots.append({"image": name, "role": f"scene {len(shots) + 1}"})
    manifest = {
        "sourceId": args.source_id,
        "output": args.output,
        "title": args.title,
        "shots": shots,
    }
    (folder / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(folder / "manifest.json")


if __name__ == "__main__":
    main()
