import hashlib
import json
import shutil
from pathlib import Path

root = Path(__file__).resolve().parent
prod = root.parent
generated = Path(r'C:\Users\Shishyan\.codex\generated_images\01a0d9f1-201a-7c43-8034-da5f50dc1dd4')
jobs = [
    ('nenjodu_nerthal', '8KQc368hCmg', 'NENJODU_NERTHAL-CINEMATIC-v1.mp4',
     'Thiruvarutpa Nenjodu Nerthal | Full Song Film',
     generated/'exec-2e7ed9ec-1a48-4a82-8e1e-acc8ba7c9b7f.png',
     prod/'ten-more-batch/maasil'),
    ('arulvidai_vetkai', 'cVbT38ujUTQ', 'ARULVIDAI_VETKAI-CINEMATIC-v1.mp4',
     'Thiruvarutpa Arulvidai Vetkai | Full Song Film',
     generated/'exec-cbf0447a-103f-4d4b-a394-9ae280cf8aed.png',
     prod/'shiva-next-five/ulagelaam_unarndhu'),
    ('arivarum_perumai', 'VyUqD3ZO3BU', 'ARIVARUM_PERUMAI-CINEMATIC-v1.mp4',
     'Thiruvarutpa Arivarum Perumai | Full Song Film',
     generated/'exec-862339af-270d-4c0b-8b8d-6359214fcfeb.png',
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
