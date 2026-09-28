import concurrent.futures, json, subprocess
from pathlib import Path
BASE=Path(__file__).parent
PROD=BASE.parent
items=[('vendumey_iththanaiyum','wC45ZWg05eo'),('pidiyathan_uruvumai','AuEZhvVmA90'),('anbu_maalai_ii','4zG1CdYiVxs'),('thiruvothur_pathigam','qqpvlkv0mSY'),('natarajar_pathu','89Q2g8AllcE')]
catalog={x['id']:x for x in json.loads((PROD/'playlist-audit/catalog-2026-09-26.json').read_text(encoding='utf-8'))['songs']}
used=set()
for p in PROD.rglob('manifest.json'):
 if p.is_relative_to(BASE):continue
 try:used.add(json.loads(p.read_text(encoding='utf-8')).get('sourceId',''))
 except Exception:pass
assert not used.intersection(i for s,i in items)
(BASE/'source').mkdir(exist_ok=True)
if not (BASE/'batch.json').exists():
 films=[dict(slug=s,sourceId=i,title=catalog[i]['title']+' | Cinematic Lord Shiva Devotional Film',rainShots=[10,18] if s=='natarajar_pathu' else [10],lightningShots=[18] if s=='natarajar_pathu' else ([10] if s=='thiruvothur_pathigam' else []),sheets=[f'{s}/sheet{n}.png' for n in range(1,7 if s=='natarajar_pathu' else 4)]) for s,i in items]
 (BASE/'batch.json').write_text(json.dumps({'films':films},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
else:
 films=json.loads((BASE/'batch.json').read_text(encoding='utf-8'))['films']
 assert {(f['slug'],f['sourceId']) for f in films}==set(items)
def download(t):
 i,fmt,ext=t;p=BASE/'source'/f'{i}{"-cover" if ext=="mp4" else ""}.{ext}'
 if p.exists() and p.stat().st_size>0:return i,ext,0,'Existing source retained'
 r=subprocess.run(['python','-m','yt_dlp','--quiet','--no-warnings','--no-playlist','-f',fmt,'-o',str(p),'https://www.youtube.com/watch?v='+i],capture_output=True,text=True)
 return i,ext,r.returncode,r.stderr[-160:]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 for r in pool.map(download,[(i,fmt,ext) for s,i in items for fmt,ext in [('140','m4a'),('160','mp4')]]):
  print(r,flush=True)
  if r[2]:raise RuntimeError(f'Source download failed: {r}')
r=subprocess.run(['python','-m','yt_dlp','--quiet','--no-warnings','--flat-playlist','-J','https://www.youtube.com/@guru-kula-desam/videos'],capture_output=True,text=True,encoding='utf-8')
if r.returncode:raise RuntimeError(r.stderr[-300:])
live=json.loads(r.stdout)
(BASE/'channel-title-preflight.json').write_text(json.dumps([{'id':e['id'],'title':e['title']} for e in live['entries']],ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for e in live['entries']:
 if any(k in e['title'].lower() for k in ['vendum','pidiy','anbu','thiruvoth','nataraj']):print('Possible title match',e['id'],e['title'])
