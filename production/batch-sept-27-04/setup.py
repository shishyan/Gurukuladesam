import hashlib
import json
import shutil
from pathlib import Path

root = Path(__file__).resolve().parent
prod = root.parent
generated = Path(r'C:\Users\Shishyan\.codex\generated_images\01a0d9f1-201a-7c43-8034-da5f50dc1dd4')
jobs = [
    ('ullam_oru_kovil', 'zuDJOeLjtcQ', 'ULLAM_ORU_KOVIL-CINEMATIC-v1.mp4',
     'Ullam Oru Kovil 2026 | Cinematic Devotional Film',
     generated/'exec-3cba95ec-f857-401f-acfd-c56b9fcc7dba.png',
     prod/'next-song-batch/nenjari_part1'),
    ('thamarai_malare', 'yMrpyhLlDc8', 'THAMARAI_MALARE-CINEMATIC-v1.mp4',
     'Thamarai Malare | Cinematic Devotional Film',
     generated/'exec-8614f2d8-82f5-4cfd-8394-1c38f7b72223.png',
     prod/'ten-more-batch/naal_en_seyyum'),
    ('thiruvasiyam_mantra', '1wD_X2LHCmw', 'THIRUVASIYAM_MANTRA-CINEMATIC-v1.mp4',
     'Thiruvasiyam Mantra 2026 | Cinematic Devotional Film',
     generated/'exec-d7c7f8e4-c593-44a6-a848-9529319fa457.png',
     prod/'shiva-next-five/ulagelaam_unarndhu'),
]
for slug, source_id, output, title, hero, pool in jobs:
    folder = root/slug
    folder.mkdir(exist_ok=True)
    images = [hero]
    hashes = {hashlib.sha256(hero.read_bytes()).hexdigest()}
    for path in sorted(pool.glob('S??.png')):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest not in hashes:
            images.append(path)
            hashes.add(digest)
        if len(images) == 12:
            break
    assert len(images) == 12, (slug, len(images))
    shots = []
    for i, image in enumerate(images, 1):
        dest = folder/f'S{i:02d}.png'
        shutil.copy2(image, dest)
        shots.append({'image': dest.name, 'role': 'opening' if i == 1 else f'scene {i}'})
    manifest = {'sourceId': source_id, 'title': title, 'output': output,
                'shots': shots, 'imageDerived': True}
    (folder/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(slug, len(shots))
