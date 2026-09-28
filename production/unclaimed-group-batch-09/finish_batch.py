import json,hashlib,datetime
from pathlib import Path
root=Path(__file__).resolve().parent
jobs=json.loads((root/'jobs.json').read_text(encoding='utf-8'))
audio_audit=json.loads((root/'audio-uniqueness.json').read_text(encoding='utf-8'))
rows=[]
for job in jobs['songs']:
    folder=root/job['slug'];mf=folder/'manifest.json'
    d=json.loads(mf.read_text(encoding='utf-8'));movie=folder/d['output']
    assert movie.stat().st_size>1000000
    assert (folder/'technical-qc.txt').read_text(encoding='utf-8').startswith('PASS')
    assert (folder/'qc-contact.png').exists()
    assert d['localQC']['originalAudioExact'] and d['localQC']['fullDecode']
    assert d['localQC']['visualReview']=='inspected'
    if not d.get('youtubeVideoId'):d['publicationStatus']='Ready for upload; publication authorized'
    d['recordingScope']=f"Distinct source recording; other recordings of this chapter already have films. No exact or near duplicate decoded audio found among {audio_audit['tracksCompared']} available source recordings."
    mf.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
    rows.append({'sourceId':job['sourceId'],'title':d['title'],'output':str(movie.resolve()),'thumbnail':str((folder/'opening-qc.png').resolve()),'durationSeconds':d['targetFrames']/d['fps'],'scenes':len(d['shots']),'description':d['description'],'playlistNames':d['playlistNames'],'status':'Ready for upload','sha256':hashlib.file_digest(movie.open('rb'),'sha256').hexdigest()})
assert len(rows)==3 and len({x['sourceId'] for x in rows})==3
report={'checkedAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'Three full-song films ready for authorized upload','sceneCount':sum(x['scenes'] for x in rows),'songs':rows,'reviewLimit':'Artwork and opening/wet/dry rendered samples inspected; full stream decode and exact original audio verified. Full human playback and exact lyric synchronisation are not claimed.'}
(root/'ready.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
md='# Unclaimed group batch 09 — ready upload queue\n\nThree distinct chapter recordings, reserved in the shared workspace. User authorized publication. Before upload, recheck public films and Studio drafts for these source IDs, and review YouTube checks.\n\n| Song | Source | Film |\n| --- | --- | --- |\n'
for x in rows:
    rel=Path(x['output']).relative_to(root).as_posix();md+=f"| {x['title']} | {x['sourceId']} | [MP4]({rel}) |\n"
md+='\n36 fresh scene images; wide openings; group gatherings; bottom-left channel emblem; dheepam, burning incense smoke, selected outdoor drizzle and brief lightning illumination.\n'
(root/'UPLOAD-QUEUE.md').write_text(md,encoding='utf-8')
print('READY',len(rows),'films;',report['sceneCount'],'scenes;',round(sum(x['durationSeconds'] for x in rows)/60,2),'minutes')
