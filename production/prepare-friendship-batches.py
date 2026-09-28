import json, shutil
from pathlib import Path
root=Path(__file__).resolve().parent
items=[('cwTmzDGpLJw','நட்பு','Natpu','natpu'),('EgSJqPCUMoo','பழைமை','Pazhaimai','pazhaimai'),('MCjbrWdQbos','தீ நட்பு','Thee Natpu','thee_natpu'),('aTpCSZFFbow','கூடா நட்பு','Kooda Natpu','kooda_natpu'),('Wq6XpZ49Huw','நட்பாராய்தல்','Natpaaraaythal','natpaaraaythal'),('VIC7Oj5k2C0','படைச்செருக்கு','Padaicherukku','padaicherukku'),('dEx_Zuc5omc','பொருள்செயல்வகை','Porul Seyalvagai','porul_seyalvagai')]
for b in range(3):
    folder=root/f'thirukkural-new-releases-{b+1:02d}'
    folder.mkdir(exist_ok=True);(folder/'source').mkdir(exist_ok=True)
    songs=[]
    for sid,ta,en,slug in items[b*3:b*3+3]:
        (folder/slug).mkdir(exist_ok=True)
        songs.append(dict(sourceId=sid,chapter=ta,english=en,slug=slug,status='reserved for full original-song production',visualPreference='community groups and gatherings in most scenes; context appropriate individuals only'))
    (folder/'jobs.json').write_text(json.dumps({'songs':songs},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    shutil.copyfile(root/'thirukkural-backlog-11/render.py',folder/'render.py')
print('Reserved seven originals in three batches. Remixes excluded.')
