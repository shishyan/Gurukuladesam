import json,datetime
from pathlib import Path
root=Path(__file__).resolve().parent
parent=root.parent
jobs=json.loads((root/'jobs.json').read_text(encoding='utf-8'))
rows=[]
for job in jobs['songs']:
    p=root/job['slug']/'manifest.json'
    d=json.loads(p.read_text(encoding='utf-8'))
    assert d['publicationStatus']=='Published'
    rows.append(dict(sourceId=d['sourceId'],videoId=d['youtubeVideoId'],url='https://www.youtube.com/watch?v='+d['youtubeVideoId'],title=d['title'],status='Public',confirmation=d['publicationConfirmation'],checksAtPublication=d['checksAtPublication'],thumbnail='opening-qc.png',playlists=d['playlistNames'],aiDisclosure=True))
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
(root/'published.json').write_text(json.dumps(dict(verifiedAtUtc=now,count=len(rows),songs=rows),ensure_ascii=False,indent=2),encoding='utf-8')
(root/'upload-progress.json').write_text(json.dumps(dict(updatedAtUtc=now,completed=rows,pending=[]),ensure_ascii=False,indent=2),encoding='utf-8')
old=json.loads((parent/'PUBLISHED-UNCLAIMED-GROUP-FILMS.json').read_text(encoding='utf-8'))
merged={r['sourceId']:r for r in old['songs']}
merged.update({r['sourceId']:r for r in rows})
allrows=list(merged.values())
(parent/'PUBLISHED-UNCLAIMED-GROUP-FILMS.json').write_text(json.dumps(dict(verifiedAtUtc=now,count=len(allrows),songs=allrows),ensure_ascii=False,indent=2),encoding='utf-8')
md=f'# Published Guru Kula Desam films\n\n{len(allrows)} films confirmed published in YouTube Studio. Checks below describe their status at publication.\n\n'
for r in allrows:md+=f"- [{r['title']}]({r['url']}) — {r['checksAtPublication']}\n"
(parent/'PUBLISHED-UNCLAIMED-GROUP-FILMS.md').write_text(md,encoding='utf-8')
md='# Batch 09 — published\n\n'
for r in rows:md+=f"- [{r['title']}]({r['url']}) — {r['checksAtPublication']}\n"
(root/'UPLOAD-QUEUE.md').write_text(md,encoding='utf-8')
ready=json.loads((root/'ready.json').read_text(encoding='utf-8'))
ready['status']='All three films published'
for r in ready['songs']:r['status']='Published'
(root/'ready.json').write_text(json.dumps(ready,ensure_ascii=False,indent=2),encoding='utf-8')
jobs['status']='All three films published'
(root/'jobs.json').write_text(json.dumps(jobs,ensure_ascii=False,indent=2),encoding='utf-8')
print('Publication records updated:',len(allrows),'films')
