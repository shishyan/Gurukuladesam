"""Render a long, non-repeating image-motion song film with the original audio."""
import argparse
import json
import math
import subprocess
from pathlib import Path

import imageio_ffmpeg
import numpy as np

FPS=12
W,H=1280,720
FFMPEG=imageio_ffmpeg.get_ffmpeg_exe()

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('manifest',type=Path)
    parser.add_argument('--test',action='store_true')
    args=parser.parse_args()
    path=args.manifest.resolve()
    data=json.loads(path.read_text(encoding='utf-8'))
    folder=path.parent
    shots=data['shots'][:2] if args.test else data['shots']
    audio=(path.parent.parent/'source'/f"{data['sourceId']}.m4a").resolve()
    logo=path.parent.parent.parent/'kalvi-image-motion/channel-emblem.png'
    assert len(shots)>=2 and audio.is_file() and logo.is_file()
    assert len({p['image'] for p in shots})==len(shots)
    if args.test:
        cuts=[0,60,120]
    else:
        raw=subprocess.check_output([FFMPEG,'-v','error','-i',str(audio),'-ac','1','-ar','8000','-f','f32le','pipe:1'])
        samples=np.frombuffer(raw,dtype='<f4')
        frames=round(len(samples)*FPS/8000)
        cuts=[0]
        n=len(shots)
        for i in range(1,n):
            nominal=round(i*frames/n)
            low=max(cuts[-1]+120,nominal-12)
            high=min(frames-(n-i)*120,nominal+12)
            def score(f):
                c=round(f*8000/FPS)
                w=samples[max(0,c-650):min(len(samples),c+650)]
                return float(np.mean(w*w))+.000002*abs(f-nominal)
            cuts.append(min(range(low,high+1),key=score))
        cuts.append(frames)
        data['fps']=FPS
        data['targetFrames']=frames
        data['imageDerived']=True
        data['cutRule']='near even spacing at low audio energy'
        for i,shot in enumerate(shots):
            shot['inFrame'],shot['outFrame']=cuts[i],cuts[i+1]
        path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    cmd=[FFMPEG,'-hide_banner','-loglevel','error','-y']
    for shot in shots:
        cmd+=['-i',str(folder/shot['image'])]
    logo_index=len(shots)
    cmd+=['-loop','1','-framerate',str(FPS),'-i',str(logo),'-i',str(audio)]
    filters=[]
    for i,shot in enumerate(shots):
        dur=cuts[i+1]-cuts[i]
        direction=1 if i%2==0 else -1
        zoom=f"1.045+0.04*on/{max(1,dur-1)}" if direction==1 else f"1.085-0.04*on/{max(1,dur-1)}"
        drift=f"(on/{max(1,dur-1)}-0.5)*0.022*iw*{direction}"
        filters.append(f"[{i}:v]scale=1344:756:force_original_aspect_ratio=increase,crop=1344:756,"
                       f"zoompan=z='{zoom}':x='(iw-iw/zoom)/2+{drift}':y='(ih-ih/zoom)/2':"
                       f"d={dur}:s={W}x{H}:fps={FPS},setsar=1[v{i}]")
    labels=''.join(f'[v{i}]' for i in range(len(shots)))
    filters.append(f'{labels}concat=n={len(shots)}:v=1:a=0[body]')
    filters.append(f'[body][{logo_index}:v]overlay=24:H-h-24:shortest=1,format=yuv420p[out]')
    output=folder/(data['output'] if not args.test else 'fast-test.mp4')
    cmd+=['-filter_complex',';'.join(filters),'-map','[out]']
    if not args.test:
        cmd+=['-map',f'{logo_index+1}:a:0']
    cmd+=['-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p']
    if not args.test:
        cmd+=['-c:a','copy']
    cmd+=['-movflags','+faststart',str(output)]
    print('Rendering',output,'shots',len(shots),'frames',cuts[-1],flush=True)
    subprocess.run(cmd,check=True)
    print(output,flush=True)

if __name__=='__main__': main()
