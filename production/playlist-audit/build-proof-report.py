"""Produce inspectable evidence; do not treat title matches as completion proof."""
import json,csv,html,datetime
from pathlib import Path
from collections import Counter
import yt_dlp
root=Path(__file__).resolve().parents[1]
dest=root/'playlist-audit'
with yt_dlp.YoutubeDL({'extract_flat':True,'skip_download':True,'quiet':True,'no_warnings':True}) as y:
    live=y.extract_info('https://www.youtube.com/playlist?list=PLAjtBRKl_IlI',download=False)
entries=[{'id':x['id'],'title':x.get('title') or '[Unavailable entry]'} for x in live['entries'] if x]
snapshot={'checkedAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'playlistId':live['id'],'title':live['title'],'reportedCount':live.get('playlist_count'),'returnedCount':len(entries),'uniqueIds':len({x['id'] for x in entries}),'entries':entries}
(dest/'master-live-count-proof.json').write_text(json.dumps(snapshot,ensure_ascii=False,indent=2),encoding='utf-8')
prior=json.loads((dest/'full-playlist-refresh-2026-09-28.json').read_text(encoding='utf-8'))
master=next(x for x in prior['playlists'] if x['name']=='Discography')
known={x['id']:x for x in master['entries']}
rows=[]
for x in entries:
    sid=x['id'];r=known.get(sid,{})
    evidence=[];status='NEEDS INVESTIGATION'
    if r.get('classification')=='existing film entry':
        status='Film listed publicly (title evidence)';evidence=[{'label':'Public film','target':'https://www.youtube.com/watch?v='+sid}]
    elif isinstance(r.get('evidence'),list):
        for ref in r['evidence']:
            f=root/ref['file']
            try:d=json.loads(f.read_text(encoding='utf-8-sig'))
            except (ValueError,OSError):continue
            rs=d if isinstance(d,list) else d.get('songs',[d])
            for q in rs:
                if not isinstance(q,dict) or (q.get('sourceId') or q.get('source_id') or q.get('sourceVideoId'))!=sid:continue
                url=q.get('publishedUrl') or q.get('youtubeUrl')
                if url:evidence.append({'label':'Publication record: '+str(url),'target':url})
                out=q.get('output') or q.get('outputFile') or q.get('videoPath')
                if isinstance(out,str):
                    for movie in [f.parent/out,Path(out),root/out]:
                        if movie.is_file() and movie.stat().st_size>1000000:
                            evidence.append({'label':str(movie.resolve())+' ('+str(movie.stat().st_size)+' bytes)','target':movie.resolve().as_uri()});break
                if f.name=='review-manifest.json' and not out:
                    for movie in f.parent.glob('*.mp4'):
                        if movie.stat().st_size>1000000:evidence.append({'label':str(movie.resolve())+' ('+str(movie.stat().st_size)+' bytes)','target':movie.resolve().as_uri()})
        if evidence:status='Local film file / publication record found'
    elif r.get('classification')=='existing video; skip duplicate':
        e=r.get('evidence',{})
        evidence=[{'label':url,'target':url} for url in e.get('films',[])]
        status='Prior audit links an existing film'
    elif 'excluded' in r.get('classification',''):
        status='Excluded third-party recording'
    else:
        status='ALTERNATE VERSION — completion mapping needs verification'
        evidence=[{'label':'Prior classification: '+r.get('classification','')+'; '+str(r.get('evidence','')),'target':''}]
    rows.append({**x,'sourceUrl':'https://www.youtube.com/watch?v='+sid,'status':status,'evidence':evidence})
counts=dict(Counter(x['status'] for x in rows))
report={'checkedAtUtc':snapshot['checkedAtUtc'],'counts':counts,'limitations':'Local MP4 existence and saved publication records are evidence of a build, not a fresh playback or public-visibility check. Alternate-version matches remain unproven in this report.','entries':rows}
(dest/'master-film-proof.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
with (dest/'master-film-proof.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f);w.writerow(['Number','YouTube ID','Title','Source URL','Evidence status','Film / evidence'])
    for i,r in enumerate(rows,1):w.writerow([i,r['id'],r['title'],r['sourceUrl'],r['status'],' | '.join(e['label'] for e in r['evidence'])])
esc=html.escape
table=[]
for i,r in enumerate(rows,1):
    links='<br>'.join(('<a href="'+esc(e['target'],quote=True)+'">'+esc(e['label'])+'</a>') if e['target'] else esc(e['label']) for e in r['evidence'])
    table.append('<tr><td>'+str(i)+'</td><td><a href="'+r['sourceUrl']+'">'+esc(r['title'])+'</a><br><small>'+r['id']+'</small></td><td>'+esc(r['status'])+'</td><td>'+links+'</td></tr>')
page='''<!doctype html><meta charset="utf-8"><title>Guru Kula Desam — master playlist evidence</title>
<style>body{font:16px system-ui;margin:30px;color:#172334}table{border-collapse:collapse;width:100%}td,th{padding:10px;border:1px solid #ddd;text-align:left;vertical-align:top}td:last-child{max-width:550px;overflow-wrap:anywhere}th{background:#edf3f7}input{padding:12px;width:80%;margin:20px 0}small{color:#657}a{color:#165aa0}</style>
<h1>Master playlist: entry-by-entry evidence</h1>'''
page+='<p>Live check: '+esc(snapshot['checkedAtUtc'])+'. YouTube reports '+str(snapshot['reportedCount'])+' entries; fetched '+str(len(rows))+' unique IDs.</p>'
page+='<p><strong>This is a count of playlist entries, not completed productions.</strong> Audio releases, alternate versions and films appear together.</p><ul>'
page+=''.join('<li>'+esc(k)+': '+str(v)+'</li>' for k,v in counts.items())+'</ul>'
page+='<p>'+esc(report['limitations'])+'</p><input id="search" placeholder="Search a song, ID, status, or evidence"><table><thead><tr><th>#</th><th>Playlist entry</th><th>Evidence status</th><th>Film / evidence</th></tr></thead><tbody>'+''.join(table)+'</tbody></table>'
page+='''<script>document.getElementById('search').addEventListener('input',e=>{const q=e.target.value.toLowerCase();document.querySelectorAll('tbody tr').forEach(r=>r.hidden=!r.textContent.toLowerCase().includes(q))})</script>'''
(dest/'master-film-proof.html').write_text(page,encoding='utf-8')
print(json.dumps({'liveCount':len(rows),'counts':counts},ensure_ascii=False))
