import glob
import json
from collections import Counter
from pathlib import Path

root = Path(__file__).resolve().parents[2]
catalog = json.loads((root/'production/playlist-audit/catalog-2026-09-26.json').read_text(encoding='utf-8'))
published = {}
for filename in glob.glob(str(root/'production/**/published.json'), recursive=True):
    try:
        data = json.loads(Path(filename).read_text(encoding='utf-8-sig'))
        for song in data if isinstance(data, list) else data.get('songs', []):
            if song.get('sourceId') and song.get('publishedUrl'):
                published[song['sourceId']] = song['publishedUrl']
    except (ValueError, AttributeError):
        pass

existing = {
    '9PUF7elNSOU': ['zPQOik79O68'],
    'Wf1Ehxt_A5s': ['coUEhVQH0Uk'],
    'Y3xujLwXuBs': ['7npbkuQwjEE'],
    'ETELjf0OTi4': ['isCeNcUwBTw'],
    'aSQrSHA4YtU': ['R82hz_s2YGQ'],
    'RDcw0Bol-cE': ['QH-xL37NmGM'],
    'xAgvuRIIl6o': ['iTALOLp7MkQ'],
    'r2ulXHQihY0': ['KFtS403RfbY', 'R8OyFbqJJEw'],
    'JDqbpISJjIA': ['KFtS403RfbY'],
    '7wJJCQrYo04': ['R8OyFbqJJEw'],
    'sHSkPTQRtH8': ['sHSkPTQRtH8'],
    'KOroiTQUE0g': ['sHSkPTQRtH8'],
    'V7dOPmD9aWg': ['GlJrQMMTRhI'],
    'OnzFNGriZ24': ['isCeNcUwBTw'],
    'tX4JtRSOuxE': ['f1jxgAbXcdE'],
    'HU-f-FpjmTQ': ['sHSkPTQRtH8'],
}
pending = {'QXhT9uoA7_w', '6ofQ9hrD1RQ'}
rows = []
for song in catalog['songs']:
    if 'Other Songs' not in song.get('playlists', []):
        continue
    sid = song['id']
    row = {'sourceId': sid, 'title': song['title']}
    if sid in published:
        row.update(status='published', films=[published[sid]])
    elif sid in existing:
        row.update(status='existing video; skip duplicate', films=['https://youtu.be/'+x for x in existing[sid]])
    elif sid in pending:
        row.update(status='rendered; daily upload limit', batch='production/batch-sept-28-10')
    else:
        row.update(status='needs audit')
    if sid == 'V7dOPmD9aWg':
        row['evidence'] = 'Decoded audio correlation with gre-26HFBfA was 1.0 at 0, 100, 500 and 1000 seconds.'
    if sid == 'r2ulXHQihY0':
        row['evidence'] = 'Combined 1104-second track is covered by existing Part 1 (840 seconds) and Part 2 (264 seconds) films.'
    rows.append(row)
out = {'playlist': 'Other Songs', 'catalogEntries': len(rows),
       'statusCounts': dict(Counter(r['status'] for r in rows)),
       'complete': False, 'remainingToPublish': sorted(pending),
       'blocker': 'YouTube daily upload limit; confirmed after Studio reload', 'songs': rows}
(root/'production/playlist-audit/other-songs-coverage-2026-09-28.json').write_text(json.dumps(out, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(out['statusCounts'])
