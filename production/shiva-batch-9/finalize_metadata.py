import json
from pathlib import Path
here=Path(__file__).resolve().parent
data=json.loads((here/'batch.json').read_text(encoding='utf-8'))
titles={
'thennadudaiya_female':'தென் நாடுடைய சிவனே போற்றி! (Female) | Cinematic Shiva Film',
'thiruvothur_v':'திருவோத்தூர் பதிகம் (V) | Thiruvothur V Cinematic Shiva Film',
'thiruppadai_hiphop':'திருப்படை ஆட்சி (HipHop) | Thiruppadai Aatchi Cinematic Shiva Film',
'namasivaya_children':'நமச்சிவாய வாழ்க! (Children) | Namasivaya Vaazhga Cinematic Shiva Film',
'kuzhaitha_pathu_ii':'குழைத்த பத்து (II) | Kuzhaitha Pathu II Cinematic Shiva Film',
}
rows=[]
for film in data['films']:
    film['title']=titles[film['slug']]
    assert len(film['title']) <= 100
    folder=here/film['slug']; path=folder/'manifest.json'
    if path.exists():
        manifest=json.loads(path.read_text(encoding='utf-8'));manifest['title']=film['title']
        path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    rows.append({'sourceId':film['sourceId'],'title':film['title'],'file':f"shiva-batch-9/{film['slug']}/{film['slug'].upper()}-CINEMATIC-ritual-v2.mp4",'description':film['title']+'\n\nThe complete original Guru Kula Desam recording, with fresh AI-generated devotional imagery, gentle camera movement, dheepam and incense. This distinct recording is labeled by its original version.\n\nOriginal song: https://youtu.be/'+film['sourceId']+'\nMusic: Guru Kula Desam\n\n#GuruKulaDesam #LordShiva #TamilDevotional','playlists':['Discography','Lord Shiva Songs'],'visibility':'Public','status':'In production'})
(here/'batch.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(here/'youtube-metadata.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
