import json,sys
from pathlib import Path
root=Path(__file__).resolve().parent/sys.argv[1]
jobs=json.loads((root/'jobs.json').read_text(encoding='utf-8'));prompts=[]
for job in jobs['songs']:
    setting=job['setting'];theme=job['theme']
    scenes=[
      f'Ultra-wide dawn panorama of {setting}, many families and neighbours arriving along broad paths, expansive sky and powerful orchestral scale',
      f'A diverse group of Tamil elders, women and men discussing {theme} around a broad stone table in a shaded courtyard, natural respectful interaction',
      f'Neighbours gathering at a small market and checking fair weights together, warm shared trust, setting {setting}',
      f'Families and traders returning a found woven basket to its owner together, open smiles and respectful community interaction, setting {setting}',
      f'A mixed-age group learning from a wise elder beside palm-leaf manuscripts in a sunlit veranda, theme {theme}',
      f'Women and men cooking and sharing a vegetarian community meal beneath trees, children helping elders, setting {setting}',
      f'Wet outdoor public square in {setting} beneath soft monsoon clouds, groups sharing woven palm umbrellas, no lightning bolts or drawn rain streaks',
      f'Dry enclosed stone assembly hall, a large attentive gathering considering {theme}, golden lamps and absolutely no rain',
      f'A Tamil woman calmly speaking to a seated circle of neighbours about {theme}, hopeful natural faces, a different courtyard and camera viewpoint',
      f'Several families and village workers repairing a stone water channel together at late afternoon, cooperative spirit, setting {setting}',
      f'A broad gathering thanking elders and community helpers at sunset beside a lake, warm gratitude, theme {theme}',
      f'Ultra-wide twilight panorama of {setting}, communities gathering under courtyard lamps and an expansive indigo sky, serene closing']
    if job['slug'].startswith('kooda_'):
        scenes[3]='Community members tending a small grove together away from the public hall, quietly keeping their promises through helpful work, authentic ancient Tamil village setting'
    if job['slug'].startswith('vaaymai_'):
        scenes[2]='Women, men and young adults listening to one another in an open council pavilion, a truthful thoughtful exchange, warm natural light and authentic Tamil surroundings'
    if job['slug'].startswith('thuravu_'):
        scenes[2]='A group of villagers and ascetics giving surplus grain and folded clothing to families in a forest monastery courtyard, dignified mutual care'
        scenes[3]='Elders and young adults placing unnecessary ornaments aside and tending saplings together in a quiet forest grove, simplicity and contentment'
        scenes[9]='A community helping elderly neighbours carry water beside a forest lake, humble service and simple clothing'
    if job['slug'].startswith('idanarithal_'):
        scenes[2]='A broad village council examining several safe river crossing locations from a high rocky viewpoint, varied groups and expansive valley geography'
        scenes[3]='Farmers and builders together inspecting stable high ground for a granary, river floodplain visible in the distance'
        scenes[9]='Village workers building a small stone bridge at a narrow stable river crossing while families watch from a safe bank'
    if job['slug'].startswith('kaalamarithal_'):
        scenes[2]='Farmers and elders waiting patiently under a pavilion while observing distant monsoon clouds above unplanted fields'
        scenes[3]='Families sowing seeds together after the first seasonal rain, fertile damp earth and soft morning sunlight'
        scenes[9]='A large group of farmers harvesting ripe golden grain at the right season, joyful purposeful activity beneath a warm afternoon sky'
    if job['slug'].startswith('valiyarithal_'):
        scenes[2]='Craft workers and elders assessing timber, rope and available hands before building a broad community pavilion, thoughtful planning in a foothill village'
        scenes[3]='A team dividing a heavy stone load into manageable baskets and helping one another on a mountain path, practical awareness of capacity'
        scenes[9]='Villagers raising a modest sturdy pavilion together with safe ropes and coordinated teamwork, realistic ancient Tamil craftsmanship'
    if job['slug'].startswith('periyarai_'):
        scenes[2]='Young women and men seeking the counsel of respected elders beneath a vast banyan tree, patient attentive group discussion'
        scenes[3]='Experienced farmers walking with younger villagers beside irrigation channels, passing on practical knowledge through gentle demonstration'
        scenes[9]='Three elderly craft mentors teaching a mixed-age group to repair a wooden cart in a shaded courtyard, warm companionship'
    if job['slug'].startswith('arivudaimai_'):
        scenes[2]='A diverse gathering carefully listening to two different viewpoints in an open Tamil council pavilion, thoughtful faces and calm interaction'
        scenes[3]='Women, men and children observing flowing water and planning an irrigation route together, curious practical learning'
        scenes[9]='A village community solving a blocked water channel through careful observation and coordinated work, hopeful shared wisdom'
    if job['slug'].startswith('sittrinam_'):
        scenes[2]='Young adults joining a circle of thoughtful artisans and generous neighbours in a garden courtyard, hopeful ethical companionship'
        scenes[3]='Friends together declining a quarrel and guiding neighbours toward peaceful cooperation beside a lotus pond, calm natural interaction'
        scenes[9]='Families and respectful companions restoring an orchard path together, healthy community bonds and warm afternoon light'
    if job['slug'].startswith('kuttrangadithal_'):
        scenes[2]='A village leader listening humbly as a mixed-age gathering points out a damaged public waterway, accountable respectful discussion'
        scenes[3]='A group sincerely apologising to neighbours and returning misplaced grain baskets, reconciliation without humiliation'
        scenes[9]='The leader and neighbours together repairing the damaged waterway, correction through practical action and shared responsibility'
    if job['slug'].startswith('kelvi_'):
        scenes[2]='Women, men and children listening attentively to an elderly storyteller beneath a palm grove, focused natural faces and varied seating'
        scenes[3]='Young farmers listening carefully while an experienced woman demonstrates a useful irrigation method beside estuary fields'
        scenes[9]='Craft apprentices listening and watching a master weaver demonstrate a traditional loom, a broad mixed-age learning circle'
    if job['slug'].startswith('naadu_'):
        scenes[2]='A broad gathering of farmers, traders and harbour workers exchanging abundant rice, vegetables and woven goods at an ancient Tamil delta harbour, prosperous orderly civic life'
        scenes[3]='Village healers and neighbours caring for families beneath a shady civic garden pavilion, clean water pots and medicinal plants, dignified community wellbeing'
        scenes[9]='A large community maintaining an irrigation sluice beside fertile fields, plentiful flowing water and hopeful shared care'
    if job['slug'].startswith('mannarai_'):
        scenes[2]='A wise Tamil woman and several advisers quietly listening to a ruler in a spacious palace audience courtyard, respectful distance and composed natural body language'
        scenes[3]='Councillors consulting privately in a shaded palace garden before offering considered advice, calm restraint and attentive group interaction'
        scenes[9]='A woman adviser thoughtfully presenting palm-leaf notes to a seated ruler and council at an appropriate moment, dignified cooperative civic leadership'
    if job['slug'].startswith('kuripparithal_'):
        scenes[2]='A circle of neighbours noticing an elderly woman’s quiet concern and listening with attentive empathetic expressions in a canal-side courtyard'
        scenes[3]='A mother, craft worker and neighbours understanding a child’s hesitant gesture and offering gentle help beside a shaded lotus garden, subtle natural expressions'
        scenes[9]='A community council noticing a shy farmer’s unspoken concern and making space for him to speak, considerate faces and restrained gestures'
    if job['slug'].startswith('thoothu_'):
        scenes[2]='A delegation of women and men listening carefully to village representatives before a journey, palm-leaf message held respectfully in a royal forecourt'
        scenes[3]='Travelling envoys and villagers sharing water beside a river crossing, composed patient diplomatic interaction'
        scenes[9]='A woman envoy and accompanying elders delivering a message clearly to a seated council in a broad audience pavilion, attentive listeners and calm respectful gestures'
    if job['slug'].startswith('vinai_seyalvagai_'):
        scenes[2]='A broad group of carpenters, potters, weavers and neighbours planning a harbour storehouse together using wooden models and palm-leaf notes'
        scenes[3]='Craft workers carefully choosing sound timber and preparing tools together in an ancient Tamil workshop courtyard, practical purposeful cooperation'
        scenes[9]='A community completing a sturdy harbour storehouse, women and men carrying baskets and checking finished work, shared satisfaction'
    if job['slug'].startswith('idukkan_'):
        scenes[2]='Neighbours encouraging tired farmers with gentle smiles after difficult field work, dignified warmth and quiet resilience beneath a hill-side pavilion'
        scenes[3]='Families and village workers restoring a storm-damaged garden path together, calm hopeful mutual support without distress or danger'
        scenes[9]='A mixed-age gathering repairing a wooden cart and sharing a light-hearted moment, natural reassuring smiles and practical courage'
    if job['slug'].startswith('solvanmai_'):
        scenes[2]='A Tamil woman and village representatives speaking clearly to a broad gathering in a lakeside public debate pavilion, listeners attentive and respectful'
        scenes[3]='Two groups of neighbours resolving a disagreement through calm eloquent conversation beneath flowering trees, natural thoughtful faces'
        scenes[9]='A mixed-age public circle listening to a young speaker present palm-leaf notes with confidence and care, open dialogue and shared understanding'
    if job['slug'].startswith('vinai_thitpam_'):
        scenes[2]='Stone craft workers and women planners assessing a half-built community pavilion together in a foothill workshop, clear purpose and patient coordination'
        scenes[3]='A broad village team continuing careful stonework despite a difficult task, safe practical tools and mutually encouraging faces'
        scenes[9]='Workers and families celebrating a completed sturdy irrigation terrace after patient shared effort, quiet satisfaction and purposeful teamwork'
    if job['slug'].startswith('vinai_thooymai_'):
        scenes[2]='Women and men checking fair grain measures with traders in a shaded river market court, honest mutual respect and principled exchange'
        scenes[3]='A community returning surplus goods to their rightful owners and offering clean drinking water to travellers, dignified ethical service'
        scenes[9]='A broad gathering tending a public garden and distributing its harvest fairly among families, transparent generous cooperation'
    for i in range(0,12,4):
        prompt='Create exactly FOUR completely distinct cinematic still images in a precise 2x2 grid, with no borders, gutters or labels. Overall landscape canvas 16:9; each quadrant also 16:9. Use case: historical-scene. Tamil Thirukkural film '+job['english']+'. Theme: '+theme+'. Photorealistic painterly film quality, authentic ancient Tamil towns and traditional clothing, realistic anatomy and natural hands. Prefer group gatherings in all human scenes; vary ages, wardrobe, arrangement, activity and camera position. Important faces and actions clear of lower corners for later video overlays. No text, letters, watermark, logo, modern objects, frozen lightning bolts, or foreground incense/lamp overlays. '
        prompt+=' '.join(label+': '+scene+'.' for label,scene in zip(['Top left','Top right','Bottom left','Bottom right'],scenes[i:i+4]))
        prompts.append({'slug':job['slug'],'sheet':i//4+1,'prompt':prompt,'path':str((root/'sheets'/f"{job['slug']}-{i//4+1}.png").resolve())})
    (root/(job['slug']+'-SCENES.json')).write_text(json.dumps(scenes,ensure_ascii=False,indent=2),encoding='utf-8')
(root/'artwork-prompts.json').write_text(json.dumps(prompts,ensure_ascii=False,indent=2),encoding='utf-8')
print(len(prompts),'sheets planned')
