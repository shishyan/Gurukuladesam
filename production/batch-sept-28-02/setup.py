import hashlib
import json
import shutil
from pathlib import Path

root = Path(__file__).resolve().parent
prod = root.parent
generated = Path(r'C:\Users\Shishyan\.codex\generated_images\01a0d9f1-201a-7c43-8034-da5f50dc1dd4')
jobs = [
    ('ulagamelan', 'QTxWZpg6F98', 'ULAGAMELAN_CINEMATIC-v1.mp4',
     'Ulagamelan Thaniniraindha | Full Song Film',
     generated/'exec-9cf46b9b-ee74-4fc0-a12e-6c3b0afc86c2.png',
     prod/'ten-more-batch/maasil'),
    ('samsaram_veenai', '28Xnfhctf0I', 'SAMSARAM_ENBATHU_VEENAI-REMIX-CINEMATIC-v1.mp4',
     'Samsaram Enbathu Veenai Remix 2026 | Full Song Film',
     generated/'exec-7c5ff19c-1e31-49dc-8ff6-6a7b03f9ef80.png',
     prod/'ten-more-batch/tamil_thai'),
    ('koiyilakanal', 'G4Tk8Z1tKRg', 'KOIYILAKANAL-CINEMATIC-v1.mp4',
     'Koiyilakanal 2026 | Full Song Film',
     generated/'exec-27eb3572-ed9c-42ec-8bb9-4b2f5e2a9b6a.png',
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
