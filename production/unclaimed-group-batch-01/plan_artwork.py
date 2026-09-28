import json
from pathlib import Path
root=Path(__file__).resolve().parent
scenes={
'potri_thiru_agaval_2026':[
'Ultra-wide dawn panorama of a Tamil river valley, distant Shiva temple and a large community pilgrimage approaching through mist; powerful orchestral opening, expansive sky and landscape',
'Wide gathering of families arranging jasmine and bilva offerings in a sunlit granite courtyard',
'A circle of Tamil devotional singers seated naturally beneath a banyan tree, veena and mridangam accompanists, elders and children listening',
'Respectful side view of a garlanded Shiva lingam sanctum with a congregation beyond the doorway',
'Women and men together preparing vegetarian prasadam in an open temple kitchen with clay pots',
'Village elders teaching children a devotional rhythm in a shaded pillared pavilion',
'Wet outdoor causeway leading to a temple tank under dark monsoon clouds, families sheltering under woven palm umbrellas; no drawn rain streaks or lightning bolts',
'Dry enclosed granite mandapam, a large group listening peacefully to a teacher beside palm-leaf manuscripts, warm golden light; absolutely no rain',
'Wide riverbank gathering at midday, devotees washing hands at stone steps with safe natural spacing',
'Community sharing food with travellers beneath neem trees, generous welcoming interaction',
'Flower vendors and families exchanging fresh garlands in a temple street, warm afternoon light',
'An open-air music gathering beside a lotus pond, varied Tamil traditional clothing and joyful respectful faces',
'Wide elevated view of many devotees circling a shaded temple courtyard, sculpted granite architecture',
'Small community tending saplings in a village grove, children carrying water vessels with elders',
'Families offering fresh flowers at a riverside shrine, wide lateral view, soft blue evening',
'Musicians and listeners together beneath a carved festival pavilion, lamp-lit amber interior',
'Devotees cleaning a temple tank stone stairway together, thoughtful community service',
'An elderly couple and neighbouring families exchanging bowls of food at a village threshold',
'A large congregation watching a priest present a flower plate beside an open sanctum entrance, dignified composition',
'Community procession across a field path toward a distant gopuram at sunset, new silhouette and camera angle',
'A choir of women, men and children beneath a terracotta veranda with evening lamps',
'Temple courtyard gathering listening in stillness under an indigo sky, many naturally spaced people',
'Wide view of warm-lit shrine doorways and families departing along a stone passage, serenity',
'Ultra-wide night panorama of the temple beside a reflective river, a community gathering as small silhouettes beneath stars, peaceful closing'],
'thiruvothur_pathigam_ii':[
'Ultra-wide sunrise view across Tamil palmyra groves toward a granite temple, dozens of villagers gathering along a broad earth path, expansive orchestral opening',
'Families carrying flower baskets through a tall carved stone gateway, wide ground-level composition',
'A gathering of Tamil women and children weaving palm-leaf offering baskets in a shaded village courtyard',
'Garlanded Shiva lingam inside an authentic granite shrine, community seen respectfully beyond the threshold',
'Devotional singers and percussionists gathered beneath tall palmyra trees, wide natural candid scene',
'A community distributing cooked vegetarian food at a temple-side veranda, warm welcoming interaction',
'Wet outdoor palmyra grove pathway near a temple under soft storm clouds, villagers sharing palm umbrellas; no visible lightning bolts or artificial rain streaks',
'Dry enclosed temple hall, families gathered around an elder reciting from palm-leaf manuscripts, clear warm lamplight; no indoor rain',
'Temple musicians accompanied by a seated congregation in a carved open pavilion, side perspective',
'Families and neighbours bringing fresh garlands together through a tree-lined sacred street at dusk',
'Wide communal evening worship at the courtyard shrine, soft practical lamps and serene faces',
'Ultra-wide moonlit temple silhouette beyond quiet palm groves, a community resting in the courtyard, spacious peaceful closing'],
'thiruvothur_pathigam_iii':[
'Ultra-wide golden dawn panorama of a Tamil village and palmyra-lined temple lake, a broad community arriving by several paths, powerful orchestral scale',
'Villagers gathering around a decorated temple chariot in a spacious granite courtyard, natural varied poses',
'Women and men preparing flower arrangements together under a woven canopy, children helping elders',
'Respectful close-medium view of a flower-adorned Shiva lingam with devotees softly visible through the shrine opening',
'Large seated circle of Tamil devotional singers beside a carved pillared hall, veena and hand drums',
'Neighbouring families welcoming pilgrims and sharing fruit in a sunlit temple street',
'Rain-darkened outdoor temple lake embankment beneath thick grey clouds, groups sheltering near palm trees with umbrellas; no fixed lightning bolts or drawn streaks',
'Dry indoor hall with families listening to a wise elder, carved stone columns and warm lamps, absolutely no rain',
'A community carrying flower offerings along a narrow village lane viewed from a balcony, varied clothing',
'Elders and children planting a small palm sapling together near the temple boundary, late golden sunlight',
'A wide evening congregation facing an illuminated temple entrance, musicians at the side, tranquil shared devotion',
'Ultra-wide sunset over palmyra silhouettes and temple lake, groups departing gently along the shore, peaceful closing']}
prompts=[]
jobs=json.loads((root/'jobs.json').read_text(encoding='utf-8'))
for job in jobs['songs']:
    ss=scenes[job['slug']]
    for i in range(0,len(ss),4):
        prompt='Create a production contact sheet with exactly FOUR completely distinct cinematic images in a precise 2x2 grid with no borders or gutters. Overall canvas landscape 16:9, each quadrant 16:9. Use case: photorealistic-natural. Tamil devotional film '+job['english']+'. Authentic Tamil granite temple and village setting; cinematic painterly photorealism, realistic anatomy and natural human interaction. Most images show communities or families, not isolated portraits. Diverse ages in traditional Tamil clothing, dignified devotional gatherings. No text, lettering, logos, watermarks, visible lightning bolts, or foreground incense/lamp overlays; the film adds its own corner effects. Keep important faces and actions clear of lower corners. Every quadrant must differ in setting, lighting, arrangement, activity and camera position. '
        prompt+=' '.join(label+': '+scene+'.' for label,scene in zip(['Top left','Top right','Bottom left','Bottom right'],ss[i:i+4]))
        prompts.append({'slug':job['slug'],'sheet':i//4+1,'prompt':prompt,'path':str((root/'sheets'/f"{job['slug']}-{i//4+1}.png").resolve())})
    (root/(job['slug']+'-SCENES.json')).write_text(json.dumps(ss,ensure_ascii=False,indent=2),encoding='utf-8')
(root/'artwork-prompts.json').write_text(json.dumps(prompts,ensure_ascii=False,indent=2),encoding='utf-8')
print(len(prompts),'sheets;',sum(len(v) for v in scenes.values()),'unique scenes planned')
