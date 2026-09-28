"""Compare live release tracks with exact-recording production evidence."""
import concurrent.futures, datetime, json, csv
from pathlib import Path
import yt_dlp
root=Path(__file__).resolve().parents[1]
dest=root/'playlist-audit'
albums=json.loads((dest/'audio-releases-live.json').read_text(encoding='utf-8'))['entries']
def fetch(a):
    with yt_dlp.YoutubeDL({'extract_flat':True,'quiet':True,'no_warnings':True}) as y:
        d=y.extract_info(a['url'],download=False)
    return [{'id':t['id'],'title':t.get('title'),'album':a.get('title')} for t in d.get('entries',[]) if t]
tracks={}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    for i,rows in enumerate(pool.map(fetch,albums),1):
        for r in rows:tracks.setdefault(r['id'],r)
        if i%20==0:print('Albums checked',i,flush=True)
records={}
def visit(x,f):
    if isinstance(x,list):
        for v in x:visit(v,f)
    elif isinstance(x,dict):
        sid=x.get('sourceId') or x.get('source_id') or x.get('sourceVideoId')
        if sid:records.setdefault(sid,[]).append(str(f.relative_to(root)))
        for v in x.values():
            if isinstance(v,(dict,list)):visit(v,f)
for f in root.rglob('*.json'):
    if 'playlist-audit' in f.parts:continue
    if not ('manifest' in f.name or f.name in ['jobs.json','ready.json','published.json','batch.json','publication-queue.json','release-progress.json']):continue
    try:visit(json.loads(f.read_text(encoding='utf-8-sig')),f)
    except (ValueError,OSError):pass
old={x['id']:x for x in json.loads((dest/'catalog-2026-09-26.json').read_text(encoding='utf-8'))['songs']}
variants={x['id']:x for x in json.loads((root/'CATALOG-VARIANTS-AUDIT.json').read_text(encoding='utf-8'))['songs']}
rows=[]
for sid,t in tracks.items():
    refs=sorted(set(records.get(sid,[])))
    t.update(sourceUrl='https://www.youtube.com/watch?v='+sid,productionRecords=refs,newSinceOldCatalog=sid not in old)
    film=any(s in (t['title'] or '').lower() for s in ['cinematic','full song film','music video','story film','image motion'])
    t['status']='Existing film entry (title evidence)' if film else ('Production/publication record exists' if refs else 'No exact-recording production found')
    t['compositionCoverage']=variants.get(sid,{}).get('status','Needs review')
    rows.append(t)
missing=[r for r in rows if r['status']=='No exact-recording production found']
report={'checkedAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'releaseAlbumsChecked':len(albums),'uniqueAudioTracks':len(rows),'noExactRecordingProduction':len(missing),'limitations':'A production record may be an unfinished job. Composition coverage does not prove a video uses this exact audio. Missing items require duplicate review before production.','tracks':rows}
(dest/'audio-release-video-gaps.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
with (dest/'audio-release-video-gaps.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f);w.writerow(['Song','Album','Audio link','Composition coverage','New release'])
    for r in missing:w.writerow([r['title'],r['album'],r['sourceUrl'],r['compositionCoverage'],r['newSinceOldCatalog']])
print(json.dumps({k:v for k,v in report.items() if k!='tracks'},ensure_ascii=False),flush=True)
print('New audio releases without production:',sum(r['newSinceOldCatalog'] for r in missing),flush=True)
