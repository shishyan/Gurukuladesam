"""Copy generated contact sheets and source audio, then split into a manifest."""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
GEN = Path(r"C:\Users\Shishyan\.codex\generated_images\01a0df15-42ba-7c23-9656-d0d29669ac1e")
OLD_SOURCE = ROOT.parent / "ten-song-batch" / "source"

p = argparse.ArgumentParser()
p.add_argument("slug")
p.add_argument("source_id")
p.add_argument("output")
p.add_argument("title")
p.add_argument("images", nargs=3)
a = p.parse_args()
folder = ROOT / a.slug
folder.mkdir(exist_ok=True)
audio = ROOT / "source" / f"{a.source_id}.m4a"
if not audio.exists():
    shutil.copy2(OLD_SOURCE / audio.name, audio)
sheets = []
for i, name in enumerate(a.images, 1):
    target = folder / f"sheet{i}.png"
    shutil.copy2(GEN / name, target)
    sheets.append(str(target))
subprocess.run([sys.executable, str(ROOT / "make_storyboard.py"), a.slug,
                a.source_id, a.output, a.title, *sheets], check=True)
