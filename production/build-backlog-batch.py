"""Build a batch from four new narrative frames and relevant existing scene assets."""
import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path
from PIL import Image

PRODUCTION = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('batch', type=Path)
args = parser.parse_args()
root = args.batch.resolve()
config = json.loads((root/'jobs.json').read_text(encoding='utf-8'))
live = json.loads((PRODUCTION/'channel-live-backlog-2026-09-28.json').read_text(encoding='utf-8'))
assets = json.loads((root/'generated-assets.json').read_text(encoding='utf-8'))
for job in config['songs']:
    slug = job['slug']
    if slug not in assets:
        continue
    folder = root/slug
    folder.mkdir(exist_ok=True)
    if (folder/'manifest.json').exists():
        continue
    matches = [s for s in live['entries'] if (job['chapter'] in s['title'] or
               re.search(r'\b'+re.escape(job['english'])+r'\b',s['title'],re.I)) and
               any(w in s['title'].lower() for w in ['film','cinematic','full music video'])]
    assert not matches, matches
    sheet = root/'sheets'/f'{slug}.png'
    sheet.parent.mkdir(exist_ok=True)
    shutil.copy2(assets[slug],sheet)
    im = Image.open(sheet).convert('RGB')
    w,h = im.size
    opening = []
    for i in range(4):
        x,y = i%2,i//2
        part = folder/f'new-{i+1}.png'
        im.crop((round(x*w/2)+3,round(y*h/2)+3,round((x+1)*w/2)-3,round((y+1)*h/2)-3)).save(part)
        opening.append(part)
    supporting = [PRODUCTION/p for p in job['supportingImages']]
    assert len(supporting) == 8
    sequence = [opening[0],*supporting[:2],opening[1],*supporting[2:5],opening[2],*supporting[5:],opening[3]]
    hashes = [hashlib.sha256(p.read_bytes()).hexdigest() for p in sequence]
    assert len(sequence) == len(set(hashes)) == 12
    shots = []
    for i, original in enumerate(sequence,1):
        name = f'S{i:02d}.png'
        shutil.copy2(original,folder/name)
        shots.append({'image':name,'role':f'narrative scene {i}',
                      'artOrigin':'new generated chapter scene' if original in opening else 'existing relevant scene library',
                      'assetSource':str(original.relative_to(PRODUCTION))})
    data = {'sourceId':job['sourceId'],'title':f"திருக்குறள் - {job['chapter']} | {job['english']} | Full Song Film",
            'output':slug.upper()+'-CINEMATIC-v1.mp4','shots':shots,'imageDerived':True,
            'theme':job['theme'],'duplicateAudit':{'publicVideosChecked':len(live['entries']),'matchingFilms':matches},
            'publicationStatus':'pending YouTube daily upload quota'}
    (folder/'manifest.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(slug,'12 scenes',flush=True)
