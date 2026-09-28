import json,sys
from pathlib import Path

root=Path(__file__).resolve().parent
if len(sys.argv)==3:
    batch,slug=sys.argv[1:]
    path=root/batch/slug/'manifest.json'
    data=json.loads(path.read_text(encoding='utf-8'))
    data['localQC']={'originalAudioExact':True,'fullDecode':True,'visualReview':'opening, rainy scene and dry successor inspected'}
    data['publicationStatus']='ready; upload deferred by user'
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
rows=[]
for number in range(2,7):
    batch=root/f'thirukkural-batch-{number:02d}'
    for path in sorted(batch.glob('*/manifest.json')):
        data=json.loads(path.read_text(encoding='utf-8'))
        output=path.parent/data['output']
        checked=data.get('localQC',{}).get('visualReview','pending')!='pending'
        status='Ready for later upload' if checked else 'Rendering or QC pending'
        rows.append({'title':data['title'],'sourceId':data['sourceId'],'output':str(output),'status':status,'manifest':str(path)})
(root/'THIRUKKURAL-UPLOAD-QUEUE.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lines=['# Thirukkural local upload queue','',"Uploads are deferred by the user while YouTube's daily upload limit resets. Check the live channel for duplicate publications/drafts before upload. Add Discography and Thirukkural Master Collection. YouTube copyright and Community Guidelines checks must complete before public release.",'', '| Film | Source ID | Status | MP4 |','| --- | --- | --- | --- |']
for row in rows:
    output=Path(row['output'])
    rel=output.relative_to(root).as_posix()
    title=row['title'].replace('|','—')
    lines.append(f"| {title} | {row['sourceId']} | {row['status']} | [Video]({rel}) |")
lines+=['','Image generation: built-in imagegen. Prompt sets and source sheets are saved within each batch. Each film uses twelve new images, wide opening, bottom-left channel logo, paired dheepam and four burning incense sticks per side with animated smoke, and localized drizzle/lightning. Original audio is preserved.']
(root/'THIRUKKURAL-UPLOAD-QUEUE.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('queue',len(rows),'ready',sum(r['status']=='Ready for later upload' for r in rows))
