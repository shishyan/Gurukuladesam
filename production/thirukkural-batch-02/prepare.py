import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
GEN = Path(r'C:\Users\Shishyan\.codex\generated_images\01a0df15-42ba-7c23-9656-d0d29669ac1e')
FILMS = [
    ('pulal_unnamai', 'h2q-ADrbBc4', 'PULAL-UNNAMAI-FILM.mp4', 'திருக்குறள் - புலால் உண்ணாமை | Pulal Unnamai Cinematic Thirukkural Film', ['a02ebed3-b992-4674-b6bc-6699627342bd','c66d7c7c-1e29-4d19-bc93-250c0764a91d','5772ca39-c244-4c6b-960e-71ed4bd142a3']),
    ('thavam', 'IEk-wwY3rC8', 'THAVAM-FILM.mp4', 'திருக்குறள் - தவம் | Thavam Cinematic Thirukkural Film', ['289ffd00-b506-4d5e-9df4-d6926c729c7a','a6dcf594-3f89-48df-bb2e-21b00383f4a5','8588e8c6-a24a-4bb1-a0e7-b78de5079c89']),
    ('kooda_ozhukkam', 'mvOSVEFhvDc', 'KOODA-OZHUKKAM-FILM.mp4', 'கூடா ஒழுக்கம் (Original) | Kooda Ozhukkam Cinematic Thirukkural Film', ['ce970866-5e4f-4390-923e-50c90073ec06','83b3bb8a-7b44-4347-a7b8-0aa5e5db9ded','36cdb94e-cbde-4cbf-869d-002821431ce9']),
]
for slug, source_id, output, title, ids in FILMS:
    sheets=[]
    for i, image_id in enumerate(ids,1):
        dst=ROOT/'sheets'/f'{slug}-{i}.png'
        shutil.copyfile(GEN/f'exec-{image_id}.png',dst)
        sheets.append(str(dst))
    subprocess.run(['python',str(ROOT/'make_storyboard.py'),slug,source_id,output,title,*sheets],check=True)
    manifest=ROOT/slug/'manifest.json'
    data=json.loads(manifest.read_text(encoding='utf-8'))
    data['rainShots']=[6]
    data['lightningShots']=[6]
    manifest.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
