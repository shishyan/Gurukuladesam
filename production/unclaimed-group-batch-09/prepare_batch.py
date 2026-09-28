import json,subprocess,sys
from pathlib import Path
root=Path(__file__).resolve().parent
jobs=json.loads((root/'jobs.json').read_text(encoding='utf-8'))
for job in jobs['songs']:
    if len(list((root/'sheets').glob(job['slug']+'-*.png')))!=3:continue
    folder=root/job['slug']
    if (folder/'manifest.json').exists():continue
    subprocess.run([sys.executable,str(root.parent/'prepare_offline_film.py'),root.name,job['slug']],check=True)
    f=folder/'manifest.json';d=json.loads(f.read_text(encoding='utf-8'))
    d['title']=f"{job['chapter']} | {job['english']} Cinematic Thirukkural Film"
    assert len(d['title'])<=100
    d['description']=f"{job['chapter']} — {job['english']}.\n\nA complete Guru Kula Desam Thirukkural recording presented with fresh community scenes.\n\nOriginal recording: https://www.youtube.com/watch?v={job['sourceId']}\n\n#Thirukkural #Tamil #GuruKulaDesam"
    d['playlistNames']=['Discography','திருக்குறள் | Thirukkural — Master Collection']
    scenes=json.loads((root/(job['slug']+'-SCENES.json')).read_text(encoding='utf-8'))
    for shot,role in zip(d['shots'],scenes):shot['role']=role
    d['recordingVersion']=job['english']
    f.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Prepared',job['slug'],flush=True)
