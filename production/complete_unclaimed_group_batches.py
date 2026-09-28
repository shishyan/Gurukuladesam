import json,datetime
from pathlib import Path
root=Path(__file__).resolve().parent
batches=sorted(p for p in root.glob('unclaimed-group-batch-*') if (p/'ready.json').exists())
rows=[]
for batch in batches:
    ready=json.loads((batch/'ready.json').read_text(encoding='utf-8'))
    unique=json.loads((batch/'uniqueness.json').read_text(encoding='utf-8'))
    assert unique['reused']==0 and unique['shots']==unique['distinct']
    assert not json.loads((batch/'ownership-check.json').read_text(encoding='utf-8'))['conflicts']
    for r in ready['songs']:
        assert Path(r['output']).is_file()
        manifest=json.loads((Path(r['output']).parent/'manifest.json').read_text(encoding='utf-8'))
        rows.append({**r,'batch':batch.name,'publicationStatus':manifest.get('publicationStatus','Ready for upload'),'youtubeVideoId':manifest.get('youtubeVideoId')})
assert rows and len({r['sourceId'] for r in rows})==len(rows)
report={'completedAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'Finished exact-recording films with recorded YouTube publication status','filmCount':len(rows),'sceneCount':sum(r['scenes'] for r in rows),'minutes':round(sum(r['durationSeconds'] for r in rows)/60,2),'scope':'These exact recordings had no prior start in shared production records. Other versions of their compositions or chapters already have films. Audio checks found no exact or near duplicate among available comparison sources.','reviewLimit':'All generated sheets and opening/wet/dry rendered samples inspected; exact original decoded audio, full video decode and no black passages of 0.5s or longer verified. Full human playback and exact lyric timing are not claimed.','songs':rows}
(root/'UNCLAIMED-GROUP-COMPLETION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
md=f"# Previously unstarted recordings — completed upload queue\n\n{len(rows)} full-song films, in {len(batches)} batches of three. The user authorized resuming uploads. Recheck public videos and Studio drafts for duplicates before each release.\n\n"+report['scope']+'\n\n| Song | Source | Finished MP4 | Publication |\n| --- | --- | --- | --- |\n'
for r in rows:
    movie=Path(r['output']).relative_to(root).as_posix()
    status=r['publicationStatus']
    if r['youtubeVideoId']:status+=f" [YouTube](https://www.youtube.com/watch?v={r['youtubeVideoId']})"
    song_title=r['title'].replace('|', '&#124;')
    md+=f"| {song_title} | [{r['sourceId']}](https://www.youtube.com/watch?v={r['sourceId']}) | [Open film]({movie}) | {status} |\n"
md+=f"\n**{report['sceneCount']} unique fresh scenes; {report['minutes']} minutes of complete original audio.** Wide openings, group gatherings, bottom-left channel emblem, dheepam and agarbaththi smoke, with selected outdoor drizzle and lightning illumination.\n\n{report['reviewLimit']}\n\nArtwork and final prompts: "+', '.join(f'[{b.name} prompts]({b.name}/artwork-prompts.json)' for b in batches)+'. All assets were generated using built-in image_gen and copied into their batch folders.\n'
(root/'UNCLAIMED-GROUP-UPLOAD-QUEUE.md').write_text(md,encoding='utf-8')
print('COMPLETE:',len(rows),'films;',report['sceneCount'],'scenes;',report['minutes'],'minutes;',sum(r['publicationStatus']=='Published' for r in rows),'published')
