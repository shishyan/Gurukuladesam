import argparse,json,datetime
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('--vids');p.add_argument('--duration');p.add_argument('--published');p.add_argument('--playback',action='store_true');a=p.parse_args()
root=Path(__file__).resolve().parent
for f in root.glob('thirukkural-new-releases-*/ready.json'):
    d=json.loads(f.read_text(encoding='utf-8'))
    for r in d['songs']:
        if r['sourceId']!=a.source:continue
        if a.vids:r.update(googleVids=a.vids,vidsVerification={'savedToDrive':True,'fullDuration':a.duration,'volume':100,'mute':False,'automaticDucking':'Off'},status='Google Vids saved; ready for publication')
        if a.published:r.update(publishedUrl=a.published,publicationVerified=True,publishedAtUtc=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='published; YouTube checks continue in background')
        if a.playback:r.update(publicPlaybackVerified=True,status='published; public playback and bottom-left logo verified; original audio matched locally')
        f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        if r.get('publishedUrl'):
            ledger=root/'release-progress.json';l=json.loads(ledger.read_text(encoding='utf-8'))
            existing=next((q for q in l['acceptedUploads'] if q['sourceId']==a.source),None)
            if existing:existing.update(url=r['publishedUrl'],status=r['status'])
            else:l['acceptedUploads'].append({'sourceId':a.source,'url':r['publishedUrl'],'status':r['status']})
            ledger.write_text(json.dumps(l,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(r['status']);raise SystemExit
raise ValueError('Source owner not found')
