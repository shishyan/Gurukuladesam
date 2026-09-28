"""Assemble three distinct song films from verified source audio and visual plates."""
import json
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROD = HERE.parent
GEN = Path(r"C:\Users\Shishyan\.codex\generated_images\01a0d9f1-201a-7c43-8034-da5f50dc1dd4")

films = {
    "dhanandharum": {
        "id": "0k9CZLNA2TY", "title": "à®¤à®©à®¨à¯à®¤à®°à¯à®®à¯ à®•à®²à¯à®µà®¿à®¤à®°à¯à®®à¯ | Dhanandharum Kalvidharum Cinematic Devotional Film",
        "sources": [
            GEN / "exec-f5906b34-3fda-4aa6-9d0c-1493162e5160.png",
            PROD / "next-five-image-motion/karumari/S02.png",
            PROD / "renukambal-image-motion/S03.png",
            PROD / "next-five-image-motion/karumari/S04.png",
            PROD / "renukambal-image-motion/S05.png",
            PROD / "next-five-image-motion/karumari/S06.png",
            PROD / "renukambal-image-motion/S07.png",
            PROD / "next-five-image-motion/karumari/S08.png",
            PROD / "renukambal-image-motion/S09.png",
            PROD / "next-five-image-motion/karumari/S10.png",
            PROD / "renukambal-image-motion/S11.png",
            PROD / "next-five-image-motion/karumari/S12.png",
        ],
    },
    "thiruneetru": {
        "id": "JzGTK1V3dkM", "title": "à®¤à®¿à®°à¯à®¨à¯€à®±à¯à®±à¯à®ªà¯ à®ªà®¤à®¿à®•à®®à¯ | Thiruneetru Pathigam Cinematic Devotional Film",
        "sources": [
            GEN / "exec-5b25193b-7178-4fc3-ad74-cee837515207.png",
            PROD / "approved/maasil-veenaiyum/M18-imagegen-tripundra-rudraksha.png",
            PROD / "next-five-image-motion/avinasi/S02.png",
            PROD / "approved/maasil-veenaiyum/M22-imagegen-nandi-sanctum-axis.png",
            PROD / "next-five-image-motion/avinasi/S04.png",
            PROD / "approved/maasil-veenaiyum/M15-imagegen-bilva-lamp-offering.png",
            PROD / "next-five-image-motion/avinasi/S06.png",
            PROD / "ten-song-batch/thennadudaiya/S08.png",
            PROD / "next-five-image-motion/avinasi/S08.png",
            PROD / "ten-song-batch/vedasar/S10.png",
            PROD / "next-five-image-motion/avinasi/S10.png",
            PROD / "approved/maasil-veenaiyum/M23-imagegen-burdens-laid-down.png",
        ],
    },
    "siva_subramaniya": {
        "id": "W2peLbC20sA", "title": "à®šà®¿à®µ à®šà¯à®ªà¯à®°à®®à®£à®¿à®¯à®°à¯ à®¤à®¿à®°à¯à®µà®¿à®°à¯à®¤à¯à®¤à®®à¯ | Siva Subramaniyar Thiruvirutham Cinematic Devotional Film",
        "sources": [
            GEN / "exec-7796a0ba-31af-44a0-a2fb-d633400ca247.png",
            PROD / "next-five-image-motion/koumaram/S02.png",
            PROD / "next-five-image-motion/muthai/S03.png",
            PROD / "next-five-image-motion/koumaram/S04.png",
            PROD / "next-five-image-motion/muthai/S05.png",
            PROD / "next-five-image-motion/koumaram/S06.png",
            PROD / "next-five-image-motion/muthai/S07.png",
            PROD / "next-five-image-motion/koumaram/S08.png",
            PROD / "next-five-image-motion/muthai/S09.png",
            PROD / "next-five-image-motion/koumaram/S10.png",
            PROD / "next-five-image-motion/muthai/S11.png",
            PROD / "next-five-image-motion/koumaram/S12.png",
        ],
    },
}

for slug, film in films.items():
    folder = HERE / slug
    folder.mkdir(exist_ok=True)
    images = []
    for i, source in enumerate(film["sources"], 1):
        if not source.is_file():
            raise FileNotFoundError(source)
        dest = folder / f"S{i:02d}.png"
        shutil.copy2(source, dest)
        images.append({"image": dest.name, "role": f"scene {i}"})
    manifest = {"sourceId": film["id"], "output": f"{slug.upper()}-CINEMATIC-v1.mp4",
                "title": film["title"], "shots": images}
    (folder / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(slug, "ready")

