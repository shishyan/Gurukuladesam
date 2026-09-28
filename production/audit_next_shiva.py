import json,re
from pathlib import Path
import yt_dlp
root=Path(__file__).resolve().parent
opts={'extract_flat':True,'skip_download':True,'quiet':True,'no_warnings':True}
with yt_dlp.YoutubeDL(opts) as ydl:
    live=ydl.extract_info('https://www.youtube.com/@guru-kula-desam/videos',download=False)
entries=[{'id':x['id'],'title':x['title'],'duration':x.get('duration')} for x in live['entries']]
(root/'channel-live-offline-production.json').write_text(json.dumps({'entries':entries},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
catalog=json.loads((root/'playlist-audit/catalog-2026-09-26.json').read_text(encoding='utf-8'))['songs']
sources={x['id']:x for x in catalog}
existing=[]
for p in root.rglob('manifest.json'):
    try:d=json.loads(p.read_text(encoding='utf-8-sig'))
    except(ValueError,OSError):continue
    existing.append((d.get('title',''),sources.get(d.get('sourceId'),{}).get('release') or '',str(p)))
candidates=['I-ZLmvGIiz4','lAWfE9YSJME','06ZOKy7SSvw','0TB3drCSvNc','DCJ2qoMSIBA','hDoLscfeg5Q','juuVtFBK3X8','kshlDPh2IqE','kyiaup-gjMc','MlaG3Z3_Kck','YORF54ouPz0','Z7qFXMBjnak','73GrCFM_v6Q','EOkuHFSfv8c','nGBmGzsD-kM']
def norm(s):return re.sub(r'[\W\d_]','',s.lower()).replace('திருவருட்பா','').replace('இரண்டாம்திருமுறை','').replace('ஆறாம்திருமுறை','')
rows=[]
for sid in candidates:
    s=sources[sid];key=norm(s['release'])
    matches=[title for title,release,path in existing if key and (key in norm(title) or key in norm(release))]
    matches += [x['title'] for x in entries if any(k in x['title'].lower() for k in ['film','cinematic','music video']) and key in norm(x['title'])]
    rows.append({**s,'matchingFilms':matches})
(root/'SHIVA-NEXT-SOURCE-AUDIT.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('live uploads',len(entries))
for r in rows:print(r['id'],r['release'],'MATCHES',r['matchingFilms'])
