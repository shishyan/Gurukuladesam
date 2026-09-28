import json,shutil,datetime
from pathlib import Path
import yt_dlp
root=Path(__file__).resolve().parent
batch=root/'unclaimed-group-batch-08'
assert not batch.exists()
spec=[('RY7nPGorS94','thoothu_remix','Thoothu Remix','thoughtful truthful diplomacy and carrying messages responsibly','an ancient Tamil river capital with broad palace forecourts and shaded traveller gardens'),('MvwT6dnGE0U','vinai_seyalvagai_female','Vinai Seyalvagai Female','careful practical action through planning, cooperation and completion','an ancient Tamil coastal craft town with workshops, a lively harbour and civic courtyards'),('ulW6fg4lkYA','idukkan_remix','Idukkan Varungaal Naguga Remix','steadfast courage, humour and mutual support during adversity','an ancient Tamil hill valley settlement with terraced fields and riverside community shelters')]
conflicts=[]
for base in [root,Path('C:/GitHub/Gurukuladesam/production')]:
    for p in base.rglob('*.json'):
        if 'playlist-audit' in p.parts:continue
        if not any(k in p.name.lower() for k in ['manifest','jobs','ready','published','batch','scene-plan','ownership','artwork-prompts','queue']):continue
        try:txt=p.read_text(encoding='utf-8-sig')
        except OSError:continue
        for sid,*_ in spec:
            if sid in txt:conflicts.append({'sourceId':sid,'path':str(p)})
assert not conflicts,conflicts
batch.mkdir();(batch/'source').mkdir();(batch/'sheets').mkdir()
for name in ['render.py','qc.py','frames.py','make_storyboard.py','dheepam-agarbaththi-corners.png','prepare_batch.py','finish_batch.py','record_publication.py']:
    shutil.copy2(root/'unclaimed-group-batch-07'/name,batch/name)
songs=[]
for sid,slug,english,theme,setting in spec:
    with yt_dlp.YoutubeDL({'quiet':True,'no_warnings':True,'format':'bestaudio[ext=m4a]','outtmpl':str(batch/'source'/(sid+'.%(ext)s'))}) as y:
        info=y.extract_info('https://www.youtube.com/watch?v='+sid,download=True)
    songs.append(dict(sourceId=sid,slug=slug,chapter=info['title'],sourceTitle=info['title'],english=english,theme=theme,setting=setting,collection='Thirukkural',duration=info['duration']))
(batch/'jobs.json').write_text(json.dumps(dict(owner='Main Guru Kula Desam task',status='Reserved; production and publication authorized',songs=songs),ensure_ascii=False,indent=2),encoding='utf-8')
(batch/'ownership-check.json').write_text(json.dumps(dict(checkedAtUtc=datetime.datetime.now(datetime.timezone.utc).isoformat(),conflicts=conflicts,selectedSources=[x[0] for x in spec],scope='Both shared production workspaces checked before reservation'),indent=2),encoding='utf-8')
for name in ['finish_batch.py','record_publication.py']:
    p=batch/name;p.write_text(p.read_text(encoding='utf-8').replace('07','08'),encoding='utf-8')
print('Reserved and downloaded three source recordings',flush=True)
