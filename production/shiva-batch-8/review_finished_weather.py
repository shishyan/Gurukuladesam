"""Extract finished dry and wet frames for release review."""
import json
import subprocess
from pathlib import Path

import imageio_ffmpeg
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
assert (HERE / 'QC.txt').read_text(encoding='utf-8-sig').count('PASS ') == 5
assert (HERE / 'legacy-weather-qc.txt').read_text(encoding='utf-8').count('PASS ') == 2
films = json.loads((HERE / 'batch.json').read_text(encoding='utf-8'))['films']
groups = [
    ('finished-weather-review.jpg', [HERE / film['slug'] for film in films]),
    ('legacy-finished-weather-review.jpg', [HERE.parent / 'shiva-batch-6' / slug for slug in ['nattrunai_vilakkam', 'poovar_senni']]),
]
for name, folders in groups:
    board = Image.new('RGB', (1280, len(folders) * 360))
    draw = ImageDraw.Draw(board)
    for row, folder in enumerate(folders):
        manifest = json.loads((folder / 'manifest.json').read_text(encoding='utf-8'))
        wet = manifest['rainShots'][-1]
        dry = 8 if folder.parent.name == 'shiva-batch-6' else wet - 1
        for col, index in enumerate([dry, wet]):
            shot = manifest['shots'][index]
            midpoint = (shot['inFrame'] + shot['outFrame']) / (2 * manifest['fps'])
            frame = folder / ('dry-frame-review.jpg' if col == 0 else 'weather-frame-review.jpg')
            subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-v', 'error', '-y', '-ss', str(midpoint), '-i', str(folder / manifest['output']), '-frames:v', '1', str(frame)], check=True)
            board.paste(Image.open(frame).convert('RGB').resize((640, 360)), (col * 640, row * 360))
            draw.text((col * 640 + 8, row * 360 + 8), f"{folder.name} - {'dry' if col == 0 else 'wet'}", fill='yellow', stroke_width=1, stroke_fill='black')
    board.save(HERE / name, quality=90)
    print(HERE / name)
