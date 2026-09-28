import concurrent.futures, hashlib, itertools, json, subprocess
from pathlib import Path
import imageio_ffmpeg, numpy as np
BASE=Path(__file__).parent; FF=imageio_ffmpeg.get_ffmpeg_exe()
selected={f['sourceId'] for f in json.loads((BASE/'jobs.json').read_text(encoding='utf-8'))['songs']}
sources={}
for batch in list(BASE.parent.glob('shiva-batch-*')) + list(BASE.parent.glob('shiva-offline-*')) + list(BASE.parent.glob('thiruvarutpa-*')) + [BASE.parent/'ten-song-batch', BASE.parent/'ten-more-batch', BASE]:
 for p in (batch/'source').glob('*.m4a'):
  if batch==BASE and p.stem not in selected:continue
  sources.setdefault(p.stem,p)
def decode(item):
 id,p=item;raw=subprocess.check_output([FF,'-v','error','-i',str(p),'-ac','1','-ar','8000','-f','s16le','pipe:1'])
 a=np.frombuffer(raw,dtype='<i2');signatures=[a[int(len(a)*r):int(len(a)*r)+48000].astype(float) for r in [.1,.5,.9]]
 return dict(sourceId=id,durationSeconds=len(a)/8000,sha256=hashlib.sha256(raw).hexdigest(),signatures=signatures)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:tracks=list(pool.map(decode,sources.items()))
duplicates=[];near=[]
for a,b in itertools.combinations(tracks,2):
 if not selected.intersection([a['sourceId'],b['sourceId']]):continue
 if a['sha256']==b['sha256']:duplicates.append([a['sourceId'],b['sourceId']])
 elif abs(a['durationSeconds']-b['durationSeconds'])<2:
  corr=[float(np.corrcoef(x,y)[0,1]) for x,y in zip(a['signatures'],b['signatures']) if len(x)==len(y)]
  if len(corr)==3 and min(corr)>.995:near.append(dict(sources=[a['sourceId'],b['sourceId']],correlations=corr))
report=dict(selectedSources=sorted(selected),tracksCompared=len(tracks),duplicateDecodedAudio=duplicates,nearDuplicateCandidates=near,method='Decoded mono 8kHz PCM SHA256; three six-second correlation windows when durations differ by less than two seconds.',tracks=[{k:v for k,v in t.items() if k!='signatures'} for t in tracks])
(BASE/'audio-uniqueness.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
assert not duplicates and not near,report
print('PASS: three candidate recordings differ from',len(tracks)-3,'earlier Shiva source recordings')
