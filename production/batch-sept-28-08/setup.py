import hashlib
import json
import shutil
from pathlib import Path

root = Path(__file__).resolve().parent
prod = root.parent
generated = Path(r'C:\Users\Shishyan\.codex\generated_images\01a0d9f1-201a-7c43-8034-da5f50dc1dd4')
jobs = [
    ('arutperunjothi_iii', '3youy-33GtY', 'ARUTPERUNJOTHI_III-CINEMATIC-v1.mp4',
     'Arutperunjothi Agaval 2026 III | Full Song Film',
     generated/'exec-ec449808-7017-4fd3-888a-f2ce9eb4d1e6.png',
     prod/'ten-more-batch/maasil'),
    ('arutperunjothi_iv', 'RtHz7rTLNHk', 'ARUTPERUNJOTHI_IV-CINEMATIC-v1.mp4',
     'Arutperunjothi Agaval 2026 IV | Full Song Film',
     generated/'exec-14d719c6-711a-46e5-9000-9b7fc191d532.png',
     prod/'shiva-next-five/ulagelaam_unarndhu'),
    ('arutperunjothi_v', '-ZkM45zylxs', 'ARUTPERUNJOTHI_V-CINEMATIC-v1.mp4',
     'Arutperunjothi Agaval 2026 V | Full Song Film',
     generated/'exec-cd0de111-add6-4512-9edc-69719531c75e.png',
     prod/'ten-more-batch/tamil_thai'),
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
