"""Sample the finished film to make a compact visual review sheet."""
import io
import json
import subprocess
from pathlib import Path

import imageio_ffmpeg
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
VIDEO = HERE / "THIRUPPAVAI-1-CINEMATIC-v1.mp4"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
manifest = json.loads((HERE / "review-manifest.json").read_text(encoding="utf-8"))
shots = manifest["shots"]
chosen = [0,3,5,9,12,15,19,22,25,27,30,32]
sheet = Image.new("RGB",(4*400,3*248),(18,18,18))
draw = ImageDraw.Draw(sheet)
for n,index in enumerate(chosen):
    shot=shots[index]
    second=(shot["inFrame"]+shot["outFrame"])/(2*manifest["fps"])
    result=subprocess.run([FFMPEG,"-hide_banner","-loglevel","error","-ss",f"{second:.3f}","-i",str(VIDEO),"-frames:v","1","-f","image2pipe","-vcodec","mjpeg","pipe:1"],capture_output=True,check=True)
    image=Image.open(io.BytesIO(result.stdout)).convert("RGB").resize((400,225),Image.Resampling.LANCZOS)
    x=(n%4)*400; y=(n//4)*248
    sheet.paste(image,(x,y))
    draw.text((x+7,y+228),f"{index+1:02d}  {second:05.1f}s  {shot['role']}",fill=(240,240,240))
sheet.save(HERE / "review-contact-sheet.jpg",quality=88)
