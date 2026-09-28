import json,subprocess,sys
from pathlib import Path
import yt_dlp,imageio_ffmpeg,numpy as np
root=Path(__file__).resolve().parent/sys.argv[1];jobs=json.loads((root/'jobs.json').read_text(encoding='utf-8'));rows=[]
for job in jobs['songs']:
    sid=job['sourceId']
    with yt_dlp.YoutubeDL({'format':'worstvideo[ext=mp4]','outtmpl':str(root/'source'/(sid+'-cover.%(ext)s')),'quiet':True,'no_warnings':True,'noprogress':True}) as y:y.extract_info('https://www.youtube.com/watch?v='+sid,download=True)
    raw=subprocess.check_output([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-i',str(root/'source'/(sid+'-cover.mp4')),'-vf','fps=1/30,scale=64:64,format=gray','-f','rawvideo','pipe:1'])
    frames=np.frombuffer(raw,dtype=np.uint8).reshape(-1,64,64).astype(np.int16)
    delta=max(float(np.abs(x-frames[0]).mean()) for x in frames)
    assert delta<2,'Changing source video requires investigation'
    rows.append({'sourceId':sid,'samples':len(frames),'maximumMeanPixelDelta':round(delta,3)});print(rows[-1],flush=True)
(root/'source-cover-checks.json').write_text(json.dumps({'method':'Frames sampled every 30 seconds, decoded grayscale 64x64 compared with first frame; static cover-based sources.','sources':rows},indent=2),encoding='utf-8')
