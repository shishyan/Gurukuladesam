"""Record only QC-passed full films that are still awaiting publication."""
import json
from pathlib import Path

P = Path(__file__).resolve().parent
entries = []
batch10 = json.loads((P/'batch-sept-28-10/ready.json').read_text(encoding='utf-8'))
for row in batch10['songs']:
    if not row.get('publishedUrl'):
        folder = P/'batch-sept-28-10'/row['slug']
        manifest = json.loads((folder/'manifest.json').read_text(encoding='utf-8'))
        entries.append({'sourceId':row['sourceId'],'title':row['title'],
                        'file':str((folder/manifest['output']).relative_to(P)),
                        'googleVids':row['googleVids'],'status':'ready; pending upload quota'})
for ready in sorted(P.glob('thirukkural-backlog-*/ready.json')):
    data = json.loads(ready.read_text(encoding='utf-8'))
    for row in data['songs']:
        if not row.get('publishedUrl'):
            film = ready.parent/row['file']
            assert film.exists()
            entries.append({'sourceId':row['sourceId'],'title':row['title'],
                            'file':str(film.relative_to(P)), 'googleVids':row.get('googleVids'),
                            'status':'ready; pending upload quota','qc':row['qc']})
assert len(entries) == len({r['sourceId'] for r in entries})
out = {'channel':'@guru-kula-desam','pendingCount':len(entries),'blocker':'YouTube daily upload limit',
       'releaseInstructions':'Recheck public channel for duplicates, import locally finished films into Google Vids, publish through the correct channel Studio, and verify public URLs. Scheduling requires the upload to succeed first.',
       'songs':entries}
(P/'publication-queue.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('QC-passed pending films:',len(entries))
