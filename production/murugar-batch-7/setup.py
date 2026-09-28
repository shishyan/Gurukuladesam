import hashlib
import json
import shutil
from pathlib import Path

root=Path(__file__).resolve().parent
prod=root.parent
source=root/'source'
source.mkdir(exist_ok=True)
shutil.copy2(prod/'murugar-remaining-audit/CFEYF0X6fLU.m4a',source/'CFEYF0X6fLU.m4a')
folder=root/'kandha_shashti_thuthi'
folder.mkdir(exist_ok=True)
pools=[
 prod/'murugar-batch-3/kandhar_alangaram',
 prod/'murugar-batch-4/rathinagiri_1',
 prod/'murugar-batch-4/rathinagiri_2',
 prod/'murugar-batch-4/seer_ulaaviya',
 prod/'murugar-batch-5/shanmuga_nama',
 prod/'murugar-batch-5/vaara_vazhipadu',
 prod/'murugar-batch-5/skanda_mantram_original',
 prod/'next-five-image-motion/koumaram',
 prod/'next-five-image-motion/muthai',
 prod/'kaiththala-film',
]
images=[]
hashes=set()
for index in range(1,13):
    for pool in pools:
        path=pool/f'S{index:02d}.png'
        if path.is_file():
            digest=hashlib.sha256(path.read_bytes()).hexdigest()
            if digest not in hashes:
                images.append(path)
                hashes.add(digest)
        if len(images)>=24: break
    if len(images)>=24: break
assert len(images)==24
shots=[]
for i,path in enumerate(images,1):
    dest=folder/f'S{i:02d}.png'
    shutil.copy2(path,dest)
    shots.append({'image':dest.name,'role':f'scene {i}'})
manifest={'sourceId':'CFEYF0X6fLU',
          'title':'கந்த சஷ்டி கவசம் துதி 2026 | Kandha Shashti Thuthi Cinematic Film',
          'output':'KANDHA_SHASHTI_THUTHI-CINEMATIC-v1.mp4','shots':shots}
(folder/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print('ready',len(shots))
