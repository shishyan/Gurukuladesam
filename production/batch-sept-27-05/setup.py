import hashlib
import json
import shutil
from pathlib import Path

root = Path(__file__).resolve().parent
prod = root.parent
generated = Path(r'C:\Users\Shishyan\.codex\generated_images\01a0d9f1-201a-7c43-8034-da5f50dc1dd4')
jobs = [
    ('ullam_oru_kovil_ii', 'x8x7cnUdTE4', 'ULLAM_ORU_KOVIL_II-CINEMATIC-v1.mp4',
     'Ullam Oru Kovil II 2026 | Full Song Film',
     generated/'exec-42222ab7-a170-4872-a7e9-c995f244ae4d.png',
     prod/'ten-more-batch/nenjari_part2'),
    ('sorpperu_meygnana', 'tAlN-7BPL7k', 'SORPPERU_MEYGNANA-CINEMATIC-v1.mp4',
     'Sorpperu Meygnana | Full Song Film',
     generated/'exec-d67dbae0-2e33-4ba5-95a9-7978d7c1e873.png',
     prod/'ten-more-batch/porai'),
    ('gnanath_thiruvadi', '6p5A87HdAAI', 'GNANATH_THIRUVADI-CINEMATIC-v1.mp4',
     'Gnanath Thiruvadi 2026 | Full Song Film',
     generated/'exec-721b73de-2958-4fc9-8b3a-2d18a854b8f9.png',
     prod/'ten-more-batch/thiruvaiyaaru'),
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
