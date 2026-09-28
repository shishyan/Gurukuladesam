import argparse,json,subprocess,sys
from pathlib import Path
parser=argparse.ArgumentParser();parser.add_argument('batch');parser.add_argument('slug');args=parser.parse_args()
root=Path(__file__).resolve().parent/args.batch
job=next(j for j in json.loads((root/'jobs.json').read_text(encoding='utf-8'))['songs'] if j['slug']==args.slug)
sheets=sorted((root/'sheets').glob(f"{args.slug}-*.png"))
assert len(sheets) in (3,6)
title=f"{job['chapter']} | {job['english']} Cinematic Shiva Film"
if len(title)>100:title=f"{job['chapter']} | {job['english']} Song Film"
output=args.slug.upper().replace('_','-')+'-FILM.mp4'
subprocess.run([sys.executable,str(root/'make_storyboard.py'),'--',args.slug,job['sourceId'],output,title,*map(str,sheets)],check=True)
p=root/args.slug/'manifest.json';data=json.loads(p.read_text(encoding='utf-8'))
data.update(rainShots=[6],lightningShots=[6],publicationStatus='in production; upload deferred by user')
collection=job.get('collection','Thiruvarutpa')
data['description']=f"{job['chapter']} — {job['english']}.\n\nA devotional image-based film for the complete original Guru Kula Desam song recording. Fresh scenes, gentle camera movement, dheepam and agarbaththi smoke, with occasional outdoor drizzle and lightning.\n\nOriginal recording: https://www.youtube.com/watch?v={job['sourceId']}\n\n#{collection} #Shiva #TamilDevotional #GuruKulaDesam"
data['playlistNames']=['Discography','Lord Shiva Songs']
p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
