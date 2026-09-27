import hashlib
import json
import shutil
from pathlib import Path

root = Path(__file__).resolve().parent
prod = root.parent
generated = Path(r'C:\Users\Shishyan\.codex\generated_images\01a0d9f1-201a-7c43-8034-da5f50dc1dd4')
jobs = [
    ('guru_bhagavan', '0gK0asNO-RM', 'GURU_BHAGAVAN_THUTHI-CINEMATIC-v1.mp4',
     'Guru Bhagavan Thuthi 2026 | Cinematic Devotional Film',
     generated/'exec-5000a51d-159c-48b5-b6af-4278149c3872.png',
     prod/'next-five-image-motion/ongi'),
    ('sani_thuthi', 'DYAKkr0e5jU', 'SANI_BHAGAVAN_THUTHI-CINEMATIC-v1.mp4',
     'Thiru Sani Bhagavan Thuthi 2026 | Cinematic Devotional Film',
     generated/'exec-edfcc55c-f8c8-4dc9-97ce-169076a15df8.png',
     prod/'new-unique-batch/arutperunjothi'),
    ('sani_pathigam', 'WMtIb1EHwGw', 'SANI_BHAGAVAN_PATHIGAM-CINEMATIC-v1.mp4',
     'Thiru Sani Bhagavan Pathigam 2026 | Cinematic Devotional Film',
     generated/'exec-c916f660-8f33-46eb-a1c8-7552c512355e.png',
     prod/'next-song-batch/aalaya_naatham'),
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
        shots.append({'image': dest.name, 'role': 'deity opening' if i == 1 else f'scene {i}'})
    manifest = {'sourceId': source_id, 'title': title, 'output': output,
                'shots': shots, 'imageDerived': True}
    (folder/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(slug, len(shots))
