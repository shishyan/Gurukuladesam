import hashlib
import json
import shutil
from pathlib import Path

root = Path(__file__).resolve().parent
prod = root.parent
generated = Path(r'C:\Users\Shishyan\.codex\generated_images\01a0d9f1-201a-7c43-8034-da5f50dc1dd4')
jobs = [
    ('arutperunjothi_vi', 'gre-26HFBfA', 'ARUTPERUNJOTHI_VI-CINEMATIC-v1.mp4',
     'Arutperunjothi 2026 VI | Full Song Film',
     generated/'exec-fab49e7c-864f-4ca5-8603-859ddf33dd8f.png',
     prod/'shiva-next-five/ulagelaam_unarndhu'),
    ('arutperunjothi_agaval_i', 'UxsU284RHQY', 'ARUTPERUNJOTHI_AGAVAL_I-CINEMATIC-v1.mp4',
     'Arutperunjothi Agaval I | Full Song Film',
     generated/'exec-ad7f3487-7e30-4074-bef4-9b2c8d306b96.png',
     prod/'ten-more-batch/maasil'),
    ('arutperunjothi_agaval_ii', '1W9SHSo-2Vk', 'ARUTPERUNJOTHI_AGAVAL_II-CINEMATIC-v1.mp4',
     'Arutperunjothi Agaval II | Full Song Film',
     generated/'exec-6600c6cf-36a6-49e3-8ddb-6aac31058b76.png',
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
