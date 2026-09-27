import hashlib
import json
import shutil
from pathlib import Path

root = Path(__file__).resolve().parent
prod = root.parent
generated = Path(r'C:\Users\Shishyan\.codex\generated_images\01a0d9f1-201a-7c43-8034-da5f50dc1dd4')
jobs = [
    ('ingitha_maalai', 'kkDJM6dKTxs', 'INGITHA_MAALAI-CINEMATIC-v1.mp4',
     'Thiruvarutpa Ingitha Maalai 2026 | Full Song Film',
     generated/'exec-1342bb89-3ba5-4fe8-ba1b-b01948acb782.png',
     prod/'ten-more-batch/maasil'),
    ('thiruvarun_muraiyidu', '5gzJXgmt7AY', 'THIRUVARUN_MURAIYIDU-CINEMATIC-v1.mp4',
     'Thiruvarutpa Thiruvarun Muraiyidu | Full Song Film',
     generated/'exec-1b82e07d-c6f4-4883-8b20-668241a31d53.png',
     prod/'shiva-next-five/ulagelaam_unarndhu'),
    ('aaram_thirumurai', '4qnq1zW63hI', 'AARAM_THIRUMURAI-CINEMATIC-v1.mp4',
     'Thiruvarutpa Aaram Thirumurai | Full Song Film',
     generated/'exec-872719d5-dd6c-43f4-8a4e-f1e1866f6695.png',
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
