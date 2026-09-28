"""Inventory all public channel surfaces and cross-reference production evidence."""
import json, csv, datetime, concurrent.futures, collections, re
from pathlib import Path
import yt_dlp

root=Path(__file__).resolve().parents[1]
dest=root/'playlist-audit'
base='https://www.youtube.com/@guru-kula-desam'
errors=[]
def fetch(url):
    try:
        with yt_dlp.YoutubeDL({'extract_flat':True,'quiet':True,'no_warnings':True,'skip_download':True}) as y:
            d=y.extract_info(url,download=False)
        return {'url':url,'id':d.get('id'),'title':d.get('title'),'reportedCount':d.get('playlist_count'),
                'entries':[{'id':x.get('id'),'title':x.get('title'),'url':x.get('url'),'duration':x.get('duration'),'channelId':x.get('channel_id'),'availability':x.get('availability')} for x in d.get('entries',[]) if x]}
    except Exception as e:
        errors.append({'url':url,'error':str(e)})
        return {'url':url,'entries':[],'error':str(e)}
surfaces=['videos','shorts','streams','releases','playlists']
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    tabs=dict(zip(surfaces,pool.map(fetch,[base+'/'+s for s in surfaces])))
print('Channel tabs fetched', {k:len(v['entries']) for k,v in tabs.items()},flush=True)
def details(entry):
    url=entry['url']
    d=fetch(url)
    d['name']=entry['title'];return d
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    playlists=list(pool.map(details,tabs['playlists']['entries']))
    releases=list(pool.map(details,tabs['releases']['entries']))
print('All playlists and albums fetched',flush=True)
items={}
def add(x,surface):
    sid=x['id']
    if not sid:return
    r=items.setdefault(sid,{**x,'memberships':[]})
    if surface not in r['memberships']:r['memberships'].append(surface)
for s in ['videos','shorts','streams']:
    for x in tabs[s]['entries']:add(x,s)
for p in playlists:
    for x in p['entries']:add(x,'playlist:'+p['name'])
for p in releases:
    for x in p['entries']:add(x,'release:'+p['name'])
records={}
def visit(x,f):
    if isinstance(x,dict):
        sid=x.get('sourceId') or x.get('source_id') or x.get('sourceVideoId')
        if sid:
            ev={'file':str(f.relative_to(root)),'status':x.get('status') or x.get('publicationStatus')}
            urls=[x.get(k) for k in ['publishedUrl','youtubeUrl','uploadedUrl'] if x.get(k)]
            if urls:ev['filmUrls']=urls
            out=x.get('output') or x.get('outputFile') or x.get('videoPath')
            if isinstance(out,str):
                for candidate in [f.parent/out,root/out,Path(out)]:
                    if candidate.is_file() and candidate.stat().st_size>1000000:
                        ev['localFilm']=str(candidate.resolve());break
            records.setdefault(sid,[]).append(ev)
        for v in x.values():
            if isinstance(v,(dict,list)):visit(v,f)
    elif isinstance(x,list):
        for v in x:visit(v,f)
for f in root.rglob('*.json'):
    if 'playlist-audit' in f.parts:continue
    if not ('manifest' in f.name or f.name in ['ready.json','jobs.json','published.json','batch.json','release-progress.json','publication-queue.json']):continue
    try:visit(json.loads(f.read_text(encoding='utf-8-sig')),f)
    except (OSError,ValueError):pass
variants={x['id']:x for x in json.loads((root/'CATALOG-VARIANTS-AUDIT.json').read_text(encoding='utf-8'))['songs']}
coverage={x['id']:x for x in json.loads((dest/'audio-release-video-gaps.json').read_text(encoding='utf-8'))['tracks']}
filmkeys=['cinematic','full song film','music video','story film','story version','image motion']
for sid,r in items.items():
    refs=records.get(sid,[])
    linked=[]
    for e in refs:
        for url in e.get('filmUrls',[]):
            m=re.search(r'(?:v=|youtu.be/)([\w-]{11})',url)
            if m and m[1] in items:linked.append(m[1])
    r['productionEvidence']=refs
    r['publicFilmIds']=sorted(set(linked))
    r['compositionCoverage']=coverage.get(sid,{}).get('compositionCoverage') or variants.get(sid,{}).get('status')
    for url in re.findall(r'https://(?:youtu.be/|www.youtube.com/watch\?v=)[\w-]{11}',r['compositionCoverage'] or ''):
        m=re.search(r'(?:v=|youtu.be/)([\w-]{11})',url)
        if m and m[1] in items:linked.append(m[1])
    r['publicFilmIds']=sorted(set(linked))
    if any(k in (r['title'] or '').lower() for k in filmkeys):r['auditStatus']='Public film entry (title evidence)'
    elif linked:r['auditStatus']='Source linked to publicly listed film'
    elif any(e.get('localFilm') for e in refs):r['auditStatus']='Local film exists; public link needs verification'
    elif refs:r['auditStatus']='Production record only; completion needs verification'
    elif r['compositionCoverage'] and r['compositionCoverage']!='Needs review':r['auditStatus']='Composition coverage recorded; exact version not verified'
    else:r['auditStatus']='Needs investigation'
publicIds={x['id'] for s in ['videos','shorts','streams'] for x in tabs[s]['entries']}
playlistIds={x['id'] for p in playlists for x in p['entries']}
unlisted=sorted(publicIds-playlistIds)
report={'checkedAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'channel':base,
        'surfaceCounts':{k:len(v['entries']) for k,v in tabs.items()},'uniqueContentIds':len(items),
        'auditCounts':dict(collections.Counter(r['auditStatus'] for r in items.values())),
        'publicUploadsOutsidePlaylists':unlisted,'errors':errors,'tabs':tabs,'playlists':playlists,'releases':releases,'content':list(items.values()),
        'limitations':'Public inventory does not expose private, draft, scheduled or unlisted-only uploads. Title evidence is not playback verification. Production jobs are not completed films. Composition coverage is not proof of exact recording coverage.'}
(dest/'complete-channel-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
with (dest/'complete-channel-audit.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f);w.writerow(['ID','Title','URL','Audit status','Composition coverage','Public film IDs','Memberships'])
    for r in items.values():w.writerow([r['id'],r['title'],'https://www.youtube.com/watch?v='+r['id'],r['auditStatus'],r['compositionCoverage'],'; '.join(r['publicFilmIds']),'; '.join(r['memberships'])])
lines=['# Complete public channel audit','', 'Checked: '+report['checkedAtUtc'],'','## Channel surfaces','', '| Surface | Entries |','| --- | ---: |']
lines += [f'| {k} | {v} |' for k,v in report['surfaceCounts'].items()]
lines += ['', '## Public playlists','','| Playlist | Entries | Unique IDs |','| --- | ---: | ---: |']
lines += [f"| {p['name']} | {len(p['entries'])} | {len({x['id'] for x in p['entries']})} |" for p in playlists]
lines += ['',f"Unique content IDs across all surfaces: **{len(items)}**. Public uploads outside named playlists: **{len(unlisted)}**.",'','## Evidence status','']
lines += [f'- {k}: {v}' for k,v in report['auditCounts'].items()]
lines += ['', '## Limits','',report['limitations'],'',f'Fetch errors: {len(errors)}.']
(dest/'COMPLETE-CHANNEL-AUDIT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ['tabs','playlists','releases','content']},ensure_ascii=True),flush=True)
