"""Assemble twelve different storyboard scenes for each pending full song film."""
import json
import shutil
import re
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent
JOBS = [
    ('avaiyarithal', '9mOpq9daQVs', 'அவையறிதல்', 'Avaiyarithal'),
    ('arivudaimai', 'FkQqysk6vmE', 'அறிவுடைமை', 'Arivudaimai'),
    ('aalvinaiyudaimai', 'um09tyT-2p0', 'ஆள்வினையுடைமை', 'Aalvinaiyudaimai'),
]

def main():
    assets = json.loads((ROOT/'generated-assets.json').read_text(encoding='utf-8'))
    live = json.loads((ROOT.parent/'channel-live-backlog-2026-09-28.json').read_text(encoding='utf-8'))
    for slug, sid, tamil, english in JOBS:
        if slug not in assets:
            continue
        matches = [s for s in live['entries'] if tamil in s['title'] or re.search(r'\b'+re.escape(english)+r'\b', s['title'], re.I)]
        # The selected catalog recordings are audio releases; any other matching film blocks production.
        films = [s for s in matches if s['id'] != sid and any(w in s['title'].lower() for w in ['film', 'cinematic', 'video'])]
        assert not films, films
        folder = ROOT/slug
        folder.mkdir(exist_ok=True)
        if (folder/'manifest.json').exists():
            continue
        shots = []
        for sheet_index, original in enumerate(assets[slug]):
            sheet = ROOT/'sheets'/f'{slug}-{sheet_index+1}.png'
            sheet.parent.mkdir(exist_ok=True)
            shutil.copy2(original, sheet)
            im = Image.open(sheet).convert('RGB')
            w, h = im.size
            for panel in range(4):
                x, y = panel%2, panel//2
                # Remove the shared seam while preserving the four distinct original panels.
                box = (round(x*w/2)+3, round(y*h/2)+3,
                       round((x+1)*w/2)-3, round((y+1)*h/2)-3)
                name = f'S{len(shots)+1:02d}.png'
                im.crop(box).save(folder/name)
                shots.append({'image': name, 'role': f'narrative scene {len(shots)+1}'})
        assert len(shots) == 12
        title = f'திருக்குறள் - {tamil} | {english} | Full Song Film'
        manifest = {'sourceId': sid, 'title': title, 'output': slug.upper()+'-CINEMATIC-v1.mp4',
                    'shots': shots, 'imageDerived': True,
                    'duplicateAudit': {'publicVideosChecked': len(live['entries']), 'matchingFilms': films},
                    'publicationStatus': 'pending YouTube daily upload quota'}
        (folder/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
        print(slug, len(shots), flush=True)

if __name__ == '__main__':
    main()
