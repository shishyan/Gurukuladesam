import concurrent.futures, json, shutil, subprocess
from pathlib import Path
prod = Path(__file__).resolve().parent.parent
base = prod / 'shiva-batch-9'
base.mkdir(exist_ok=True)
items = [('thennadudaiya_female','vZyHNMkm8xU'),('thiruvothur_v','oOGRP4cqGP8'),('thiruppadai_hiphop','tW9-r0H5rx8'),('namasivaya_children','aq0j2OMVNoU'),('kuzhaitha_pathu_ii','jsFIjA8ZOkw')]
catalog = {s['id']:s for s in json.loads((prod/'playlist-audit/catalog-2026-09-26.json').read_text(encoding='utf-8'))['songs']}
for path in prod.rglob('manifest.json'):
    if base in path.parents: continue
    try: data=json.loads(path.read_text(encoding='utf-8-sig'))
    except (ValueError,OSError): continue
    assert data.get('sourceId') not in {sid for slug,sid in items}, str(path)
for name in ['.gitignore','prepare.py','render_fast.py','review_scenes.py','check_sources.py','check_audio_unique.py','dheepam-agarbaththi-corners.png']:
    if not (base/name).exists(): shutil.copy2(prod/'shiva-batch-8'/name,base/name)
films=[dict(slug=slug,sourceId=sid,title=(catalog[sid].get('release') or catalog[sid]['title'])+' | Cinematic Shiva Film',rainShots=[10],lightningShots=[10] if slug=='kuzhaitha_pathu_ii' else [],sheets=[f'{slug}/sheet{n}.png' for n in range(1,4)]) for slug,sid in items]
if not (base/'batch.json').exists():
    (base/'batch.json').write_text(json.dumps({'films':films},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
else:
    saved=json.loads((base/'batch.json').read_text(encoding='utf-8'))['films']
    assert {(f['slug'],f['sourceId']) for f in saved} == set(items)
(base/'source').mkdir(exist_ok=True)
def download(task):
    sid,fmt,ext=task; dest=base/'source'/f'{sid}{"-cover" if ext=="mp4" else ""}.{ext}'
    if dest.exists(): return sid,ext,'retained'
    r=subprocess.run(['python','-m','yt_dlp','--quiet','--no-warnings','--no-playlist','-f',fmt,'-o',str(dest),'https://www.youtube.com/watch?v='+sid],capture_output=True,text=True)
    assert r.returncode==0, r.stderr[-300:]
    return sid,ext,'downloaded'
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    for result in pool.map(download,[(sid,fmt,ext) for slug,sid in items for fmt,ext in [('140','m4a'),('160','mp4')]]): print(result,flush=True)
