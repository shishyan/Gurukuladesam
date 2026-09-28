"""Assemble three static-cover audio tracks as full-length image-motion films."""
import json
import shutil
from pathlib import Path

root = Path(__file__).resolve().parent
prod = root.parent
gen = Path(r"C:\Users\Shishyan\.codex\generated_images\01a0d9f1-201a-7c43-8034-da5f50dc1dd4")
films = {
    "naatha_vindhugal": ("C9Ea0-FfMNs", "à®¨à®¾à®¤ à®µà®¿à®¨à¯à®¤à¯à®•à®³à¯ | Naatha Vindhugal Pazhani Thiruppugazh Cinematic Devotional Film", [
        gen / "exec-ced8bece-9671-4520-9be8-a50e2562f175.png",
        prod / "next-five-image-motion/koumaram/S02.png",
        prod / "next-five-image-motion/muthai/S03.png",
        prod / "next-five-image-motion/koumaram/S04.png",
        prod / "next-five-image-motion/muthai/S05.png",
        prod / "next-five-image-motion/koumaram/S06.png",
        prod / "next-five-image-motion/muthai/S07.png",
        prod / "next-five-image-motion/koumaram/S08.png",
        prod / "next-five-image-motion/muthai/S09.png",
        prod / "next-five-image-motion/koumaram/S10.png",
        prod / "next-five-image-motion/muthai/S11.png",
        prod / "next-five-image-motion/koumaram/S12.png",
    ]),
    "abhirami": ("UUytjlINYLw", "à®…à®ªà®¿à®°à®¾à®®à®¿ à®…à®¨à¯à®¤à®¾à®¤à®¿ à®¤à¯à®¤à®¿ | Abhirami Andhathi Thuthi Cinematic Devotional Film", [
        gen / "exec-b259922a-1fe2-4c47-b21c-9d48ae683fb1.png",
        prod / "next-five-image-motion/karumari/S02.png",
        prod / "renukambal-image-motion/S03.png",
        prod / "next-five-image-motion/karumari/S04.png",
        prod / "renukambal-image-motion/S05.png",
        prod / "next-five-image-motion/karumari/S06.png",
        prod / "renukambal-image-motion/S07.png",
        prod / "next-five-image-motion/karumari/S08.png",
        prod / "renukambal-image-motion/S09.png",
        prod / "next-five-image-motion/karumari/S10.png",
        prod / "renukambal-image-motion/S11.png",
        prod / "next-five-image-motion/karumari/S12.png",
    ]),
    "annam_paalikkum": ("y7TMSgzWf8o", "à®…à®©à¯à®©à®®à¯ à®ªà®¾à®²à®¿à®•à¯à®•à¯à®®à¯ à®¤à®¿à®²à¯à®²à¯ˆ | Annam Paalikkum Thillai Cinematic Devotional Film", [
        gen / "exec-271e263b-a2bc-46b5-8c9d-bea9d40f5b4b.png",
        prod / "approved/maasil-veenaiyum/M01-imagegen-pilgrimage.png",
        prod / "next-five-image-motion/avinasi/S03.png",
        prod / "approved/maasil-veenaiyum/M05-imagegen-sanctum-threshold.png",
        prod / "ten-song-batch/thirupulambal/S05.png",
        prod / "approved/maasil-veenaiyum/M09-imagegen-moonlit-veena-strings.png",
        prod / "next-five-image-motion/avinasi/S07.png",
        prod / "approved/maasil-veenaiyum/M15-imagegen-bilva-lamp-offering.png",
        prod / "ten-song-batch/thirupulambal/S09.png",
        prod / "approved/maasil-veenaiyum/M18-imagegen-tripundra-rudraksha.png",
        prod / "approved/maasil-veenaiyum/M13-imagegen-moon-vimana.png",
        prod / "approved/maasil-veenaiyum/M22-imagegen-nandi-sanctum-axis.png",
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

