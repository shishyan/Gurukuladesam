import json
import shutil
from pathlib import Path

root = Path(__file__).resolve().parent
prod = root.parent
b4, b5 = prod/'murugar-batch-4', prod/'murugar-batch-5'
kou, mut = prod/'next-five-image-motion/koumaram', prod/'next-five-image-motion/muthai'
kai, naa = prod/'kaiththala-film', prod/'new-unique-batch-2/naatha_vindhugal'
films = {
    'magaram_original': ('qRqkS1Kf8lA', 'மகரம் அளறு இடை (Original) | Magaram Alaru Idai Cinematic Film', [
        b5/'vaara_vazhipadu/S01.png', kou/'S03.png', kai/'S04.png', mut/'S05.png',
        naa/'S06.png', kou/'S07.png', kai/'S08.png', mut/'S09.png',
        naa/'S10.png', kou/'S11.png', kai/'S12.png', mut/'S12.png']),
    'magaram_remix': ('cEIEecb51Fc', 'மகரம் அளறு இடை (Remix) | Magaram Alaru Idai Cinematic Film', [
        b4/'rathinagiri_2/S01.png', mut/'S02.png', kai/'S03.png', kou/'S04.png',
        naa/'S05.png', mut/'S06.png', kou/'S07.png', kai/'S08.png',
        mut/'S09.png', naa/'S10.png', kou/'S11.png', kai/'S12.png']),
    'skanda_symphony': ('N8MOVChJwPQ', 'ஸ்கந்த மந்திரம் (Symphony) | Skanda Mantram Cinematic Film', [
        b5/'skanda_mantram_original/S01.png', kai/'S02.png', mut/'S03.png', kou/'S04.png',
        naa/'S05.png', kai/'S06.png', mut/'S07.png', kou/'S08.png',
        kai/'S09.png', mut/'S10.png', naa/'S11.png', kou/'S12.png']),
}
for slug, (source_id, title, images) in films.items():
    folder = root/slug
    folder.mkdir(exist_ok=True)
    shots=[]
    for i, path in enumerate(images,1):
        dest=folder/f'S{i:02d}.png'
        shutil.copy2(path,dest)
        shots.append({'image':dest.name,'role':f'scene {i}'})
    manifest={'sourceId':source_id,'title':title,'output':f'{slug.upper()}-CINEMATIC-v1.mp4','shots':shots}
    (folder/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    print(slug,'ready')
