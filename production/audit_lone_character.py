import json,re,datetime
from pathlib import Path
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parent
dest=root/'lone-character-audit';dest.mkdir(exist_ok=True)
raw=(root/'character-audit-channel-current.json').read_bytes()
channel=json.loads(raw.decode('utf-16') if raw.startswith(b'\xff\xfe') else raw.decode('utf-8-sig'))
live={x['id']:x for x in channel['entries'] if x}
records={}
def visit(x):
    if isinstance(x,list):
        for v in x:visit(v)
    elif isinstance(x,dict):
        sid=x.get('sourceId') or x.get('source_id')
        url=x.get('publishedUrl') or x.get('uploadedUrl') or x.get('url')
        vid=x.get('youtubeVideoId') or x.get('videoId')
        if not vid and isinstance(url,str):
            m=re.search(r'(?:youtu\.be/|[?&]v=)([\w-]{11})',url);vid=m[1] if m else None
        if sid and vid and vid!=sid and vid in live:records.setdefault(sid,{}).update({vid:x})
        for v in x.values():
            if isinstance(v,(list,dict)):visit(v)
bases=[root,Path('C:/GitHub/Gurukuladesam/production')]
for base in bases:
    for p in base.rglob('*.json'):
        if 'playlist-audit' in p.parts or dest in p.parents:continue
        if not any(k in p.name.lower() for k in ['published','release','progress','manifest','ready']):continue
        try:visit(json.loads(p.read_text(encoding='utf-8-sig')))
        except (ValueError,OSError):pass
rows=[];covered=set()
for base in bases:
    for p in sorted(base.rglob('manifest.json')):
        try:d=json.loads(p.read_text(encoding='utf-8-sig'))
        except (ValueError,OSError):continue
        sid=d.get('sourceId');shots=d.get('shots',[])
        if sid not in records or not shots:continue
        ids=[v for v in records[sid] if v not in covered]
        if not ids:continue
        if not all((p.parent/s['image']).exists() for s in shots):continue
        # Prefer the finished local film that matches this saved publication title.
        if not (p.parent/d.get('output','')).is_file():continue
        for vid in ids:
            index=len(rows);fps=d.get('fps',12)
            row={'index':index,'sourceId':sid,'videoId':vid,'title':live[vid]['title'],'manifest':str(p.resolve()),'seconds':sum((s['outFrame']-s['inFrame'])/fps for s in shots),'shots':[dict(number=i+1,image=str((p.parent/s['image']).resolve()),seconds=(s['outFrame']-s['inFrame'])/fps) for i,s in enumerate(shots)],'classification':'Awaiting visual inspection','publicationRecord':records[sid][vid]}
            rows.append(row);covered.add(vid)
            w=1536;h=((len(shots)+5)//6)*164+42
            canvas=Image.new('RGB',(w,h),'#151515');draw=ImageDraw.Draw(canvas)
            draw.text((8,6),f"{index:03d} | {vid} | {sid} | {p.parent.name}",fill='white')
            for i,s in enumerate(row['shots']):
                img=Image.open(s['image']).convert('RGB');img.thumbnail((256,144))
                x=(i%6)*256;y=42+(i//6)*164
                canvas.paste(img,(x,y));draw.text((x+3,y+144),f"S{i+1:02d} {s['seconds']:.1f}s",fill='white')
            contact=dest/f"{index:03d}-{vid}.jpg";canvas.save(contact,quality=85);row['contact']=str(contact.resolve())
report={'checkedAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'publicChannelCount':len(live),'mappedLocalFilmCount':len(rows),'rule':'More than 75% of duration with exactly one depicted primary character, excluding lower-corner channel logo/ritual overlays. Count group characters within the scene. Assess source shot images and duration, verify candidate published film before replacement.','films':rows,'unmappedPublicVideos':[dict(videoId=vid,title=v['title'],duration=v.get('duration')) for vid,v in live.items() if vid not in covered]}
(dest/'inventory.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('Public videos:',len(live),'mapped local films:',len(rows),'unmapped:',len(live)-len(rows))
print('Contacts:',dest)
