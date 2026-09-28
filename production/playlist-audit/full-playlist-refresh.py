"""Read every public channel playlist and cross-check every entry, not a preview."""
import json, datetime, concurrent.futures
from pathlib import Path
from collections import Counter
import yt_dlp

root = Path(__file__).resolve().parents[1]
options = {'extract_flat': True, 'skip_download': True, 'quiet': True, 'no_warnings': True}
def fetch(url):
    with yt_dlp.YoutubeDL(options) as ydl:
        return ydl.extract_info(url, download=False)

previous = json.loads((root/'playlist-audit/next-batch-refresh-2026-09-28.json').read_text(encoding='utf-8'))
listed = fetch('https://www.youtube.com/@guru-kula-desam/playlists')
inventory = {x['id']: x.get('title', x['id']) for x in listed.get('entries', []) if x}
for p in previous['playlists']:
    inventory.setdefault(p['id'], p['name'])

evidence = {}
for path in root.rglob('*.json'):
    if path.name not in ('manifest.json','jobs.json','published.json','review-manifest.json'):
        continue
    try: data = json.loads(path.read_text(encoding='utf-8-sig'))
    except (ValueError,OSError): continue
    rows = data if isinstance(data,list) else data.get('songs',[data])
    for row in rows:
        if not isinstance(row,dict): continue
        sid = row.get('sourceId') or row.get('source_id') or row.get('sourceVideoId')
        if sid:
            evidence.setdefault(sid,[]).append({'file':str(path.relative_to(root)),
                'status':row.get('publicationStatus') or row.get('status') or ('production job' if path.name=='jobs.json' else 'production record')})
variants = {x['id']:x for x in json.loads((root/'CATALOG-VARIANTS-AUDIT.json').read_text(encoding='utf-8'))['songs']}
other = {x['sourceId']:x for x in json.loads((root/'playlist-audit/other-songs-coverage-2026-09-28.json').read_text(encoding='utf-8'))['songs'] if x['status']!='needs audit'}
uploads = {}
for x in json.loads((root/'release-progress.json').read_text(encoding='utf-8')).get('acceptedUploads',[]):
    uploads[x['url'].split('v=')[-1]] = x

def audit(item):
    pid,name = item
    d = fetch('https://www.youtube.com/playlist?list='+pid)
    rows = []
    for x in d.get('entries',[]):
        if not x: continue
        sid,title = x['id'],x.get('title') or '[Unavailable entry]'
        r = {'id':sid,'title':title}
        if sid in uploads:
            r.update(classification='film already built and accepted for upload',evidence=uploads[sid])
        elif sid == '0TB3drCSvNc':
            r.update(classification='same composition as completed Thiruvarul Vetkai film',evidence='SHIVA-OFFLINE-OWNERSHIP.md; thiruvarutpa-backlog-02 (dbdp19C0j3M)')
        elif any(k in title.lower() for k in ['cinematic','full song film','music video','story film','story version','image motion','new cinematic']):
            r.update(classification='existing film entry')
        elif sid in evidence:
            r.update(classification='production record exists; inspect readiness if needed',evidence=evidence[sid])
        elif sid in variants:
            r.update(classification=variants[sid]['status'],evidence=variants[sid].get('evidence'))
        elif sid in other:
            r.update(classification=other[sid]['status'],evidence=other[sid])
        else:
            r.update(classification='needs investigation')
        rows.append(r)
    print(name,len(rows),'entries',sum(r['classification']=='needs investigation' for r in rows),'unresolved',flush=True)
    return {'id':pid,'name':name,'entryCount':len(rows),'statusCounts':dict(Counter(r['classification'] for r in rows)),'entries':rows}

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    playlists = list(pool.map(audit,inventory.items()))
unresolved = {}
for p in playlists:
    for r in p['entries']:
        if r['classification']=='needs investigation':
            unresolved.setdefault(r['id'],{**r,'playlists':[]})['playlists'].append(p['name'])
report = {'checkedAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'publicChannelPlaylistCount':len(listed.get('entries',[])), 'playlists':playlists,
    'unresolved':list(unresolved.values())}
(root/'playlist-audit/full-playlist-refresh-2026-09-28.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('Unresolved:',json.dumps(report['unresolved'],ensure_ascii=False),flush=True)
