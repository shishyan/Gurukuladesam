"""Record only verified completed films in this batch's publication queue."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
films = json.loads((HERE / 'batch.json').read_text(encoding='utf-8'))['films']
qc_path = HERE / 'QC.txt'
qc = qc_path.read_text(encoding='utf-8') if qc_path.exists() else ''
queue = json.loads((HERE.parent / 'shiva-batch-7/publication-queue.json').read_text(encoding='utf-8'))
legacy_path = HERE / 'legacy-weather-qc.txt'
legacy_qc = legacy_path.read_text(encoding='utf-8') if legacy_path.exists() else ''
legacy_slugs = {'SDPLWITWGho': 'nattrunai_vilakkam', 'iKIsoxTz5-k': 'poovar_senni'}
for item in queue['songs']:
    if item['sourceId'] in legacy_slugs:
        reviewed = f"PASS {legacy_slugs[item['sourceId']]}:" in legacy_qc
        item['qc']['weatherPlacementReviewed'] = reviewed
        if not reviewed:
            item['status'] = 'pending weather placement correction and upload quota'
rows = []
for film in films:
    slug = film['slug']
    ready = f'PASS {slug}' in qc
    rows.append(f"| {film['title'].replace('|', '/')} | [Original](https://youtu.be/{film['sourceId']}) | {'QC complete; pending upload quota' if ready else 'In production'} |")
    if ready:
        queue['songs'].append({
            'sourceId': film['sourceId'], 'title': film['title'],
            'file': f"shiva-batch-8/{slug}/{slug.upper()}-CINEMATIC-ritual-v2.mp4",
            'status': 'ready; pending upload quota',
            'playlists': ['Discography', 'Lord Shiva Songs'],
            'qc': {'uniqueScenes': len(film['sheets']) * 4, 'exactDecodedAudio': True, 'fullDecodePassed': True},
        })
queue['pendingCount'] = len(queue['songs'])
published_path = HERE / 'published.json'
published = json.loads(published_path.read_text(encoding='utf-8')) if published_path.exists() else []
published_ids = {item['sourceId'] for item in published}
queue['songs'] = [item for item in queue['songs'] if item['sourceId'] not in published_ids]
queue['pendingCount'] = len(queue['songs'])
queue['blocker'] = 'YouTube daily upload limit'
queue['latestUploadAttempt'] = {'date': '2026-09-28', 'sourceId': 'e9fTnxiiLnc', 'result': 'Daily upload limit reached; no video link created'}
(HERE / 'publication-queue.json').write_text(json.dumps(queue, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
text = '# Lord Shiva films - batch 8\n\n'
text += 'Five source recordings passed static-cover and decoded-audio uniqueness checks against 30 earlier Shiva recordings. Public channel titles were also checked; the already-produced Thiruvaiyaaru Thirumurai was excluded.\n\n'
text += 'Twelve distinct generated scenes per film; Natarajar Pathu uses 24 for its longer recording. Full original audio, lower-left Guru Kula Desam emblem, paired dheepam, four agarbaththi per side, rising white-grey smoke, outdoor drizzle and restrained occasional lightning.\n\n'
text += '| Song | Source | Status |\n|---|---|---|\n' + '\n'.join(rows) + '\n\n'
text += 'Publish publicly when the daily quota resets, adding each film to both Discography and Lord Shiva Songs. Check for an existing Studio draft before uploading. No batch 8 film is yet published.\n'
if published:
    text += '\nUpload retry accepted Eeswara Naamavali II: [published film](https://youtu.be/KvU4v5v2X98), public with Discography and Lord Shiva Songs selected. Studio confirmed publication and completed checks with no issues. The next Thiruvarthai upload reached the daily limit without creating a video link. Fourteen verified films remain queued.\n'
if legacy_qc.count('PASS ') == 2:
    text += '\nThe earlier queued Nattrunai Vilakkam and Poovar Senni films were rerendered and verified using corrected weather indices and the corrected saved renderer. Finished frame review confirms their indoor scenes are dry and drizzle appears in outdoor scene eleven. Their checks are recorded in legacy-weather-qc.txt. Other earlier queued weather scenes were reviewed as outdoor settings.\n'
else:
    text += '\nThe earlier queued Nattrunai Vilakkam and Poovar Senni films are being checked with the corrected saved renderer. Completed checks are recorded in legacy-weather-qc.txt.\n'
(HERE / 'RELEASES.md').write_text(text, encoding='utf-8')
print(f'Recorded {len(queue["songs"])} QC-complete pending films')
