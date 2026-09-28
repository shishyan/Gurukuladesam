import json
from pathlib import Path
here=Path(__file__).resolve().parent
data=json.loads((here/'batch.json').read_text(encoding='utf-8'))
titles={
'thirumanthiram_2026':'திருமந்திரம் (முதல் தந்திரம்) 2026 | Thirumanthiram Cinematic Shiva Film',
'sivapuranam_ii':'சிவ புராணம் 2026 (II) | Sivapuranam II Cinematic Shiva Film',
'maasil_veenaiyum_alt':'மாசில் வீணையும் | Maasil Veenaiyum — Alternate Recording Shiva Film',
'mandhiram_aavadhu_neeru_alt':'மந்திரம் ஆவது நீறு | Mandhiram Aavadhu Neeru — Alternate Recording Film',
'thiruvothur_i':'திருவோத்தூர் பதிகம் 2026 (I) | Thiruvothur I Cinematic Shiva Film',
}
rows=[]
for film in data['films']:
    film['title']=titles[film['slug']]
    assert len(film['title'])<=100
    path=here/film['slug']/'manifest.json'
    if path.exists():
        m=json.loads(path.read_text(encoding='utf-8'));m['title']=film['title']
        path.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    rows.append({'sourceId':film['sourceId'],'title':film['title'],'file':f"shiva-batch-10/{film['slug']}/{film['slug'].upper()}-CINEMATIC-ritual-v2.mp4",'description':film['title']+'\n\nThe complete original Guru Kula Desam recording with fresh AI-generated devotional imagery, gentle camera movement, dheepam and incense. This distinct recording is labeled by its original version or as an alternate recording.\n\nOriginal song: https://youtu.be/'+film['sourceId']+'\nMusic: Guru Kula Desam\n\n#GuruKulaDesam #LordShiva #TamilDevotional','playlists':['Discography','Lord Shiva Songs'],'visibility':'Public','status':'In production'})
(here/'batch.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(here/'youtube-metadata.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
