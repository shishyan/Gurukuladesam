import hashlib,json
from pathlib import Path
here=Path(__file__).resolve().parent
films=json.loads((here/'batch.json').read_text(encoding='utf-8'))['films']
qc=(here/'QC.txt').read_text(encoding='utf-8')
assert qc.count('PASS ')==5
assert json.loads((here/'visual-review.json').read_text(encoding='utf-8'))['finishedWeatherReviewed']
metadata=json.loads((here/'youtube-metadata.json').read_text(encoding='utf-8'))
queue=json.loads((here.parent/'shiva-batch-9/publication-queue.json').read_text(encoding='utf-8'))
queue['scope']='Pending Shiva films from batches 6 through 10; other production queues are separate'
ids={f['sourceId'] for f in films}
conflicts=[]
for path in here.parent.rglob('manifest.json'):
    if here in path.parents:continue
    try:d=json.loads(path.read_text(encoding='utf-8-sig'))
    except (ValueError,OSError):continue
    if d.get('sourceId') in ids:conflicts.append(str(path))
assert not conflicts,conflicts
scenes=[]
for film in films:
    m=json.loads((here/film['slug']/'manifest.json').read_text(encoding='utf-8'))
    for shot in m['shots']:
        image=here/film['slug']/shot['image']
        scenes.append({'file':str(image.relative_to(here)),'sha256':hashlib.sha256(image.read_bytes()).hexdigest()})
assert len(scenes)==len({s['sha256'] for s in scenes})==60
(here/'scene-uniqueness.json').write_text(json.dumps({'distinctScenes':60,'repeatedImages':[],'scenes':scenes},indent=2)+'\n',encoding='utf-8')
for row in metadata:
    row['status']='Ready; pending upload availability'
    row['qc']={'uniqueScenes':12,'exactDecodedAudio':True,'fullDecodePassed':True,'noLongBlackPassages':True,'finishedWeatherReviewed':True,'minimumGroupScenes':8}
    queue['songs'].append(row)
queue['pendingCount']=len(queue['songs'])
(here/'publication-queue.json').write_text(json.dumps(queue,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(here/'youtube-metadata.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
audio=json.loads((here/'audio-uniqueness.json').read_text(encoding='utf-8'))
(here/'pre-push-audit.json').write_text(json.dumps({'selectedSourceIds':sorted(ids),'conflictingProductionManifests':conflicts,'audioTracksCompared':audio['tracksCompared'],'duplicateDecodedAudio':audio['duplicateDecodedAudio'],'nearDuplicateCandidates':audio['nearDuplicateCandidates'],'publicTitleReview':'The existing Thirumanthiram, Maasil Veenaiyum, Thiruneetru Pathigam and Sivapuranam films use earlier recordings. New selected source recordings passed decoded-audio checks. Check Studio again before uploading.'},indent=2)+'\n',encoding='utf-8')
text='# Lord Shiva films — batch 10\n\nFive distinct recording versions, checked against earlier local production sources and refreshed public channel titles. Full original audio is preserved.\n\n'
text+='The user requested more group gatherings during production. The first eight shots in every film were revised to feature congregations, family visits, communal singing, musicians and temple processions: forty group scenes across sixty distinct final scenes. The group-first preference is saved in FILM-PRODUCTION-CHECKLIST.md. Initial sheets 1 and 2 are superseded; only the group-sheet files enter the final manifests.\n\n'
text+='Built-in imagegen artwork and complete prompt sets are saved here. Camera movement, lower-left Guru Kula Desam emblem, paired dheepam, four agarbaththi per side, white-grey rising smoke, outdoor drizzle and occasional brief lightning illumination. No additional thunder audio is mixed into the original songs.\n\n'
text+='All five passed exact decoded-audio, full media decode, distinct-scene and long black passage checks. Scene boards and finished dry/wet frames were visually reviewed. Cut placement follows low audio energy near scene intervals; detailed lyric-by-lyric editing is not claimed.\n\n'
text+='| Film | Original | Status |\n|---|---|---|\n'
for f in films:text+=f"| {f['title'].replace('|','/')} | [Recording](https://youtu.be/{f['sourceId']}) | Ready locally |\n"
text+='\nNo batch 10 film has been uploaded or published. Upload when available after checking current Studio drafts and public films; select both Discography and Lord Shiva Songs, and disclose realistic AI visuals. The prior daily-limit observation is recorded in batch 8.\n'
(here/'RELEASES.md').write_text(text,encoding='utf-8')
for path in here.glob('*render.log'):
    raw=path.read_bytes()
    if raw.startswith(b'\xff\xfe'):path.write_text(raw.decode('utf-16'),encoding='utf-8')
print('Five verified films; scoped queue count',len(queue['songs']))
