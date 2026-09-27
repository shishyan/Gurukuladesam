import hashlib
import json
import shutil
from pathlib import Path

root = Path(__file__).resolve().parent
prod = root.parent
generated = Path(r'C:\Users\Shishyan\.codex\generated_images\01a0d9f1-201a-7c43-8034-da5f50dc1dd4')
jobs = [
    ('indian_anthem', 'Bq6eGijG9T4', 'INDIAN_NATIONAL_ANTHEM-CINEMATIC-v1.mp4',
     'Indian National Anthem 2026 | Full Song Film',
     generated/'exec-08e1c439-80d8-4277-af7d-9d8d4f377d24.png',
     prod/'ten-more-batch/tamil_thai'),
    ('thayin_manikkodi', 'CvDDeKLC4mw', 'THAYIN_MANIKKODI-CINEMATIC-v1.mp4',
     'Thayin Manikkodi Paareer | Full Song Film',
     generated/'exec-e9fb5377-8756-4f26-a45c-8e938498b367.png',
     prod/'ten-more-batch/maasil'),
    ('vaazvathu_thamiz', 'sTSKhkPNI64', 'VAAZVATHU_THAMIZ-CINEMATIC-v1.mp4',
     'Vaazvathu Thamiz Aagattum | Full Song Film',
     generated/'exec-ea2430ef-57d2-43ca-a319-a7af6399e9e1.png',
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
