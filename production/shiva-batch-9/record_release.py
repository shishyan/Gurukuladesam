import json
from pathlib import Path
here=Path(__file__).resolve().parent
films=json.loads((here/'batch.json').read_text(encoding='utf-8'))['films']
qc=(here/'QC.txt').read_text(encoding='utf-8-sig')
assert qc.count('PASS ')==5
metadata=json.loads((here/'youtube-metadata.json').read_text(encoding='utf-8'))
queue=json.loads((here.parent/'shiva-batch-8/publication-queue.json').read_text(encoding='utf-8'))
queue['scope']='Pending Shiva films from batches 6 through 9; other production queues are separate'
ids={f['sourceId'] for f in films}
conflicts=[]
for path in here.parent.rglob('manifest.json'):
    if here in path.parents:continue
    try: d=json.loads(path.read_text(encoding='utf-8-sig'))
    except (ValueError,OSError):continue
    if d.get('sourceId') in ids:conflicts.append(str(path))
assert not conflicts,conflicts
for row in metadata:
    row['status']='Ready; pending upload quota'
    row['qc']={'uniqueScenes':12,'exactDecodedAudio':True,'fullDecodePassed':True,'noLongBlackPassages':True,'finishedWeatherReviewed':True}
    queue['songs'].append(row)
queue['pendingCount']=len(queue['songs'])
(here/'publication-queue.json').write_text(json.dumps(queue,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(here/'youtube-metadata.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
report={'selectedSourceIds':sorted(ids),'conflictingProductionManifests':conflicts,'livePlaylistEntries':132,'newCatalogEntries':0,'rejectedExactDuplicate':{'sourceId':'xc1iNs05Bkw','existingSourceId':'o5PVED0ZcfU'},'audioTracksCompared':70,'publicTitleReview':'Existing Thennadudaiya film Z9GnvOMjDjU uses mb-lljpUJ5g; the female recording is distinct. Other selected version titles have no matching public film in the refreshed channel list. Check Studio again before uploading.'}
(here/'pre-push-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
text='# Lord Shiva films — batch 9\n\nFive distinct alternate recordings, clearly labeled by version. No new compositions were found in the refreshed Shiva playlist. Thiruvenba (hiphop) was rejected because its decoded audio exactly matched the completed Thiruvenba recording.\n\n'
text+='Built-in imagegen artwork: 60 distinct scenes, with contact sheets and prompt set saved here. Full original audio is preserved. Lower-left emblem, paired dheepam, four agarbaththi per side, rising white-grey smoke, outdoor drizzle and occasional brief illumination. Children’s courtyard rain is confined to the exposed right-hand area so the covered veranda and people remain dry.\n\n'
text+='All five passed exact decoded-audio, full media decode, distinct-scene and long black passage checks. Scene contact sheets and finished dry/wet frames were visually reviewed. Cut placement follows low audio energy near scene intervals; detailed lyric-by-lyric musical editing is not claimed.\n\n'
text+='| Film | Original | Status |\n|---|---|---|\n'
for f in films:text+=f"| {f['title'].replace('|','/')} | [Recording](https://youtu.be/{f['sourceId']}) | Ready locally |\n"
text+='\nNo batch 9 film has been uploaded or published. The latest verified quota block is recorded in batch 8; upload later after a fresh draft/public-film duplicate check, with both Discography and Lord Shiva Songs selected and realistic AI visuals disclosed.\n'
(here/'RELEASES.md').write_text(text,encoding='utf-8')
for p in here.glob('*render.log'):
    raw=p.read_bytes()
    if raw.startswith(b'\xff\xfe'):p.write_text(raw.decode('utf-16'),encoding='utf-8')
print('Release records ready for five films; scoped pending count',len(queue['songs']))
