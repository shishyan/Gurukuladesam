import json
import subprocess
import sys
from pathlib import Path

import imageio_ffmpeg

root = Path(__file__).resolve().parent
folder = root / sys.argv[1]
data = json.loads((folder / 'manifest.json').read_text(encoding='utf-8'))
film = folder / data['output']
for label, number in [('opening', 0), ('rain', data['rainShots'][0]), ('dry', data['rainShots'][0] + 1)]:
    shot = data['shots'][number]
    frame = shot['inFrame'] + min(24, (shot['outFrame'] - shot['inFrame']) // 2)
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-v', 'error', '-y', '-ss', str(frame / data['fps']), '-i', str(film), '-frames:v', '1', str(folder / f'{label}-qc.png')], check=True)
