import subprocess,sys
from pathlib import Path
import imageio_ffmpeg,numpy as np
root=Path(__file__).resolve().parent/sys.argv[1];ff=imageio_ffmpeg.get_ffmpeg_exe()
for p in sorted((root/'source').glob('*-cover.mp4')):
    raw=subprocess.check_output([ff,'-v','error','-i',str(p),'-vf','fps=1/30,scale=64:64,format=gray','-f','rawvideo','pipe:1'])
    f=np.frombuffer(raw,dtype=np.uint8).reshape(-1,64,64).astype(np.int16)
    maximum=max(float(np.abs(x-f[0]).mean()) for x in f)
    print(p.stem,len(f),'samples; max pixel delta',round(maximum,2))
    assert maximum<2,'Changing visual source: investigate existing film'
