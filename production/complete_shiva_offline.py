"""Record verified local films and prepare their metadata for later upload."""
import datetime,hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parent
queue=json.loads((root/'SHIVA-OFFLINE-UPLOAD-QUEUE.json').read_text(encoding='utf-8'))
assert len(queue)==12 and len({r['sourceId'] for r in queue})==12
assert all(r['status']=='Ready for later upload' for r in queue)
records=[]
for row in queue:
    p=Path(row['manifest']);d=json.loads(p.read_text(encoding='utf-8'))
    assert d['localQC']['originalAudioExact'] and d['localQC']['fullDecode']
    assert d['localQC']['visualReview']!='pending'
    assert len(d['title'])<=100
    assert (p.parent/'technical-qc.txt').read_text().startswith('PASS:')
    movie=Path(row['output']);assert movie.stat().st_size>1_000_000
    with movie.open('rb') as f:digest=hashlib.file_digest(f,'sha256').hexdigest()
    records.append({**row,'description':d['description'],'playlistNames':d['playlistNames'], 'scenes':len(d['shots']),'durationSeconds':d['targetFrames']/d['fps'],'bytes':movie.stat().st_size,'sha256':digest})
checks=[]
for n in range(2,6):
    b=root/f'shiva-offline-{n:02}'
    check=json.loads((b/'uniqueness.json').read_text())
    assert check['reused']==0 and check['shots']==check['distinct']
    checks.append(check)
    films=[r for r in records if Path(r['manifest']).parent.parent==b]
    assert len(films)==3
    (b/'ready.json').write_text(json.dumps(films,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert sum(c['shots'] for c in checks)==180
report={'completedAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'films':12,'freshScenes':180,'uploadStatus':'deferred by user','totalMinutes':sum(r['durationSeconds'] for r in records)/60,'songs':records}
(root/'SHIVA-OFFLINE-COMPLETION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('COMPLETE:',report['films'],'films;',report['freshScenes'],'fresh scenes;',round(report['totalMinutes'],2),'minutes; upload deferred')
