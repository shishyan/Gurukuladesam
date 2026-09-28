import hashlib
import json
import shutil
from pathlib import Path

root=Path(__file__).resolve().parent
prod=root.parent
audit=prod/'murugar-remaining-audit'
source=root/'source'
sources=[
 ('kandha_sashti_kavasam','tCxe5Q1ogPc',30,
  'கந்த சஷ்டி கவசம் | Kandha Sashti Kavasam Cinematic Film'),
 ('kandha_sashti_kavasam_ii','8mzfe5h9JoY',36,
  'கந்த சஷ்டி கவசம் II | Kandha Sashti Kavasam II Cinematic Film'),
]
images=[]
seen=set()
patterns=['murugar-batch-4/*/S*.png','murugar-batch-5/*/S*.png',
          'murugar-batch-3/*/S*.png','next-five-image-motion/*/S*.png',
          'kaiththala-film/S*.png','new-unique-batch-2/naatha_vindhugal/S*.png']
for pattern in patterns:
    for path in sorted(prod.glob(pattern)):
        digest=hashlib.sha256(path.read_bytes()).hexdigest()
        if digest not in seen:
            seen.add(digest)
            images.append(path)
assert len(images)>=60
for film_idx,(slug,source_id,n,title) in enumerate(sources):
    shutil.copy2(audit/f'{source_id}.m4a',source/f'{source_id}.m4a')
    folder=root/slug
    folder.mkdir(exist_ok=True)
    order=images[15*film_idx:]+images[:15*film_idx]
    shots=[]
    for i,path in enumerate(order[:n],1):
        dest=folder/f'S{i:02d}.png'
        shutil.copy2(path,dest)
        shots.append({'image':dest.name,'role':f'scene {i}'})
    manifest={'sourceId':source_id,'title':title,
              'output':f'{slug.upper()}-CINEMATIC-v1.mp4','shots':shots}
    (folder/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    print(slug,n,'ready')
