import json
from pathlib import Path
root=Path(__file__).resolve().parent
scenes={
'amaichu_remix':[
'Ultra-wide sunrise panorama of an ancient Tamil town with an open council pavilion, many residents gathering along broad streets, majestic orchestral scale',
'A diverse council of Tamil elders, women and men listening around a broad stone table, dignified collaborative discussion',
'A community gathering reviewing granary baskets and palm-leaf records with a thoughtful adviser, naturally posed hands',
'Farmers and irrigation workers consulting together at a stone canal junction, wide countryside view',
'An assembly of artisans and neighbours sharing practical knowledge in a shaded courtyard',
'Women, men and young adults planning a community meal beside abundant vegetable baskets, candid interaction',
'Wet outdoor town square under soft grey monsoon clouds, neighbours sheltering together beneath woven umbrellas, no lightning bolts',
'Dry interior council hall, a mixed-age assembly listening attentively to a calm speaker, warm oil-lamp lighting and no rain',
'A group of advisers hearing villagers speak beneath a banyan canopy, inclusive respectful gathering',
'Many workers and families opening a repaired irrigation gate together in late afternoon, hopeful wide composition',
'An open pavilion council meeting at dusk, neighbours seated in a semicircle with a welcoming central speaker',
'Ultra-wide evening town panorama, community gathered beneath warm courtyard lamps and an expansive sky, peaceful closing'],
'aran_symphony':[
'Ultra-wide powerful dawn panorama of a massive ancient Tamil stone fort overlooking farmland and a river, many townspeople approaching the gate, symphonic grandeur',
'Families and guards welcoming travellers at a broad fortified entrance, dignified peaceful community scene',
'Builders and village elders inspecting a stone rampart together, realistic historic Tamil clothing',
'A group of farmers, traders and children sharing supplies in a protected courtyard beside grain stores',
'Neighbours carrying water jars together to a broad clean communal cistern inside the fort',
'A council of women and men discussing the welfare of their town in a shaded gatehouse pavilion',
'Wet outdoor stone fort walkway beneath monsoon clouds, grouped townspeople carrying palm umbrellas, no visible lightning bolts',
'Dry enclosed hall inside the fort, families and elders gathered beside food stores, warm lamplight, absolutely no rain',
'Workers and residents maintaining a stone bridge together, welcoming safe passage, wide river view',
'Children and elders learning together in a protected courtyard garden, serene group interaction',
'Many neighbours celebrating a shared harvest beneath fort walls in amber evening light',
'Ultra-wide sunset panorama of the fort, river and green fields, peaceful community silhouettes along the parapet, spacious closing'],
'avai_anjaamai_female':[
'Ultra-wide dawn view of an ancient Tamil open-air assembly pavilion beside a lake, women and men arriving in groups, expansive musical opening',
'A Tamil woman standing thoughtfully before a large seated assembly, calm courage, respectful listeners and natural anatomy',
'Several women and elders studying palm-leaf manuscripts together in a shaded courtyard',
'An inclusive circle of neighbours exchanging ideas beneath a banyan tree, children listening nearby',
'A group of young women practising a speech with supportive elders at a stone veranda, warm candid atmosphere',
'Residents of different ages listening carefully to a woman explaining an idea in an open hall, encouraging faces',
'Wet outdoor path toward the assembly pavilion under grey clouds, groups sharing palm umbrellas, no frozen lightning bolts',
'Dry enclosed lecture hall, a woman speaking confidently to neighbours seated in a semicircle, warm lamps, no rain',
'Community members discussing a thoughtful question in small groups beside a lotus lake',
'A woman and several advisers presenting palm-leaf records to a dignified council, balanced group composition',
'The assembled community thanking several speakers in a wide sunset courtyard, shared warmth and confidence',
'Ultra-wide twilight lake and assembly pavilion, families and neighbours departing together beneath a violet sky, hopeful peaceful closing']}
jobs=json.loads((root/'jobs.json').read_text(encoding='utf-8'));prompts=[]
for job in jobs['songs']:
 ss=scenes[job['slug']]
 for i in range(0,12,4):
  prompt='Create exactly FOUR distinct cinematic images in a precise 2x2 grid with no borders, gutters, labels or text. Overall landscape 16:9 canvas; each quadrant is also 16:9. Use case: historical-scene. Tamil Thirukkural song film '+job['english']+'; theme '+job['theme']+'. Photorealistic painterly film quality, authentic ancient Tamil architecture, culturally accurate traditional clothing, realistic human anatomy and natural hands. Prefer group gatherings in every human scene, with varied participants and activity. Keep important faces and actions clear of lower corners for overlays added later. No modern objects, no logos or watermarks, no letters, no lightning bolts, no incense/lamp corner overlays. Each scene completely different in location, arrangement, activity, camera and lighting. '
  prompt+=' '.join(label+': '+scene+'.' for label,scene in zip(['Top left','Top right','Bottom left','Bottom right'],ss[i:i+4]))
  prompts.append({'slug':job['slug'],'sheet':i//4+1,'prompt':prompt,'path':str((root/'sheets'/f"{job['slug']}-{i//4+1}.png").resolve())})
 (root/(job['slug']+'-SCENES.json')).write_text(json.dumps(ss,ensure_ascii=False,indent=2),encoding='utf-8')
(root/'artwork-prompts.json').write_text(json.dumps(prompts,ensure_ascii=False,indent=2),encoding='utf-8')
print('9 sheets; 36 fresh group scenes planned')
