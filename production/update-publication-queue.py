"""Record only QC-passed full films that are still awaiting publication."""
import json
from pathlib import Path

P = Path(__file__).resolve().parent
entries = []
other_owners = {}
for manifest_path in sorted(P.glob('thirukkural-batch-*/*/manifest.json')):
    manifest = json.loads(manifest_path.read_text(encoding='utf-8-sig'))
    if manifest.get('sourceId'):
        other_owners[manifest['sourceId']] = {
            'manifest':str(manifest_path.relative_to(P)),
            'file':str((manifest_path.parent/manifest['output']).relative_to(P))}
excluded = []
batch10 = json.loads((P/'batch-sept-28-10/ready.json').read_text(encoding='utf-8'))
for row in batch10['songs']:
    if not row.get('publishedUrl'):
        folder = P/'batch-sept-28-10'/row['slug']
        manifest = json.loads((folder/'manifest.json').read_text(encoding='utf-8'))
        entries.append({'sourceId':row['sourceId'],'title':row['title'],
                        'file':str((folder/manifest['output']).relative_to(P)),
                        'googleVids':row['googleVids'],'status':'ready; pending upload quota'})
for ready in sorted(P.glob('thirukkural-backlog-*/ready.json')):
    data = json.loads(ready.read_text(encoding='utf-8'))
    changed = False
    for row in data['songs']:
        if not row.get('publishedUrl'):
            film = ready.parent/row['file']
            assert film.exists()
            if row['sourceId'] in other_owners:
                owner = other_owners[row['sourceId']]
                excluded.append({'sourceId':row['sourceId'],'title':row['title'],
                                 'alternateRender':str(film.relative_to(P)),
                                 'preferredOtherProduction':owner,
                                 'status':'alternate render excluded from upload; other agent owns this source song'})
                row.update(status='excluded from upload: other-agent production exists',
                           uploadSuppressed=True,preferredOtherProduction=owner)
                changed = True
                continue
            entries.append({'sourceId':row['sourceId'],'title':row['title'],
                            'file':str(film.relative_to(P)), 'googleVids':row.get('googleVids'),
                            'status':'ready; pending upload quota','qc':row['qc']})
    if changed:
        ready.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert len(entries) == len({r['sourceId'] for r in entries})
out = {'channel':'@guru-kula-desam','pendingCount':len(entries),'blocker':'YouTube daily upload limit',
       'releaseInstructions':'Recheck public channel for duplicates, import locally finished films into Google Vids, publish through the correct channel Studio, and verify public URLs. Scheduling requires the upload to succeed first.',
       'songs':entries,'excludedAlternateRenders':excluded}
(P/'publication-queue.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lines = ['# Pending song videos', '', f"{len(entries)} QC-passed full-song films are ready locally. YouTube publication is blocked by the daily upload quota.", '',
         'The first two already have Google Vids projects. The remaining local films must be imported into Vids before publication.', '',
         '| Song | Source | Local MP4 |', '| --- | --- | --- |']
for row in entries:
    label = row['title'].replace('|','/').replace('\n',' ')
    lines.append(f"| {label} | `{row['sourceId']}` | [Open film]({row['file'].replace(chr(92),'/')}) |")
lines.extend(['', 'Scheduling changes the publication time after an upload succeeds. It does not bypass the upload quota.',
              '', 'Before publication, refresh the public channel and check for another film of the same song. Record and verify each published URL.'])
if excluded:
    lines.extend(['','## Other-agent productions: do not upload the alternate renders','',
                  '| Source | Preferred other production | Excluded alternate |','| --- | --- | --- |'])
    for row in excluded:
        preferred = row['preferredOtherProduction']['file'].replace(chr(92),'/')
        alternate = row['alternateRender'].replace(chr(92),'/')
        lines.append(f"| `{row['sourceId']}` | [{preferred}]({preferred}) | {alternate} |")
(P/'PENDING-VIDEOS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('QC-passed pending films:',len(entries))
print('Alternate renders excluded to avoid cross-agent duplicates:',len(excluded))
