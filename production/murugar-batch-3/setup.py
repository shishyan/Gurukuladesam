"""Prepare three Lord Murugar full-song image-motion films."""
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
films = {
    'kandhar_alangaram': ('ZZKjQ1SD_mQ', 'கந்தர் அலங்காரம் 2026 | Kandhar Alangaram Cinematic Devotional Film', [
        gen / 'exec-cdcd2837-5234-4f51-af5c-8355835ad750.png',
        m / 'S02.png', k / 'S04.png', c / 'S04.png', m / 'S07.png',
        k / 'S06.png', c / 'S06.png', m / 'S08.png', k / 'S09.png',
        c / 'S10.png', m / 'S11.png', c / 'S12.png',
    ]),
    'arumugam': ('jpCBad1MjgI', 'ஆறுமுகம் ஆறுமுகம் | Arumugam Arumugam Cinematic Devotional Film', [
        gen / 'exec-dc318162-982c-4a95-91e5-d81fd1dcc499.png',
        m / 'S07.png', n / 'S03.png', c / 'S02.png', k / 'S05.png',
        c / 'S07.png', k / 'S07.png', m / 'S09.png', n / 'S08.png',
        c / 'S09.png', c / 'S11.png', k / 'S12.png',
    ]),
    'uruvaai_aruvaai': ('XqDL5bZgW9c', 'உருவாய் அருவாய் | Uruvaai Aruvaai Kandhar Anubhudhi Cinematic Devotional Film', [
        gen / 'exec-a4955c20-932c-44e7-b2bb-e58a9d558ae8.png',
        k / 'S01.png', c / 'S05.png', m / 'S03.png', k / 'S03.png',
        c / 'S06.png', m / 'S06.png', n / 'S07.png', m / 'S04.png',
        c / 'S10.png', n / 'S11.png', m / 'S12.png',
    ]),
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
