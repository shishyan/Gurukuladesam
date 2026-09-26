"""Explicitly image-based video effects study; never rewrites the source image."""
from pathlib import Path
import math
import random
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import imageio_ffmpeg

folder = Path(__file__).resolve().parent
root = folder.parents[2]
w, h, fps, seconds = 1280, 720, 24, 8
rng = random.Random(62021)
mask = Image.new('L', (w, h), 0)
draw = ImageDraw.Draw(mask)
# Exterior only: conservative distant sky and clear pond, not roof or people.
draw.polygon([(452, 0), (1280, 0), (1280, 350), (1000, 345),
              (938, 277), (816, 278), (749, 130), (647, 62), (538, 148), (455, 139)], fill=255)
draw.polygon([(612, 382), (970, 382), (938, 419), (601, 418)], fill=255)
mask_array = np.asarray(mask.filter(ImageFilter.GaussianBlur(1.4)), dtype=np.float32) / 255
drops = []
for depth, count in [(0, 800), (1, 230)]:
    for _ in range(count):
        drops.append((rng.uniform(-30, w + 30), rng.uniform(0, h),
                      rng.uniform(220, 340) if depth else rng.uniform(130, 200),
                      rng.uniform(7, 13) if depth else rng.uniform(3, 7),
                      rng.uniform(45, 85) if depth else rng.uniform(18, 40)))
impacts = [(rng.uniform(-0.5, seconds), rng.uniform(625, 935), rng.uniform(389, 414),
            rng.uniform(0.2, 0.45), rng.uniform(1.8, 3.5)) for _ in range(240)]
label = "drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='IMAGE-BASED EFFECTS STUDY - PEOPLE NOT ANIMATED':fontsize=20:fontcolor=white:box=1:boxcolor=black@0.75:x=20:y=20"
graph = (
    '[0:v]scale=1280:720,setsar=1,format=gbrp[b];'
    '[1:v]format=gbrp[r];[b][r]blend=all_mode=screen:all_opacity=0.42,'
    # One restrained continuous eight-pixel drift, no zoom oscillation/jitter.
    "scale=1296:729,crop=1280:720:x='4+8*t/8':y=4,"
    f'{label},format=yuv420p[v]'
)
output = folder / 'VS06-temple-IMAGE-BASED-EFFECTS-STUDY-v1.mp4'
cmd = [imageio_ffmpeg.get_ffmpeg_exe(), '-hide_banner', '-loglevel', 'warning', '-n',
       '-loop', '1', '-framerate', str(fps), '-i', str(folder / 'VS06-temple-community-rain-master-v1.png'),
       '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{w}x{h}', '-r', str(fps), '-i', 'pipe:0',
       '-filter_complex', graph, '-map', '[v]', '-an', '-frames:v', str(fps * seconds),
       '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-movflags', '+faststart', str(output)]
proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
try:
    for frame in range(fps * seconds):
        t = frame / fps
        layer = Image.new('L', (w, h), 0)
        pen = ImageDraw.Draw(layer)
        for x, phase, speed, length, opacity in drops:
            y = (phase + speed * t) % (h + 30) - 15
            xx = x - y * 0.085
            pen.line((xx, y, xx - length * 0.085, y + length), fill=int(opacity), width=1)
        for birth, x, y, life, size in impacts:
            age = t - birth
            if 0 < age < life:
                p = age / life
                rad = size * (0.3 + p)
                pen.arc((x-rad, y-rad*0.22, x+rad, y+rad*0.22), 0, 290,
                        fill=int(85*(1-p)), width=1)
                if p < 0.25:
                    pen.line((x, y, x, y-1.5), fill=int(100*(1-p)), width=1)
        values = np.asarray(layer.filter(ImageFilter.GaussianBlur(0.3)), dtype=np.float32) * mask_array
        proc.stdin.write(np.repeat(values.astype(np.uint8)[:, :, None], 3, axis=2).tobytes())
finally:
    proc.stdin.close()
if proc.wait() != 0:
    raise RuntimeError('Effects study encode failed')
print(output)
