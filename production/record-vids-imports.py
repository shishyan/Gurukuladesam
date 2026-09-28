"""Copy verified browser import records into per-batch release ledgers."""
import json
from pathlib import Path
P=Path(__file__).resolve().parent
imports={s['sourceId']:s for s in json.loads((P/'vids-import-progress.json').read_text(encoding='utf-8'))['imports']}
for f in list(P.glob('thirukkural-backlog-*/ready.json'))+list(P.glob('thiruvarutpa-backlog-*/ready.json')):
    data=json.loads(f.read_text(encoding='utf-8'));changed=False
    for row in data['songs']:
        if row['sourceId'] not in imports:continue
        record=imports[row['sourceId']]
        assert record['savedToDrive'] and record['volumePercent']==100 and not record['muted']
        row['googleVids']=record['googleVids']
        row['vidsVerification']={k:v for k,v in record.items() if k not in ['sourceId','googleVids']}
        changed=True
    if changed:f.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
