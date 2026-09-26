"""Create a twelve-frame contact sheet from an encoded image film."""
import argparse
import io
import json
import subprocess
from pathlib import Path

import imageio_ffmpeg
from PIL import Image, ImageDraw

parser = argparse.ArgumentParser()
parser.add_argument("video", type=Path)
args = parser.parse_args()
video = args.video.resolve()
manifest = json.loads((video.parent / "review-manifest.json").read_text(encoding="utf-8"))
shots = manifest["shots"]
indices = [round(i * (len(shots)-1) / 11) for i in range(12)]
sheet = Image.new("RGB", (1600, 744), (18,18,18))
draw = ImageDraw.Draw(sheet)
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
for n,index in enumerate(indices):
    shot = shots[index]
    second = (shot["inFrame"] + shot["outFrame"]) / (2*manifest["fps"])
    result = subprocess.run([ffmpeg,"-hide_banner","-loglevel","error","-ss",f"{second:.3f}","-i",str(video),"-frames:v","1","-f","image2pipe","-vcodec","mjpeg","pipe:1"],capture_output=True,check=True)
    frame = Image.open(io.BytesIO(result.stdout)).convert("RGB").resize((400,225),Image.Resampling.LANCZOS)
    x=(n%4)*400; y=(n//4)*248
    sheet.paste(frame,(x,y))
    draw.text((x+6,y+228),f"{index+1:02d}  {second:05.1f}s  {shot['role']}",fill=(240,240,240))
destination = video.parent / "review-contact-sheet.jpg"
sheet.save(destination,quality=88)
print(destination)
