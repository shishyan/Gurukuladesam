import subprocess
from pathlib import Path
import imageio_ffmpeg

root = Path(__file__).resolve().parent / 'source'
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
for source in root.glob('*.mp4'):
    target = source.with_suffix('.m4a')
    subprocess.run([ffmpeg, '-v', 'error', '-y', '-i', str(source),
                    '-vn', '-c:a', 'copy', '-bsf:a', 'aac_adtstoasc',
                    str(target)], check=True)
    print(target.name, target.stat().st_size)
