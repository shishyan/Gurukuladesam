"""Video-only procedural effects composite. Source still is never repainted."""
from pathlib import Path
import subprocess, random, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import imageio_ffmpeg

root=Path(__file__).resolve().parents[2]
out=root/'production/batch03/ANBU-rain-environment-EFFECTS-TEST-v2.mp4'
w,h=768,512
rng=random.Random(8201)
# Coordinates are half-source pixels. Conservative outdoor mask only.
mask=Image.new('L',(w,h),0)
md=ImageDraw.Draw(mask)
md.polygon([(0,150),(220,150),(220,310),(252,343),(740,500),(768,512),(0,512)],fill=255)
# Foreground occluders: foliage, vessels and dog. Deliberately conservative.
md.rectangle((0,235,118,430),fill=0)
md.rectangle((120,270,172,332),fill=0)
md.rectangle((213,250,271,343),fill=0)
md.ellipse((110,350,218,418),fill=0)
md.rectangle((0,434,279,512),fill=0)
mask_arr=np.asarray(mask,dtype=np.float32)/255
drops=[(rng.uniform(-30,w+30),rng.uniform(0,h),rng.uniform(190,340),rng.uniform(4,10),rng.uniform(0.15,0.45)) for _ in range(340)]
# Sparse irregular impacts only on exposed paving; no large pond rings.
impacts=[]
for _ in range(230):
    x=rng.uniform(225,685); y=rng.uniform(360,500)
    if mask.getpixel((int(x),int(y))) and y>343+(x-252)*0.322:
        impacts.append((rng.uniform(0,20),x,y,rng.uniform(.18,.38),rng.uniform(1.2,3.4)))
label="drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='RAIN EFFECTS TEST - STILL PEOPLE - INCOMPLETE':fontsize=20:fontcolor=white:box=1:boxcolor=black@0.7:x=112:y=18"
graph=f'[0:v]scale=1080:720,pad=1280:720:100:0:black,format=gbrp[b];[1:v]scale=1080:720,pad=1280:720:100:0:black,format=gbrp[r];[b][r]blend=all_mode=screen:all_opacity=0.55,format=gbrp,{label},format=yuv420p[v]'
cmd=[imageio_ffmpeg.get_ffmpeg_exe(),'-hide_banner','-loglevel','warning','-y','-loop','1','-framerate','24','-i',str(root/'production/batch03/ANBU-courtyard-v1.png'),'-f','rawvideo','-pix_fmt','rgb24','-s',f'{w}x{h}','-r','24','-i','pipe:0','-i',str(root/'source/youtube/lneosghJWgs.m4a'),'-filter_complex',graph,'-map','[v]','-map','2:a','-t','20','-c:v','libx264','-preset','veryfast','-crf','18','-c:a','aac','-b:a','192k','-movflags','+faststart',str(out)]
proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
try:
    for f in range(480):
        t=f/24
        layer=Image.new('L',(w,h),0);d=ImageDraw.Draw(layer)
        for x,y,speed,length,opacity in drops:
            yy=(y+speed*t)%(h+30)-15
            xx=x+9*math.sin(t*.28)-yy*.045
            d.line((xx,yy,xx-.6,yy+length),fill=int(255*opacity),width=1)
        for birth,x,y,life,size in impacts:
            a=t-birth
            if 0<a<life:
                p=a/life;rad=size*(.3+p)
                d.arc((x-rad,y-rad*.3,x+rad,y+rad*.3),10,155,fill=int(100*(1-p)),width=1)
                if p<.45:d.line((x,y,x+.5,y-2.5*(1-p)),fill=int(130*(1-p)),width=1)
        arr=np.asarray(layer.filter(ImageFilter.GaussianBlur(.25)),dtype=np.float32)*mask_arr
        rgb=np.repeat(arr.astype(np.uint8)[:,:,None],3,axis=2)
        proc.stdin.write(rgb.tobytes())
finally:
    proc.stdin.close()
if proc.wait()!=0:raise RuntimeError('FFmpeg composite failed')
print(out)
