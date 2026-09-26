"""Render the complete Thiruppavai 1 image-motion film from verified audio."""
import json
import math
import subprocess
from pathlib import Path

import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
STILLS = ROOT / "production/approved/thiruppavai1"
AUDIO = next((ROOT / "source/youtube").glob("RDcw0Bol-cE*.m4a"))
LOGO = ROOT / "production/gananatha-om/channel-avatar-reference.jpg"
OUTPUT = HERE / "THIRUPPAVAI-1-CINEMATIC-v1.mp4"
SOURCE_VIDEO_ID = "RDcw0Bol-cE"
ALLOW_REPEAT = True
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
W, H, FPS = 1280, 720, 24

# The image order traces the nine devotees from the Margazhi gathering through
# rain, their collective pilgrimage, and an offering at the Vishnu sanctum.
SHOTS = [
    ("S24", .50,.51,1.06,"blue-hour gopuram reflection"),
    ("S21", .48,.52,1.10,"lotus-tank first light"),
    ("S19", .52,.50,1.08,"Margazhi rain"),
    ("S07", .50,.49,1.04,"nine devotees gather"),
    ("S09", .50,.55,1.13,"kolam threshold"),
    ("TG02",.50,.47,1.05,"nine devotees at tank"),
    ("S18", .48,.48,1.12,"morning temple bell"),
    ("S22", .48,.54,1.08,"sheltered lamp"),
    ("S21", .56,.59,1.36,"lotus water detail"),
    ("TG03",.50,.49,1.04,"nine devotees walk together"),
    ("S30", .50,.55,1.06,"nine lotus departure"),
    ("S32", .50,.54,1.07,"nine pairs of footprints"),
    ("S33", .50,.54,1.09,"temple ascent"),
    ("S34", .50,.54,1.07,"after rain ascent"),
    ("S35", .50,.49,1.06,"gopuram approach"),
    ("TG03",.61,.48,1.35,"walking group closer framing"),
    ("S36", .49,.52,1.06,"wet-to-dry threshold"),
    ("S37", .51,.53,1.09,"garland passage"),
    ("S38", .49,.52,1.09,"garland toward sanctum"),
    ("TG01",.50,.49,1.04,"nine devotees in mandapam"),
    ("S27", .50,.49,1.06,"sacred conch and chakra"),
    ("S28", .48,.51,1.11,"ritual conch"),
    ("S29", .53,.52,1.11,"chakra reflection"),
    ("S25", .51,.51,1.09,"sacred gold reflection"),
    ("TG01",.60,.48,1.30,"mandapam group closer framing"),
    ("S39", .50,.52,1.06,"nine garlands"),
    ("S40", .50,.49,1.06,"sanctum light offering"),
    ("TG04",.50,.49,1.04,"nine devotees offer flowers"),
    ("S41a",.50,.50,1.06,"offering reaches sanctum"),
    ("S41b",.50,.49,1.07,"sanctum door light"),
    ("TG04",.58,.48,1.30,"group prayer closer framing"),
    ("S31", .50,.50,1.07,"vision resolves"),
    ("S42", .50,.49,1.04,"final sanctum hold"),
]

def source_for(code):
    folder = STILLS if code.startswith("S") else HERE
    matches = list(folder.glob(f"{code}-*.png"))
    if len(matches) != 1:
        raise ValueError(f"Expected one source for {code}: {matches}")
    return matches[0]

def duration_frames():
    result = subprocess.run([FFMPEG,"-i",str(AUDIO)],capture_output=True)
    import re
    match = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", result.stderr.decode("utf-8","replace"))
    h,m,s = match.groups()
    return round((int(h)*3600+int(m)*60+float(s))*FPS)

def cuts(count):
    pcm = subprocess.check_output([FFMPEG,"-loglevel","error","-i",str(AUDIO),"-ac","1","-ar","4000","-f","f32le","pipe:1"])
    samples = np.frombuffer(pcm,dtype="<f4")
    points=[0]
    for i in range(1,len(SHOTS)):
        nominal=round(i*count/len(SHOTS))
        lo=max(points[-1]+120,nominal-18)
        hi=min(count-(len(SHOTS)-i)*120,nominal+18)
        if hi<lo: raise ValueError("Insufficient duration for shot plan")
        def score(f):
            c=int(f*4000/FPS)
            window=samples[max(0,c-260):min(len(samples),c+260)]
            return (math.sqrt(float(np.mean(window*window))) if len(window) else 0)+abs(f-nominal)*.0002
        points.append(min(range(lo,hi+1),key=score))
    return points+[count]

def frame_for(source,spec,t,index):
    _,cx,cy,base,_=spec
    zoom=base+.035*(t if index%2==0 else 1-t)
    sw,sh=source.size
    cw=min(sw/zoom,sh*W/H/zoom)
    ch=cw*H/W
    x=min(max(cx*sw-cw/2+(t-.5)*.023*sw*(1 if index%2==0 else -1),0),sw-cw)
    y=min(max(cy*sh-ch/2,0),sh-ch)
    return source.crop((round(x),round(y),round(x+cw),round(y+ch))).resize((W,H),Image.Resampling.BICUBIC)

def main():
    count=duration_frames()
    points=cuts(count)
    sources={code:source_for(code) for code,*_ in SHOTS}
    images={code:Image.open(path).convert("RGB") for code,path in sources.items()}
    avatar=Image.open(LOGO).convert("RGB").resize((102,102),Image.Resampling.LANCZOS)
    mask=Image.new("L",avatar.size,0)
    ImageDraw.Draw(mask).ellipse((0,0,101,101),fill=255)
    if not ALLOW_REPEAT and len(sources) != len(SHOTS):
        raise ValueError("Every shot must have a distinct source image")
    manifest={"sourceVideoId":SOURCE_VIDEO_ID,"sourceAudio":str(AUDIO.relative_to(ROOT)),"imageDerived":True,"fps":FPS,"frames":count,"logo":str(LOGO.relative_to(ROOT)),"shots":[{"image":str(sources[spec[0]].relative_to(ROOT)),"role":spec[4],"inFrame":points[i],"outFrame":points[i+1],"center":[spec[1],spec[2]],"baseZoom":spec[3]} for i,spec in enumerate(SHOTS)]}
    (HERE/"review-manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    cmd=[FFMPEG,"-hide_banner","-loglevel","error","-y","-f","rawvideo","-pixel_format","rgb24","-video_size",f"{W}x{H}","-framerate",str(FPS),"-i","pipe:0","-i",str(AUDIO),"-map","0:v:0","-map","1:a:0","-c:v","libx264","-preset","veryfast","-crf","20","-pix_fmt","yuv420p","-c:a","copy","-movflags","+faststart",str(OUTPUT)]
    process=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    try:
        for i,spec in enumerate(SHOTS):
            length=points[i+1]-points[i]
            print(f"shot {i+1}/{len(SHOTS)} {spec[0]} {length} frames",flush=True)
            for local in range(length):
                frame=frame_for(images[spec[0]],spec,local/max(length-1,1),i)
                frame.paste(avatar,(24,H-24-102),mask)
                process.stdin.write(frame.tobytes())
    finally:
        process.stdin.close()
    if process.wait(): raise RuntimeError("ffmpeg encode failed")
    print(OUTPUT)

if __name__=="__main__": main()
