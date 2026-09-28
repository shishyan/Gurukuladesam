import json
import shutil
from pathlib import Path

root = Path(__file__).resolve().parent
prod = root.parent
gen = Path(r'C:\Users\Shishyan\.codex\generated_images\01a0d9f1-201a-7c43-8034-da5f50dc1dd4')
k = prod / 'next-five-image-motion' / 'koumaram'
m = prod / 'next-five-image-motion' / 'muthai'
c = prod / 'kaiththala-film'
n = prod / 'new-unique-batch-2' / 'naatha_vindhugal'
t = prod / 'murugar-batch-3'
films = {
 'rathinagiri_1': ('S4ogw4EfpDY', 'திருப்புகழ் 566 இரத்னகிரி I | Rathinagiri Thiruppugazh Cinematic Film', [
   gen/'exec-1abe75d6-3113-43f0-85b7-0431472e34b2.png', c/'S02.png', k/'S03.png', m/'S03.png',
   c/'S05.png', m/'S05.png', k/'S06.png', c/'S06.png', m/'S07.png', k/'S08.png',
   t/'kandhar_alangaram/S11.png', k/'S12.png']),
 'rathinagiri_2': ('bOxyDZgsI2c', 'திருப்புகழ் 566 இரத்னகிரி II | Rathinagiri Thiruppugazh Cinematic Film', [
   gen/'exec-2055c94b-4be7-45cc-9f2d-babcbeabe35e.png', k/'S11.png', c/'S04.png', m/'S04.png',
   n/'S07.png', m/'S06.png', c/'S07.png', k/'S07.png', m/'S09.png', c/'S10.png',
   m/'S11.png', c/'S12.png']),
 'seer_ulaaviya': ('iPFEtwdcIxc', 'திருப்புகழ் 712 சீர் உலாவிய | Seer Ulaaviya Cinematic Devotional Film', [
   gen/'exec-6adde674-eb3c-4f8f-994c-e550f382833f.png', m/'S03.png', c/'S02.png', k/'S03.png',
   c/'S05.png', k/'S04.png', m/'S08.png', k/'S07.png', c/'S08.png', n/'S10.png',
   m/'S11.png', m/'S12.png']),
}
for slug, (source_id, title, sources) in films.items():
    folder = root / slug
    folder.mkdir(exist_ok=True)
    shots = []
    for i, source in enumerate(sources, 1):
        if not source.is_file():
            raise FileNotFoundError(source)
        dest = folder / f'S{i:02d}.png'
        shutil.copy2(source, dest)
        shots.append({'image': dest.name, 'role': f'scene {i}'})
    manifest = {'sourceId': source_id, 'title': title,
                'output': f'{slug.upper()}-CINEMATIC-v1.mp4', 'shots': shots}
    (folder / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    print(slug, 'ready')
