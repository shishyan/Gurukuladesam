import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
GEN = Path(r'C:\Users\Shishyan\.codex\generated_images\01a0df15-42ba-7c23-9656-d0d29669ac1e')
FILMS = [
    ('kadavul_vazhthu', 'kA_mQ4bRB2E', 'KADAVUL-VAZHTHU-FILM.mp4', 'திருக்குறள் - கடவுள் வாழ்த்து | Kadavul Vazhthu Cinematic Thirukkural Film', ['dd856ebf-ca19-4316-b6c0-ec7bfcc89b4d', 'fe9b917a-3617-49d4-9bd3-76c435bc24cf', '4bb57fb8-6ab1-484b-88d0-09889c947d1c'], 7),
    ('ilvazhkkai', 'v_dsHTOvKP8', 'ILVAZHKKAI-FILM.mp4', 'திருக்குறள் - இல்வாழ்க்கை | Ilvazhkkai Cinematic Thirukkural Film', ['01dfdc0d-30eb-4423-8892-c73f11a52ef2', '47acd7d3-d14e-4392-98d0-ff82d7bb33a9', '50c20926-3e0a-4614-9c75-cf5790e5db18'], 6),
    ('aruludaimai', 'EChaj0wXk_0', 'ARULUDAIMAI-FILM.mp4', 'திருக்குறள் - அருளுடைமை | Aruludaimai Cinematic Thirukkural Film', ['0fbbca0e-df6d-44ee-acee-b2a1b841d09f', '50e6c0b7-3d4a-47cb-b587-3691713e814e', '172780aa-f919-4214-9faf-8813c3d4745d'], 6),
]

for slug, source_id, output, title, ids, rain in FILMS:
    sheets = []
    for i, image_id in enumerate(ids, 1):
        src = GEN / f'exec-{image_id}.png'
        dst = ROOT / 'sheets' / f'{slug}-{i}.png'
        shutil.copyfile(src, dst)
        sheets.append(str(dst))
    subprocess.run(['python', str(ROOT / 'make_storyboard.py'), slug, source_id, output, title, *sheets], check=True)
    manifest = ROOT / slug / 'manifest.json'
    data = json.loads(manifest.read_text(encoding='utf-8'))
    data['rainShots'] = [rain]
    data['lightningShots'] = [rain]
    manifest.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
