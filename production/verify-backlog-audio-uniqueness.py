"""Check the saved queue for identical decoded audio or near-identical recordings."""
import hashlib
import itertools
import json
import subprocess
from pathlib import Path
import imageio_ffmpeg
import numpy as np

P = Path(__file__).resolve().parent
queue = json.loads((P/'publication-queue.json').read_text(encoding='utf-8'))
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
tracks = []
for row in queue['songs']:
    film = P/row['file']
    source = film.parent.parent/'source'/f"{row['sourceId']}.m4a"
    raw = subprocess.check_output([ffmpeg,'-v','error','-i',str(source),'-ac','1','-ar','8000','-f','s16le','pipe:1'])
    samples = np.frombuffer(raw,dtype='<i2')
    signature = []
    for ratio in [0.1,0.5,0.9]:
        start = min(max(0,round(len(samples)*ratio)),len(samples)-48000)
        signature.append(samples[start:start+48000].astype(np.float64))
    tracks.append({'sourceId':row['sourceId'],'durationSeconds':len(samples)/8000,
                   'decodedPcmSha256':hashlib.sha256(raw).hexdigest(),'signature':signature})
    print('Decoded',row['sourceId'],flush=True)
duplicates = []
comparisons = []
for first, second in itertools.combinations(tracks,2):
    if first['decodedPcmSha256'] == second['decodedPcmSha256']:
        duplicates.append({'sources':[first['sourceId'],second['sourceId']],'reason':'identical decoded PCM'})
    elif abs(first['durationSeconds']-second['durationSeconds']) <= 2:
        correlations = []
        for a,b in zip(first['signature'],second['signature']):
            correlations.append(float(np.corrcoef(a,b)[0,1]) if np.std(a)>0 and np.std(b)>0 else 0)
        comparisons.append({'sources':[first['sourceId'],second['sourceId']],'correlations':correlations})
        if min(correlations)>0.995:
            duplicates.append({'sources':[first['sourceId'],second['sourceId']],'reason':'near-identical audio at three separated windows','correlations':correlations})
report = {'tracksChecked':len(tracks),'decodedPcmHashesUnique':len({t['decodedPcmSha256'] for t in tracks})==len(tracks),
          'method':'Full decoded mono 8kHz PCM SHA256; three six-second correlation windows for tracks with durations within two seconds.',
          'duplicateCandidates':duplicates,'sameDurationComparisons':comparisons,
          'tracks':[{k:v for k,v in t.items() if k!='signature'} for t in tracks]}
(P/'backlog-audio-uniqueness.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
assert not duplicates, duplicates
print('No duplicate audio candidates among',len(tracks),'queued tracks.',flush=True)
