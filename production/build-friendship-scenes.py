import json,shutil,sys
from pathlib import Path
root=Path(__file__).resolve().parent
libraries={
'natpu':[('thirukkural-backlog-07/suttranthazhaal',n) for n in [1,3,5,6,7,8,9,10,12]],
'pazhaimai':[('thirukkural-backlog-02/arivudaimai',n) for n in [2,3,5,7,9,10]]+[('thirukkural-backlog-07/suttranthazhaal',n) for n in [2,4,12]],
'thee_natpu':[('thirukkural-backlog-05/kuttrankadithal',n) for n in [3,7,8,9,12]]+[('thirukkural-backlog-02/avaiyarithal',n) for n in [3,5,8,9]],
'kooda_natpu':[('thirukkural-backlog-02/avaiyarithal',n) for n in [2,3,5,6,8,9,10,11,12]],
'natpaaraaythal':[('thirukkural-backlog-11/therinthu_thelithal',n) for n in [2,3,5,6,7,8,9,10,12]],
'padaicherukku':[('thirukkural-backlog-14/valiyarithal',n) for n in [1,4,5,7,8,9,10,11,12]],
'porul_seyalvagai':[('thirukkural-backlog-14/vinai_seyalvagai',n) for n in [2,3,4,5,6,7,9,10,12]],
}
batch=root/sys.argv[1]
jobs=json.loads((batch/'jobs.json').read_text(encoding='utf-8'))['songs']
for j in jobs:
    folder=batch/j['slug'];sources=[folder/f'new-{i}.png' for i in range(1,4)]
    supports=[root/d/f'S{n:02d}.png' for d,n in libraries[j['slug']]]
    order=[sources[0]]+supports[:3]+[sources[1]]+supports[3:6]+[sources[2]]+supports[6:]
    shots=[]
    for i,src in enumerate(order,1):
        assert src.is_file(),src
        name=f'S{i:02d}.png';shutil.copyfile(src,folder/name)
        shots.append({'image':name,'role':'community narrative scene','assetSource':str(src.relative_to(root)),'artOrigin':'new song-specific artwork' if src in sources else 'relevant group scene library'})
    d={'sourceId':j['sourceId'],'title':f"திருக்குறள் - {j['chapter']} | {j['english']} | Full Song Film",'output':j['slug'].upper()+'-CINEMATIC-v1.mp4','shots':shots,'visualDirection':'Group gatherings, reciprocal support and community story; no looping scenes','audioRule':'Full original AAC bitstream only, no clip audio'}
    (folder/'manifest.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(j['slug'],'12 scenes prepared')
