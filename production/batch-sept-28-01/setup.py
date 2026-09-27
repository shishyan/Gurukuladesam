import hashlib
import json
import shutil
from pathlib import Path

root = Path(__file__).resolve().parent
prod = root.parent
generated = Path(r'C:\Users\Shishyan\.codex\generated_images\01a0d9f1-201a-7c43-8034-da5f50dc1dd4')
jobs = [
    ('avalath_thazhungal', 'X-EB6CFVz1E', 'AVALATH_THAZHUNGAL-CINEMATIC-v1.mp4',
     'Avalath Thazhungal 2026 | Full Song Film',
     generated/'exec-721055a0-66ea-464c-a616-74a828f6b3de.png',
     prod/'ten-more-batch/maasil'),
    ('ekamaai_anthamaai', '-Gd2dy_L98c', 'EKAMAAI_ANTHAMAAI-CINEMATIC-v1.mp4',
     'Ekamaai Anthamaai | Full Song Film',
     generated/'exec-db89c6f3-e6c0-4f17-9268-c4e48e60e1fd.png',
     prod/'shiva-next-five/ulagelaam_unarndhu'),
    ('vizhiyile_malarnthathu', 'Iky5L-131A4', 'VIZHIYILE_MALARNTHATHU-REMIX-CINEMATIC-v1.mp4',
     'Vizhiyile Malarnthathu Remix 2026 | Full Song Film',
     generated/'exec-50099f8b-924a-4221-aeb0-c424879a5fe6.png',
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
