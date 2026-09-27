import hashlib
import json
import shutil
from pathlib import Path

root = Path(__file__).resolve().parent
prod = root.parent
generated = Path(r'C:\Users\Shishyan\.codex\generated_images\01a0d9f1-201a-7c43-8034-da5f50dc1dd4')
jobs = [
    ('aparadha_iii', 'PLBuPRdKMHE', 'APARADHA_VINNAPPAM_III-CINEMATIC-v1.mp4',
     'Thiruvarutpa Aparadha Vinnappam III Golden | Full Song Film',
     generated/'exec-9941ecd4-bc7a-400a-bff9-abd65d691979.png',
     prod/'ten-more-batch/maasil'),
    ('thiruppugazh_vilasam', 'XelTS98bLec', 'THIRUPPUGAZH_VILASAM-CINEMATIC-v1.mp4',
     'Thiruvarutpa Thiruppugazh Vilasam | Full Song Film',
     generated/'exec-eb4efef7-9540-4585-9785-f28b523b9e3c.png',
     prod/'shiva-next-five/ulagelaam_unarndhu'),
    ('arutperunjothi_ii', '00BGSFBWdlA', 'ARUTPERUNJOTHI_II-CINEMATIC-v1.mp4',
     'Arutperunjothi Agaval 2026 II | Full Song Film',
     generated/'exec-d9f49e56-cd29-482d-85e1-398d16667ebd.png',
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
