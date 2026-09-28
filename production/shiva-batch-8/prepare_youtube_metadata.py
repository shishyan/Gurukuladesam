"""Build ready-to-use publication metadata from the source-backed titles."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
batch = json.loads((HERE / 'batch.json').read_text(encoding='utf-8'))
films = batch['films']
catalog = {item['id']: item for item in json.loads((HERE.parent / 'playlist-audit/catalog-2026-09-26.json').read_text(encoding='utf-8'))['songs']}
names = {
    'vendumey_iththanaiyum': 'Vendumey Iththanaiyum (Thiruvempavai)',
    'pidiyathan_uruvumai': 'Pidiyathan Uruvumai',
    'anbu_maalai_ii': 'Anbu Maalai II (Thiruvarutpa)',
    'thiruvothur_pathigam': 'Thiruvothur Pathigam',
    'natarajar_pathu': 'Natarajar Pathu (Thiruvasagam)',
}
items = []
for film in films:
    english_title = names[film['slug']].split(' (')[0]
    title = catalog[film['sourceId']]['title'] + f' | {english_title} Cinematic Shiva Film'
    assert len(title) <= 100, title
    description = (
        f"{names[film['slug']]} - a full-length Lord Shiva devotional film from Guru Kula Desam.\n\n"
        "The original song accompanies temple journeys, sacred offerings and quiet moments of devotion.\n\n"
        f"Original song and audio: https://youtu.be/{film['sourceId']}\n"
        "Music: Guru Kula Desam\n\n"
        "#GuruKulaDesam #LordShiva #TamilDevotional"
    )
    items.append({
        'slug': film['slug'], 'sourceId': film['sourceId'],
        'title': title, 'description': description,
        'playlists': ['Discography', 'Lord Shiva Songs'],
        'visibility': 'public',
    })
    film['title'] = title
    manifest_path = HERE / film['slug'] / 'manifest.json'
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
        manifest['title'] = title
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
(HERE / 'batch.json').write_text(json.dumps(batch, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
(HERE / 'youtube-metadata.json').write_text(json.dumps(items, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Prepared five titles, descriptions and playlist assignments')
