import hashlib,io,json,subprocess,sys
from pathlib import Path
import imageio_ffmpeg
from PIL import Image,ImageDraw,ImageChops
root=Path(__file__).resolve().parent/sys.argv[1]
ff=imageio_ffmpeg.get_ffmpeg_exe()
def audio(p):return subprocess.check_output([ff,'-v','error','-i',str(p),'-map','0:a:0','-c','copy','-f','adts','pipe:1'])
def frame(p,t):return Image.open(io.BytesIO(subprocess.check_output([ff,'-v','error','-ss',str(t),'-i',str(p),'-frames:v','1','-f','image2pipe','-vcodec','mjpeg','pipe:1']))).convert('RGB')
ready={'songs':[]}
for p in sorted(root.glob('*/manifest.json')):
    d=json.loads(p.read_text(encoding='utf-8'));film=p.parent/d['output']
    matched=hashlib.sha256(audio(film)).digest()==hashlib.sha256(audio(root/'source'/f"{d['sourceId']}.m4a")).digest()
    decode=subprocess.run([ff,'-v','error','-i',str(film),'-f','null','NUL'],capture_output=True)
    contact=Image.new('RGB',(1280,630),'#141414');draw=ImageDraw.Draw(contact);moves=[]
    for i,s in enumerate(d['shots']):
        a,b=s['inFrame']/d['fps'],s['outFrame']/d['fps']
        moves.append(ImageChops.difference(frame(film,a+1),frame(film,b-1)).getbbox() is not None)
        x,y=i%4*320,i//4*210;contact.paste(frame(film,(a+b)/2).resize((320,180)),(x,y));draw.text((x+5,y+184),f'Scene {i+1}',fill='white')
    unique=len({hashlib.sha256((p.parent/s['image']).read_bytes()).digest() for s in d['shots']})
    report={'sourceId':d['sourceId'],'durationSeconds':d['targetFrames']/d['fps'],'uniqueImages':unique,'originalAacBitstreamMatched':matched,'fullDecodePassed':decode.returncode==0,'allScenesHaveMovement':all(moves),'logoPosition':'bottom-left, 24px inset','fileBytes':film.stat().st_size}
    assert matched and decode.returncode==0 and unique==12 and all(moves),report
    contact.save(p.parent/'contact-qc.jpg',quality=88)
    (p.parent/'qc.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    ready['songs'].append({'sourceId':d['sourceId'],'title':d['title'],'file':str(film.relative_to(root)),'qc':report,'status':'ready; pending Google Vids import and upload'})
    print(p.parent.name,report,flush=True)
(root/'ready.json').write_text(json.dumps(ready,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
