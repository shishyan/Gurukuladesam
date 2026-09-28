"""Compare selected source recordings using existing PCM hashes and near-length audio windows."""
import json,hashlib,subprocess,sys,concurrent.futures,itertools
from pathlib import Path
import imageio_ffmpeg,numpy as np
root=Path(__file__).resolve().parent;batch=root/sys.argv[1];ff=imageio_ffmpeg.get_ffmpeg_exe()
selected={x['sourceId'] for x in json.loads((batch/'jobs.json').read_text(encoding='utf-8'))['songs']}
paths={}
for p in root.rglob('*.m4a'):
    if 'source' in p.parts:paths.setdefault(p.stem,p)
cache={}
for p in root.rglob('audio-uniqueness.json'):
    try:d=json.loads(p.read_text(encoding='utf-8'))
    except (ValueError,OSError):continue
    for t in d.get('tracks',[]):
        if all(k in t for k in ['sourceId','sha256','durationSeconds']):cache[t['sourceId']]=t
def decode(item):
    sid,p=item;raw=subprocess.check_output([ff,'-v','error','-i',str(p),'-ac','1','-ar','8000','-f','s16le','pipe:1'])
    a=np.frombuffer(raw,dtype='<i2');return {'sourceId':sid,'durationSeconds':len(a)/8000,'sha256':hashlib.sha256(raw).hexdigest(),'signatures':[a[int(len(a)*r):int(len(a)*r)+48000].astype(float) for r in [.1,.5,.9]]}
new=[decode((sid,batch/'source'/(sid+'.m4a'))) for sid in sorted(selected)]
duplicates=[];near=[]
for t in new:
    for old in cache.values():
        if old['sourceId'] not in selected and old['sha256']==t['sha256']:duplicates.append([t['sourceId'],old['sourceId']])
for a,b in itertools.combinations(new,2):
    if a['sha256']==b['sha256']:duplicates.append([a['sourceId'],b['sourceId']])
near_ids={old['sourceId'] for old in cache.values() if old['sourceId'] not in selected and old['sourceId'] in paths and any(abs(old['durationSeconds']-t['durationSeconds'])<2 for t in new)}
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:old_decoded=list(pool.map(decode,[(sid,paths[sid]) for sid in sorted(near_ids)]))
for a in new:
    for b in old_decoded+new:
        if a['sourceId']==b['sourceId'] or abs(a['durationSeconds']-b['durationSeconds'])>=2:continue
        corr=[float(np.corrcoef(x,y)[0,1]) for x,y in zip(a['signatures'],b['signatures']) if len(x)==len(y)]
        if len(corr)==3 and min(corr)>.995:near.append({'sources':[a['sourceId'],b['sourceId']],'correlations':corr})
tracks={sid:{k:v for k,v in t.items() if k!='signatures'} for sid,t in cache.items()}
for t in new:tracks[t['sourceId']]={k:v for k,v in t.items() if k!='signatures'}
report={'selectedSources':sorted(selected),'tracksCompared':len(tracks),'duplicateDecodedAudio':duplicates,'nearDuplicateCandidates':near,'nearLengthSourcesDecoded':len(old_decoded),'method':'Decoded mono 8kHz PCM SHA256 compared with previously saved hashes; three six-second correlation windows for source durations differing by less than two seconds. This does not prove lyric identity or exclude shifted excerpts.','tracks':list(tracks.values())}
(batch/'audio-uniqueness.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
assert not duplicates and not near,{'duplicates':duplicates,'near':near}
print('PASS:',len(selected),'sources;',len(tracks),'recording hashes;',len(old_decoded),'near-length source windows checked',flush=True)
