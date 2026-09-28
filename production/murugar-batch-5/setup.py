import json
import shutil
from pathlib import Path

root = Path(__file__).resolve().parent
prod = root.parent
prev = prod / 'murugar-batch-4'
three = prod / 'murugar-batch-3'
kou = prod / 'next-five-image-motion' / 'koumaram'
mut = prod / 'next-five-image-motion' / 'muthai'
kai = prod / 'kaiththala-film'
naa = prod / 'new-unique-batch-2' / 'naatha_vindhugal'
films = {
    'shanmuga_nama': ('LL77sdbmUNE', 'ஸ்ரீ சிவசண்முக நாம ஸங்கீர்த்தனம் | Siva Shanmuga Nama Sankeerthanam Cinematic Film', [
        prev/'rathinagiri_1/S01.png', kai/'S02.png', mut/'S03.png', kou/'S04.png',
        kai/'S05.png', mut/'S06.png', naa/'S07.png', kou/'S08.png',
        mut/'S09.png', kai/'S10.png', three/'kandhar_alangaram/S11.png', kou/'S12.png']),
    'vaara_vazhipadu': ('qr5jAhLRLUE', 'முருகர் வார வழிபாடு | Murugar Vaara Vazhipadu Cinematic Film', [
        prev/'rathinagiri_2/S01.png', kou/'S02.png', kai/'S03.png', mut/'S04.png',
        kou/'S05.png', kai/'S06.png', mut/'S07.png', naa/'S08.png',
        kou/'S09.png', mut/'S10.png', kai/'S11.png', mut/'S12.png']),
    'skanda_mantram_original': ('8jLZHiozGxw', 'ஸ்கந்த மந்திரம் (Original) | Skanda Mantram Cinematic Film', [
        prev/'seer_ulaaviya/S01.png', mut/'S02.png', kou/'S03.png', kai/'S04.png',
        mut/'S05.png', naa/'S06.png', kai/'S07.png', kou/'S08.png',
        mut/'S09.png', naa/'S10.png', kou/'S11.png', kai/'S12.png']),
}
for slug, (source_id, title, images) in films.items():
    folder = root / slug
    folder.mkdir(exist_ok=True)
    shots = []
    for i, path in enumerate(images, 1):
        dest = folder / f'S{i:02d}.png'
        shutil.copy2(path, dest)
        shots.append({'image': dest.name, 'role': f'scene {i}'})
    manifest = {'sourceId': source_id, 'title': title,
                'output': f'{slug.upper()}-CINEMATIC-v1.mp4', 'shots': shots}
    (folder/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    print(slug, 'ready')
