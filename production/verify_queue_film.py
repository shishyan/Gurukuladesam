import json,subprocess,sys
from pathlib import Path
from PIL import Image,ImageDraw

root=Path(__file__).resolve().parent
batch=root/sys.argv[1]
slug=sys.argv[2]
result=subprocess.run([sys.executable,str(batch/'qc.py'),slug],capture_output=True,text=True)
print(result.stdout)
if result.returncode:
    print(result.stderr)
    raise SystemExit(result.returncode)
subprocess.run([sys.executable,str(batch/'frames.py'),slug],check=True)
folder=batch/slug
data=json.loads((folder/'manifest.json').read_text(encoding='utf-8'))
data['localQC']={'originalAudioExact':True,'fullDecode':True,'visualReview':'pending'}
(folder/'manifest.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
canvas=Image.new('RGB',(1280,760),'#111111')
draw=ImageDraw.Draw(canvas)
for i,label in enumerate(['opening','rain','dry']):
    im=Image.open(folder/f'{label}-qc.png').resize((640,360))
    x=(i%2)*640;y=(i//2)*380
    canvas.paste(im,(x,y+20));draw.text((x+8,y+3),label,fill='white')
canvas.save(folder/'qc-contact.png')
