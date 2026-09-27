import hashlib
import json
import shutil
from pathlib import Path

root = Path(__file__).resolve().parent
prod = root.parent
generated = Path(r'C:\Users\Shishyan\.codex\generated_images\01a0d9f1-201a-7c43-8034-da5f50dc1dd4')

jobs = [
    ('vishnum_jishnum', '468ErjVLRCs', 'VISHNUM_JISHNUM-CINEMATIC-v1.mp4',
     'Vishnum Jishnum | Cinematic Devotional Film',
     generated/'exec-aa3215ed-8c4d-492a-b045-0eb820b07be9.png',
     list((prod/'next-five-image-motion/ongi').glob('S??.png'))),
    ('krishna_mantram', 'izHLRwITs_Q', 'KRISHNA_MANTRAM-CINEMATIC-v1.mp4',
     'Krishna Mantram I | Cinematic Devotional Film',
     generated/'exec-077d2efa-e9c4-42ea-a9fa-0429a66dcb56.png',
     list((prod/'approved/thiruppavai1').glob('*.png'))),
    ('anjaneyar_thuthi', '7NECOtuTZ_Y', 'ANJANEYAR_THUTHI-CINEMATIC-v1.mp4',
     'Anjaneyar Thuthi | Cinematic Devotional Film',
     generated/'exec-030540db-281c-443c-9e1f-e8e8bd61bf7f.png',
     list((prod/'new-unique-batch/rama_rama').glob('S??.png'))),
]
for slug, source_id, output, title, hero, pool in jobs:
    folder = root/slug
    folder.mkdir(exist_ok=True)
    images = [hero]
    hashes = {hashlib.sha256(hero.read_bytes()).hexdigest()}
    for path in sorted(pool):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest not in hashes:
            images.append(path)
            hashes.add(digest)
        if len(images) == 12:
            break
    assert len(images) == 12, (slug, len(images))
    shots = []
    for index, path in enumerate(images, 1):
        dest = folder/f'S{index:02d}.png'
        shutil.copy2(path, dest)
        shots.append({'image': dest.name, 'role': 'deity opening' if index == 1 else f'scene {index}'})
    manifest = {'sourceId': source_id, 'title': title, 'output': output,
                'shots': shots, 'imageDerived': True}
    (folder/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(slug, len(shots))
