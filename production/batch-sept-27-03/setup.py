import hashlib
import json
import shutil
from pathlib import Path

root = Path(__file__).resolve().parent
prod = root.parent
generated = Path(r'C:\Users\Shishyan\.codex\generated_images\01a0d9f1-201a-7c43-8034-da5f50dc1dd4')
jobs = [
    ('konrai_vendhan', 'MDK8Oq7p1j8', 'KONRAI_VENDHAN-CINEMATIC-v1.mp4',
     'Konrai Vendhan | Cinematic Devotional Film',
     generated/'exec-dba3689d-fa1b-46cb-99e1-e7094c266c31.png',
     prod/'ten-more-batch/inna_seidharai'),
    ('anbe_saranam', 'lw2nEZfR7Kc', 'ANBE_SARANAM-CINEMATIC-v1.mp4',
     'Anbe Saranam Arule Saranam | Cinematic Devotional Film',
     generated/'exec-c7ee6e66-fe22-4881-88da-cb2f07536dd5.png',
     prod/'shiva-next-five/anandha_maalai'),
    ('arul_nama_vilakkam', 'ZsxGP1jIZ-s', 'ARUL_NAMA_VILAKKAM-CINEMATIC-v1.mp4',
     'Arul Nama Vilakkam | Cinematic Devotional Film',
     generated/'exec-a21aba5c-c303-4ef8-84f0-1cf8901a8e73.png',
     prod/'next-song-batch/tunjalum'),
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
