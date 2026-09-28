import json, shutil, subprocess, concurrent.futures
from pathlib import Path
root=Path(__file__).parent
catalog={x['id']:x for x in json.loads((root/'playlist-audit/catalog-2026-09-26.json').read_text(encoding='utf-8'))['songs']}
for batch in ['shiva-batch-5','shiva-batch-6']:
 p=root/batch/'batch.json';d=json.loads(p.read_text(encoding='utf-8'))
 for f in d['films']:
  if '?' in f['title']:
   f['title']=catalog[f['sourceId']]['title']+' | Cinematic Lord Shiva Devotional Film'
   m=root/batch/f['slug']/'manifest.json';md=json.loads(m.read_text(encoding='utf-8'));md['title']=f['title'];m.write_text(json.dumps(md,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
dst=root/'shiva-batch-7';dst.mkdir(exist_ok=True)
for name in ['.gitignore','check_sources.py','prepare.py','review_scenes.py','render_fast.py','verify.py','dheepam-agarbaththi-corners.png']:shutil.copy2(root/'shiva-batch-6'/name,dst/name)
items=[('thiruppadai_aatchi','XB7cD-5ye-k'),('aruliyal_vinaaval','-bqKXZW8vFk'),('anbu_maalai_i','SLaW0c4zDuc'),('kuzhaitha_pathu','fdB9R7QeXo0'),('aadhi_yogeeswarar','2QOF2ycA4RQ')]
films=[dict(slug=s,sourceId=i,title=catalog[i]['title']+' | Cinematic Devotional Film',rainShots=[8],sheets=[f'{s}/sheet{n}.png' for n in range(1,4)]) for s,i in items]
(dst/'batch.json').write_text(json.dumps({'films':films},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(dst/'source').mkdir(exist_ok=True)
def download(t):
 i,fmt,ext=t;p=dst/'source'/f'{i}{"-cover" if ext=="mp4" else ""}.{ext}'
 r=subprocess.run(['python','-m','yt_dlp','--quiet','--no-warnings','--no-playlist','-f',fmt,'-o',str(p),'https://www.youtube.com/watch?v='+i],capture_output=True,text=True)
 return i,ext,r.returncode,r.stderr[-150:]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 for r in pool.map(download,[(i,fmt,ext) for s,i in items for fmt,ext in [('140','m4a'),('160','mp4')]]):print(r,flush=True)
