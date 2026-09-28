import json,re,sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from collections import Counter
root=Path(__file__).resolve().parent
catalog=json.loads((root/'playlist-audit/catalog-2026-09-26.json').read_text(encoding='utf-8'))
covered={};reserved=set()
for path in root.rglob('*.json'):
    if path.name not in ('manifest.json','jobs.json','published.json','review-manifest.json'):
        continue
    try: data=json.loads(path.read_text(encoding='utf-8-sig'))
    except (ValueError,OSError):continue
    rows=data if isinstance(data,list) else data.get('songs',[data])
    for row in rows:
        if not isinstance(row,dict):continue
        sid=row.get('sourceId') or row.get('source_id') or row.get('sourceVideoId')
        if sid:
            if path.name=='jobs.json':reserved.add(sid)
            else:covered.setdefault(sid,[]).append(str(path.relative_to(root)))
other=json.loads((root/'playlist-audit/other-songs-coverage-2026-09-28.json').read_text(encoding='utf-8'))
for row in other.get('songs',[]):
    if row['status']!='needs audit': covered.setdefault(row['sourceId'],[]).append('Other Songs coverage audit')
remaining=[s for s in catalog['songs'] if s['id'] not in covered and s['id'] not in reserved]
out={'catalogSongs':len(catalog['songs']),'coveredSourceIds':len(covered),'reservedSourceIds':len(reserved),'remaining':remaining}
(root/'REMAINING-CATALOG-AUDIT.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Remaining',len(remaining));print(Counter(p for s in remaining for p in s['playlists']))
for s in remaining:print(s['id'],s['title'],' / '.join(s['playlists']))
