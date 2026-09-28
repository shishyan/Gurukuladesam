import json
from pathlib import Path
here=Path(__file__).resolve().parent
films=json.loads((here/'batch.json').read_text(encoding='utf-8'))['films']
records=[]
for film in films:
    p=here/film['slug']/'QC.txt'
    if p.exists():records.append(p.read_text(encoding='utf-8'))
(here/'QC.txt').write_text(''.join(records),encoding='utf-8')
print('Verified films:',len(records))
