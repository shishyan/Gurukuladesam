"""Check audio preservation, decoding, scene uniqueness and actual movement."""
import hashlib
import io
import json
import subprocess
from pathlib import Path
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageChops

ROOT = Path(__file__).resolve().parent
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

def frame(film, seconds):
    raw = subprocess.check_output([FFMPEG, '-v', 'error', '-ss', str(seconds), '-i', str(film),
                                   '-frames:v', '1', '-f', 'image2pipe', '-vcodec', 'mjpeg', 'pipe:1'])
    return Image.open(io.BytesIO(raw)).convert('RGB')

def audio(path):
    return subprocess.check_output([FFMPEG, '-v', 'error', '-i', str(path), '-map', '0:a:0',
                                    '-c', 'copy', '-f', 'adts', 'pipe:1'])

rows = []
for path in sorted(ROOT.glob('*/manifest.json')):
    data = json.loads(path.read_text(encoding='utf-8'))
    folder = path.parent
    film = folder/data['output']
    source = ROOT/'source'/f"{data['sourceId']}.m4a"
    audio_ok = hashlib.sha256(audio(source)).digest() == hashlib.sha256(audio(film)).digest()
    decode = subprocess.run([FFMPEG, '-v', 'error', '-i', str(film), '-f', 'null', 'NUL'], capture_output=True)
    contact = Image.new('RGB', (1280,630), '#141414')
    draw = ImageDraw.Draw(contact)
    movement = []
    for i, shot in enumerate(data['shots']):
        start, end = shot['inFrame']/data['fps'], shot['outFrame']/data['fps']
        early, late = frame(film, start+1), frame(film, end-1)
        movement.append(ImageChops.difference(early, late).getbbox() is not None)
        middle = frame(film, (start+end)/2).resize((320,180))
        x,y = (i%4)*320,(i//4)*210
        contact.paste(middle,(x,y)); draw.text((x+5,y+184),f'Scene {i+1}',fill='white')
    contact.save(folder/'contact.jpg',quality=88)
    hashes = [hashlib.sha256((folder/s['image']).read_bytes()).hexdigest() for s in data['shots']]
    report = {'sourceId': data['sourceId'], 'durationSeconds': data['targetFrames']/data['fps'],
              'scenes': len(hashes), 'uniqueImages': len(set(hashes)),
              'originalAacBitstreamMatched': audio_ok, 'fullDecodePassed': decode.returncode == 0,
              'allScenesHaveMovement': all(movement), 'logoPosition': 'bottom-left, 24px inset',
              'fileBytes': film.stat().st_size}
    assert audio_ok and decode.returncode == 0 and len(set(hashes)) == 12 and all(movement), report
    (folder/'qc.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    rows.append({'sourceId':data['sourceId'],'title':data['title'],'file':str(film.relative_to(ROOT)),
                 'status':'ready; pending daily upload quota','publishedUrl':None,'qc':report})
    print(folder.name,report,flush=True)
(ROOT/'ready.json').write_text(json.dumps({'songs':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
