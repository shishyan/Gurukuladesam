import json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw
import imageio_ffmpeg
here=Path(__file__).resolve().parent
films=json.loads((here/'batch.json').read_text(encoding='utf-8'))['films']
qc=(here/'QC.txt').read_text(encoding='utf-8-sig')
films=[film for film in films if 'PASS '+film['slug']+':' in qc]
board=Image.new('RGB',(1920,360*len(films)))
draw=ImageDraw.Draw(board)
for row,film in enumerate(films):
    folder=here/film['slug'];m=json.loads((folder/'manifest.json').read_text(encoding='utf-8'))
    wet=m['rainShots'][-1]
    for col,idx in enumerate([3,wet-1,wet]):
        s=m['shots'][idx];t=(s['inFrame']+s['outFrame'])/(2*m['fps'])
        label=['group','dry','wet'][col]
        frame=folder/(label+'-frame-review.jpg')
        if not frame.exists() or frame.stat().st_mtime < (folder/m['output']).stat().st_mtime:
            subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-y','-ss',str(t),'-i',str(folder/m['output']),'-frames:v','1',str(frame)],check=True)
        board.paste(Image.open(frame).resize((640,360)),(col*640,row*360))
        draw.text((col*640+8,row*360+8),film['slug']+' '+label,fill='yellow',stroke_width=1,stroke_fill='black')
board.save(here/'finished-weather-review.jpg',quality=90)
