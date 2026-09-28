import json
from pathlib import Path
base=Path(__file__).parent
p=base/'batch.json';d=json.loads(p.read_text(encoding='utf-8'))
for f in d['films']:
 f['rainShots']=[10]
 f['lightningShots']=[10] if f['slug']=='thiruppadai_aatchi' else []
 m=base/f['slug']/'manifest.json';md=json.loads(m.read_text(encoding='utf-8'));md.update(rainShots=f['rainShots'],lightningShots=f['lightningShots']);m.write_text(json.dumps(md,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lines=['# Lord Shiva films — batch 7','','Five distinct source recordings; static covers checked at 30-second intervals. Twelve separate generated scenes reviewed for each film. Complete original audio, lower-left Guru Kula Desam emblem, paired dheepam, four agarbaththi per side and white-grey smoke. Drizzle is restricted to outdoor scene eleven; Thiruppadai Aatchi includes restrained lightning.','','| Song | Source | Release |','|---|---|---|']
for f in d['films']:lines.append(f"| {f['title']} | [Original](https://youtu.be/{f['sourceId']}) | Pending YouTube upload quota |")
lines+=['','Full decode and exact-audio QC results are recorded in QC.txt. Upload to Discography and Lord Shiva Songs when the daily limit relaxes. Inspect Studio for a saved draft before starting any upload.','']
(base/'RELEASES.md').write_text('\n'.join(lines),encoding='utf-8')
