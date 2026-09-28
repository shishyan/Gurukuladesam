"""Exact-recording ownership check, distinct from one-film-per-composition coverage."""
import json,csv,datetime
from pathlib import Path
from collections import Counter
root=Path(__file__).resolve().parents[1]
proof=json.loads((root/'playlist-audit/master-film-proof.json').read_text(encoding='utf-8'))
records={}
for f in root.rglob('*.json'):
    name=f.name.lower()
    if 'playlist-audit' in f.parts:continue
    if not ('manifest' in name or name in ('jobs.json','ready.json','published.json','batch.json','publication-queue.json') or 'scene-plan' in name or 'ownership' in name or 'artwork-prompts' in name):continue
    try:d=json.loads(f.read_text(encoding='utf-8-sig'))
    except (ValueError,OSError):continue
    def visit(x):
        if isinstance(x,list):
            for v in x:visit(v)
        elif isinstance(x,dict):
            sid=x.get('sourceId') or x.get('source_id') or x.get('sourceVideoId')
            if sid:
                records.setdefault(sid,[]).append({'path':str(f.relative_to(root)),'status':x.get('publicationStatus') or x.get('status'),'suppressed':x.get('generationSuppressed',False)})
            for v in x.values():
                if isinstance(v,(list,dict)):visit(v)
    visit(d)
chapter=json.loads((root/'playlist-audit/thirukkural-backlog-audit.json').read_text(encoding='utf-8'))
chapters={sid:x for x in chapter['chapters'] for sid in x['recordings']}
rows=[]
for r in proof['entries']:
    if not r['status'].startswith('ALTERNATE'):continue
    refs=records.get(r['id'],[])
    category='Already started or claimed in shared workspace' if refs else 'No exact-recording production found'
    match=chapters.get(r['id'])
    row={'sourceId':r['id'],'title':r['title'],'sourceUrl':r['sourceUrl'],'status':category,'workspaceRecords':refs,'priorCompositionClassification':r['evidence'][0]['label']}
    if match:
        row['chapterProduction']=match
        mf=Path(match.get('manifest',''))
        if not mf.is_absolute():mf=root.parent/mf
        row['chapterManifestExists']=mf.exists()
        row['chapterFilmFiles']=[str(x.resolve()) for x in mf.parent.glob('*.mp4') if x.stat().st_size>1000000] if mf.exists() else []
    rows.append(row)
report={'checkedAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'84 entries previously lacking explicit alternate-version film mappings. Exact-recording start status, not composition uniqueness. Existing/claimed alternate recordings must not be selected twice. No new production claimed by this audit.','counts':dict(Counter(x['status'] for x in rows)),'rows':rows}
dest=root/'playlist-audit'
(dest/'never-started-recordings.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
with (dest/'never-started-recordings.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f);w.writerow(['Source ID','Song','Source URL','Exact recording status','Workspace records','Same chapter existing film','Previous composition classification'])
    for x in rows:w.writerow([x['sourceId'],x['title'],x['sourceUrl'],x['status'],' | '.join(r['path'] for r in x['workspaceRecords']),' | '.join(x.get('chapterFilmFiles',[])),x['priorCompositionClassification']])
with (dest/'unclaimed-recordings-only.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f);w.writerow(['Source ID','Song','Source URL','Existing chapter film','Previous composition classification'])
    for x in rows:
        if not x['workspaceRecords']:w.writerow([x['sourceId'],x['title'],x['sourceUrl'],' | '.join(x.get('chapterFilmFiles',[])),x['priorCompositionClassification']])
print(report['counts'])
for x in rows:
    if x['workspaceRecords']:print('CLAIMED',x['sourceId'],x['title'],[r['path'] for r in x['workspaceRecords']])
print('Chapter mappings with actual files:',sum(bool(x.get('chapterFilmFiles')) for x in rows))
