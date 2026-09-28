"""Choose one uncovered recording per chapter, avoiding existing song films."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
P = ROOT/'production'
catalog = json.loads((P/'playlist-audit/catalog-2026-09-26.json').read_text(encoding='utf-8'))
live = json.loads((P/'channel-live-backlog-2026-09-28.json').read_text(encoding='utf-8'))

def chapter(title):
    text = title.split('|')[0].split('(')[0].strip()
    text = re.sub(r'^திருக்குறள்\s*[–—-]?\s*', '', text)
    text = re.sub(r'\b2026\b', '', text)
    return re.sub(r'\s+', ' ', text).strip()

covered = {}
for entry in live['entries']:
    if any(x in entry['title'].lower() for x in ['film','cinematic','full music video']):
        covered[chapter(entry['title'])] = {'status':'existing public film','id':entry['id']}
for path in P.rglob('manifest.json'):
    try:
        m = json.loads(path.read_text(encoding='utf-8-sig'))
    except (ValueError, OSError):
        continue
    if m.get('sourceId'):
        song = next((s for s in catalog['songs'] if s['id'] == m['sourceId']), None)
        if song:
            covered.setdefault(chapter(song['title']), {'status':'local production exists','manifest':str(path.relative_to(ROOT))})

groups = {}
known_covered_ids = set()
other_audit = P/'playlist-audit/other-songs-coverage-2026-09-28.json'
if other_audit.exists():
    other = json.loads(other_audit.read_text(encoding='utf-8'))
    for row in other.get('songs', other.get('entries', [])):
        if row.get('status') in ['published','existing video; skip duplicate']:
            known_covered_ids.add(row['sourceId'])
for song in catalog['songs']:
    if any('Master Collection' in x for x in song['playlists']):
        groups.setdefault(chapter(song['title']), []).append(song)
rows = []
for name, songs in groups.items():
    if any(s['id'] in known_covered_ids for s in songs):
        rows.append({'chapter':name,'recordings':[s['id'] for s in songs],'status':'covered by Other Songs film audit'})
    elif name in covered:
        rows.append({'chapter':name,'recordings':[s['id'] for s in songs],**covered[name]})
    elif 'Hans Zimmer' in name:
        rows.append({'chapter':name,'recordings':[s['id'] for s in songs],'status':'outside devotional scope'})
    else:
        preferred = next((s for s in songs if '(Original)' in s['title']), songs[0])
        rows.append({'chapter':name,'recordings':[s['id'] for s in songs],'status':'needs production',
                     'sourceId':preferred['id'],'sourceTitle':preferred['title']})

out = {'playlist':'Thirukkural Master Collection','publicVideosChecked':len(live['entries']),
       'rule':'One uncovered chapter recording per film; do not create another film for a chapter already filmed.',
       'chapters':rows}
(P/'playlist-audit/thirukkural-backlog-audit.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('chapters',len(rows),'remaining',sum(r['status']=='needs production' for r in rows))
for row in rows:
    if row['status']=='needs production':
        print(row['sourceId'],row['sourceTitle'])
