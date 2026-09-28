"""Prepare verified static-cover songs as three themed image-motion films."""
import json
import shutil
from pathlib import Path

root = Path(__file__).resolve().parent
prod = root.parent
gen = Path(r"C:\Users\Shishyan\.codex\generated_images\01a0d9f1-201a-7c43-8034-da5f50dc1dd4")
films = {
    "rama_rama": ("jfXxy-Y9zuA", "à®‡à®°à®¾à®® à®°à®¾à®® à®°à®¾à®® à®¹à®°à¯‡ à®¹à®°à¯‡ | Rama Rama Rama Hare Hare Cinematic Devotional Film", [
        gen / "exec-a513b5d3-fd08-47e8-9e7c-25f68dae241d.png",
        prod / "approved/namo-narayanam/N07-imagegen-rama-bow.png",
        prod / "approved/namo-narayanam/N14-imagegen-garuda-banner.png",
        prod / "next-five-image-motion/ongi/S03.png",
        prod / "approved/namo-narayanam/N16-imagegen-tulsi-conch-water.png",
        prod / "next-five-image-motion/ongi/S05.png",
        prod / "approved/namo-narayanam/N13-imagegen-vishnu-lakshmi.png",
        prod / "next-five-image-motion/ongi/S07.png",
        prod / "thiruppavai1-image-motion/TG03-nine-devotees-walk.png",
        prod / "next-five-image-motion/ongi/S09.png",
        prod / "approved/namo-narayanam/N01-imagegen-four-emblems.png",
        prod / "next-five-image-motion/ongi/S11.png",
    ]),
    "maha_ganesha": ("zqStqzcFgbM", "à®®à®•à®¾ à®•à®£à¯‡à®š à®ªà®žà¯à®šà®°à®¤à¯à®©à®®à¯ | Maha Ganesha Pancharatnam Cinematic Devotional Film", [
        gen / "exec-6169d986-34b0-4514-80cc-a8d5cc684c1b.png",
        prod / "gananatha-om/GN02-temple-exterior.png",
        prod / "gananatha-om/GN03-temple-bell.png",
        prod / "gananatha-om/GN04-offerings.png",
        prod / "gananatha-om/GN05-mouse-vahana.png",
        prod / "gananatha-om/GN06-lamp-corridor.png",
        prod / "gananatha-om/GN07-banyan-garden.png",
        prod / "gananatha-om/GN08-temple-tank.png",
        prod / "gananatha-om/GN09-garland.png",
        prod / "gananatha-om/GN11-incense.png",
        prod / "gananatha-om/GN12-sunrise-courtyard.png",
        prod / "gananatha-om/GN13-lotus-tank.png",
    ]),
    "arutperunjothi": ("9PUF7elNSOU", "à®…à®°à¯à®Ÿà¯à®ªà¯†à®°à¯à®žà¯à®šà¯‹à®¤à®¿ 2026 | Arutperunjothi Cinematic Devotional Film", [
        gen / "exec-99186e73-1998-4d78-a6f4-fab141840a5e.png",
        prod / "next-five-image-motion/avinasi/S01.png",
        prod / "approved/maasil-veenaiyum/M05-imagegen-sanctum-threshold.png",
        prod / "next-five-image-motion/avinasi/S03.png",
        prod / "approved/maasil-veenaiyum/M11-imagegen-breeze-bells-corridor.png",
        prod / "next-five-image-motion/avinasi/S05.png",
        prod / "approved/maasil-veenaiyum/M12-imagegen-grace-footlight.png",
        prod / "next-five-image-motion/avinasi/S07.png",
        prod / "approved/maasil-veenaiyum/M21-imagegen-sunrise-departure.png",
        prod / "next-five-image-motion/avinasi/S09.png",
        prod / "approved/maasil-veenaiyum/M23-imagegen-burdens-laid-down.png",
        prod / "approved/maasil-veenaiyum/M16-imagegen-overhead-pilgrimage.png",
    ]),
}
for slug, (source_id, title, sources) in films.items():
    folder = root / slug
    folder.mkdir(exist_ok=True)
    shots = []
    for i, source in enumerate(sources, 1):
        if not source.is_file():
            raise FileNotFoundError(source)
        dest = folder / f"S{i:02d}.png"
        shutil.copy2(source, dest)
        shots.append({"image": dest.name, "role": f"scene {i}"})
    manifest = {"sourceId": source_id, "title": title,
                "output": f"{slug.upper()}-CINEMATIC-v1.mp4", "shots": shots}
    (folder / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(slug, "ready")

