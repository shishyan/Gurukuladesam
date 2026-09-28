import json
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parent
jobs = json.loads((root/'jobs.json').read_text(encoding='utf-8'))['songs']
for job in jobs:
    slug = job['slug']
    if len(sys.argv) > 1 and slug != sys.argv[1]:
        continue
    sheets = [root/'sheets'/f'{slug}-{n}.png' for n in range(1,4)]
    title = f"திருக்குறள் - {job['chapter']} | {job['english']} Cinematic Thirukkural Film"
    output = slug.upper().replace('_','-')+'-FILM.mp4'
    subprocess.run([sys.executable,str(root/'make_storyboard.py'),'--',slug,job['sourceId'],output,title,*map(str,sheets)],check=True)
    path = root/slug/'manifest.json'
    data = json.loads(path.read_text(encoding='utf-8'))
    data.update(rainShots=[6],lightningShots=[6],publicationStatus='ready after render and QC; upload deferred')
    data['description'] = f"{job['chapter']} — {job['english']}.\n\nA cinematic image-based film for the complete original Guru Kula Desam recording, with twelve distinct scenes, gentle movement, dheepam and agarbaththi smoke, and occasional drizzle and lightning.\n\nOriginal recording: https://www.youtube.com/watch?v={job['sourceId']}\n\n#Thirukkural #TamilSong #GuruKulaDesam"
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
