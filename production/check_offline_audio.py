import concurrent.futures,hashlib,itertools,json,subprocess
from pathlib import Path
import imageio_ffmpeg,numpy as np
root=Path(__file__).resolve().parent
ff=imageio_ffmpeg.get_ffmpeg_exe(); selected={}
for b in root.glob('shiva-offline-*'):
    if not b.is_dir():continue
    for j in json.loads((b/'jobs.json').read_text(encoding='utf-8'))['songs']:
        selected[j['sourceId']]=b/'source'/f"{j['sourceId']}.m4a"
sources=dict(selected)
for b in root.glob('shiva*'):
    if not b.is_dir():continue
    for p in (b/'source').glob('*.m4a'):sources.setdefault(p.stem,p)
def decode(item):
    sid,p=item
    raw=subprocess.check_output([ff,'-v','error','-i',str(p),'-ac','1','-ar','8000','-f','s16le','pipe:1'])
    a=np.frombuffer(raw,dtype='<i2')
    return {'id':sid,'duration':len(a)/8000,'hash':hashlib.sha256(raw).hexdigest(),'sig':[a[int(len(a)*r):int(len(a)*r)+48000].astype(float) for r in [.1,.5,.9]]}
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:tracks=list(pool.map(decode,sources.items()))
duplicates=[];near=[]
for a,b in itertools.combinations(tracks,2):
    if not selected.keys() & {a['id'],b['id']}:continue
    if a['hash']==b['hash']:duplicates.append([a['id'],b['id']])
    elif abs(a['duration']-b['duration'])<2:
        corr=[float(np.corrcoef(x,y)[0,1]) for x,y in zip(a['sig'],b['sig']) if len(x)==len(y)]
        if len(corr)==3 and min(corr)>.995:near.append({'ids':[a['id'],b['id']],'correlations':corr})
report={'tracksCompared':len(tracks),'selected':list(selected),'duplicates':duplicates,'nearDuplicates':near,'tracks':[{k:v for k,v in t.items() if k!='sig'} for t in tracks]}
(root/'SHIVA-OFFLINE-AUDIO-AUDIT.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print('Compared',len(tracks),'duplicates',duplicates,'near',near)
for t in tracks:
    if t['id'] in selected:print(t['id'],round(t['duration'],2))
assert not duplicates and not near
