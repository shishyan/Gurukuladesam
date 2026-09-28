import json,sys
from pathlib import Path

root=Path(__file__).resolve().parent
if len(sys.argv)==3:
    path=root/sys.argv[1]/sys.argv[2]/'manifest.json'
    data=json.loads(path.read_text(encoding='utf-8'))
    assert (path.parent/'technical-qc.txt').exists()
    assert (path.parent/'qc-contact.png').exists()
    data['localQC']['visualReview']='opening, rainy scene and dry successor inspected'
    data['publicationStatus']='ready; upload deferred by user'
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
rows=[]
for number in range(1,6):
    batch=root/f'shiva-offline-{number:02d}'
    for job in json.loads((batch/'jobs.json').read_text(encoding='utf-8'))['songs']:
        if job.get('generationSuppressed'):continue
        path=batch/job['slug']/'manifest.json'
        data=json.loads(path.read_text(encoding='utf-8')) if path.exists() else job
        checked=data.get('localQC',{}).get('visualReview','pending')!='pending'
        rows.append({'title':data.get('title',job.get('english',job['slug'])), 'sourceId':data['sourceId'], 'status':'Ready for later upload' if checked else 'Production or QC pending', 'manifest':str(path), 'output':str(path.parent/data['output']) if 'output' in data else None, 'thumbnail':str(path.parent/'opening-qc.png') if checked else None})
assert len({r['sourceId'] for r in rows})==len(rows)
(root/'SHIVA-OFFLINE-UPLOAD-QUEUE.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lines=['# Shiva offline upload queue','', 'Uploads deferred by user. Before later upload, check live channel and drafts for duplicates; add Discography and Lord Shiva Songs, and complete YouTube checks before publication.', '', '| Film | Source | Status | Video |','| --- | --- | --- | --- |']
for row in rows:
    link=f"[MP4]({Path(row['output']).relative_to(root).as_posix()})" if row['output'] else 'Pending'
    lines.append(f"| {row['title'].replace('|','—')} | {row['sourceId']} | {row['status']} | {link} |")
lines+=['', 'Original recordings preserved. Fresh still images with camera and ritual effects; 12 scenes per film, 24 for three longer songs. Technical QC and selected frame reviews are recorded individually.']
(root/'SHIVA-OFFLINE-UPLOAD-QUEUE.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('Ready',sum(r['status']=='Ready for later upload' for r in rows),'of',len(rows))
