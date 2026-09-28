import hashlib
import subprocess
from pathlib import Path
import imageio_ffmpeg

root=Path(__file__).resolve().parent
prod=root.parent
files=list(root.glob('*.m4a'))+[
 prod/'murugar-batch-4/source/iPFEtwdcIxc.m4a',
 prod/'next-five-image-motion/source/On2xoZqBsss.m4a',
 prod/'new-unique-batch/source/W2peLbC20sA.m4a',
]
ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
for path in files:
    process=subprocess.Popen([ffmpeg,'-v','error','-i',str(path),'-map','0:a:0',
        '-ac','1','-ar','8000','-f','s16le','pipe:1'],stdout=subprocess.PIPE)
    digest=hashlib.sha256()
    samples=0
    while chunk:=process.stdout.read(1_000_000):
        digest.update(chunk)
        samples+=len(chunk)//2
    if process.wait()!=0: raise RuntimeError(path)
    print(path.name,round(samples/8000,2),digest.hexdigest(),flush=True)
