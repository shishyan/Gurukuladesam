"""Initialize the next claimed batch of three chapters from the saved plan."""
import argparse
import json
import shutil
import sys
from pathlib import Path

P = Path(__file__).resolve().parent
sys.stdout.reconfigure(encoding='utf-8')
parser = argparse.ArgumentParser()
parser.add_argument('number', type=int)
args = parser.parse_args()
number = args.number
assert 4 <= number <= 15
plan = json.loads((P/'thirukkural-production-plan.json').read_text(encoding='utf-8'))
selected = plan['songs'][(number-4)*3:(number-3)*3]
root = P/f'thirukkural-backlog-{number:02d}'
root.mkdir(exist_ok=True)
(root/'source').mkdir(exist_ok=True)
pools = {
    'council': ['thirukkural-backlog-01/amaichu/S02.png','thirukkural-backlog-01/amaichu/S03.png','thirukkural-backlog-01/amaichu/S04.png','thirukkural-backlog-01/amaichu/S06.png','thirukkural-backlog-01/amaichu/S07.png','thirukkural-backlog-02/avaiyarithal/S05.png','thirukkural-backlog-02/avaiyarithal/S09.png','thirukkural-backlog-01/amaichu/S10.png'],
    'care': ['thirukkural-backlog-01/amaichu/S02.png','thirukkural-backlog-01/amaichu/S06.png','thirukkural-backlog-02/arivudaimai/S07.png','thirukkural-backlog-01/amaichu/S08.png','thirukkural-backlog-02/avaiyarithal/S07.png','thirukkural-backlog-02/arivudaimai/S09.png','thirukkural-backlog-02/aalvinaiyudaimai/S11.png','thirukkural-backlog-01/amaichu/S12.png'],
    'wisdom': ['thirukkural-backlog-02/arivudaimai/S01.png','thirukkural-backlog-02/arivudaimai/S02.png','thirukkural-backlog-02/arivudaimai/S04.png','thirukkural-backlog-02/arivudaimai/S08.png','thirukkural-backlog-01/avai_anjaamai/S11.png','thirukkural-backlog-02/arivudaimai/S10.png','thirukkural-backlog-02/arivudaimai/S11.png','thirukkural-backlog-02/arivudaimai/S12.png'],
    'work': ['thirukkural-backlog-02/aalvinaiyudaimai/S01.png','thirukkural-backlog-02/aalvinaiyudaimai/S02.png','thirukkural-backlog-02/aalvinaiyudaimai/S03.png','thirukkural-backlog-02/aalvinaiyudaimai/S04.png','thirukkural-backlog-02/aalvinaiyudaimai/S07.png','thirukkural-backlog-02/aalvinaiyudaimai/S09.png','thirukkural-backlog-02/aalvinaiyudaimai/S10.png','thirukkural-backlog-02/aalvinaiyudaimai/S11.png'],
}
jobs = []
for sid, tamil, english, theme, kind in selected:
    slug = english.lower().replace(' ','_')
    jobs.append({'sourceId':sid,'chapter':tamil,'english':english,'theme':theme,'slug':slug,'supportingImages':pools[kind]})
(root/'jobs.json').write_text(json.dumps({'songs':jobs},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for name in ['render.py','qc.py']:
    shutil.copy2(P/'thirukkural-backlog-01'/name,root/name)
(root/'README.md').write_text(f'# Thirukkural backlog batch {number:02d}\n\nThree claimed chapters are listed in jobs.json. Four new chapter-specific scenes and eight relevant library scenes form each full-song film. Every scene appears once with continuous movement. Original AAC audio only; channel emblem bottom-left.\n\nPublication is pending YouTube upload quota. Recheck the live channel before release, import the MP4 into Google Vids, then publish using Guru Kula Desam Studio.\n',encoding='utf-8')
print(json.dumps({'batch':str(root),'songs':jobs},ensure_ascii=False))
