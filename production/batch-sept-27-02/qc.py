import hashlib
import io
import json
import subprocess
from pathlib import Path

import imageio_ffmpeg
from PIL import Image, ImageDraw

root=Path(__file__).resolve().parent
ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
for folder in (root/'guru_bhagavan',root/'sani_thuthi',root/'sani_pathigam'):
    data=json.loads((folder/'manifest.json').read_text(encoding='utf-8'))
    source=root/'source'/f"{data['sourceId']}.m4a"
    film=folder/data['output']
    def audio_bytes(path):
        return subprocess.check_output([ffmpeg,'-v','error','-i',str(path),'-map','0:a:0','-c','copy','-f','adts','pipe:1'])
    audio_ok=hashlib.sha256(audio_bytes(source)).digest()==hashlib.sha256(audio_bytes(film)).digest()
    decode=subprocess.run([ffmpeg,'-v','error','-i',str(film),'-f','null','NUL'],capture_output=True)
    hashes=[hashlib.sha256((folder/s['image']).read_bytes()).hexdigest() for s in data['shots']]
    contact=Image.new('RGB',(4*320,3*210),'#141414')
    drawer=ImageDraw.Draw(contact)
    for i,shot in enumerate(data['shots']):
        middle=(shot['inFrame']+shot['outFrame'])/2/data['fps']
        frame=subprocess.check_output([ffmpeg,'-v','error','-ss',str(middle),'-i',str(film),'-frames:v','1','-f','image2pipe','-vcodec','mjpeg','pipe:1'])
        im=Image.open(io.BytesIO(frame)).convert('RGB').resize((320,180))
        x=(i%4)*320;y=(i//4)*210
        contact.paste(im,(x,y));drawer.text((x+5,y+184),f"Scene {i+1}",fill='white')
    contact.save(folder/'contact.jpg',quality=85)
    report={'sourceId':data['sourceId'],'song':data['title'],'durationSeconds':data['targetFrames']/data['fps'],
            'scenes':len(data['shots']),'uniqueImages':len(set(hashes)),'originalAacBitstreamMatched':audio_ok,
            'fullDecodePassed':decode.returncode==0,'fileBytes':film.stat().st_size}
    (folder/'qc.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(folder.name,report,flush=True)

