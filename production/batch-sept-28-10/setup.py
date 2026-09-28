import hashlib
import json
import shutil
from pathlib import Path

root = Path(__file__).resolve().parent
prod = root.parent
generated = Path(r'C:\Users\Shishyan\.codex\generated_images\01a0d9f1-201a-7c43-8034-da5f50dc1dd4')
jobs = [
    ('agara_muthala', 'QXhT9uoA7_w', 'AGARA_MUTHALA-CINEMATIC-v1.mp4',
     'Thirukkural Agara Muthala | Full Song Film',
     generated/'exec-b18159fb-d3c8-4153-81ba-03af2d6cbb72.png',
     prod/'thirukkural-batch-01/kadavul_vazhthu'),
    ('vaazkkai_thunai', '6ofQ9hrD1RQ', 'VAAZKKAI_THUNAI-CINEMATIC-v1.mp4',
     'Thirukkural Vaazkkai Thunai | Full Song Film',
     generated/'exec-50fe3098-c8be-4234-a43f-880493302693.png',
     prod/'thirukkural-batch-01/ilvazhkkai'),
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
