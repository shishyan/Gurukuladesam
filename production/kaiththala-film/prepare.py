"""Crop three generated four-frame sheets into the film's twelve scene images."""

import json
import shutil
from pathlib import Path

from PIL import Image


HERE = Path(__file__).resolve().parent
SHEETS = [
    Path(r"C:\Users\Shishyan\.codex\generated_images\01a0dccb-8645-74d1-bba1-954d6d05f31f\exec-38b7723f-5a6b-4758-a2ff-fd594488a179.png"),
    Path(r"C:\Users\Shishyan\.codex\generated_images\01a0dccb-8645-74d1-bba1-954d6d05f31f\exec-cea69c52-d425-49bf-b72d-d074f798c6f2.png"),
    Path(r"C:\Users\Shishyan\.codex\generated_images\01a0dccb-8645-74d1-bba1-954d6d05f31f\exec-0524e650-6a71-4e26-b34b-b20ef07d8659.png"),
]


def main():
    shots = []
    for group, source in enumerate(SHEETS):
        saved_sheet = HERE / f"sheet{group + 1}.png"
        if not saved_sheet.exists():
            shutil.copy2(source, saved_sheet)
        sheet = Image.open(saved_sheet).convert("RGB")
        width, height = sheet.size
        for quadrant in range(4):
            col, row = quadrant % 2, quadrant // 2
            left = col * width // 2 + (5 if col else 0)
            top = row * height // 2 + (5 if row else 0)
            right = (col + 1) * width // 2 - (5 if col == 0 else 0)
            bottom = (row + 1) * height // 2 - (5 if row == 0 else 0)
            frame = sheet.crop((left, top, right, bottom))
            frame = frame.resize((1280, 720), Image.Resampling.LANCZOS)
            name = f"S{group * 4 + quadrant + 1:02d}.png"
            frame.save(HERE / name)
            shots.append({"image": name, "role": f"scene {len(shots) + 1}"})
    (HERE / "source").mkdir(exist_ok=True)
    local_audio = HERE / "source" / "IhE1OvdIBKs.m4a"
    if not local_audio.exists():
        shutil.copy2(HERE.parent / "new-unique-batch-2" / "source" / "IhE1OvdIBKs.m4a", local_audio)
    manifest = {
        "sourceId": "IhE1OvdIBKs",
        "title": "கைத்தல நிறைகனி | Kaiththala Niraigani Cinematic Thiruppugazh Film",
        "output": "KAITHTHALA-NIRAIGANI-CINEMATIC-v1.mp4",
        "shots": shots,
    }
    (HERE / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Prepared {len(shots)} scenes")


if __name__ == "__main__":
    main()
