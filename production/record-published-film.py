"""Record an externally verified public release in its existing batch ledger."""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('source_id')
parser.add_argument('public_url')
args = parser.parse_args()
assert args.public_url.startswith('https://www.youtube.com/watch?v=')
production = Path(__file__).resolve().parent
matches = []
for path in [production/'batch-sept-28-10/ready.json', *production.glob('thirukkural-backlog-*/ready.json'), *production.glob('thiruvarutpa-backlog-*/ready.json')]:
    data = json.loads(path.read_text(encoding='utf-8'))
    for song in data['songs']:
        if song['sourceId'] == args.source_id and not song.get('uploadSuppressed'):
            matches.append((path, data, song))
assert len(matches) == 1, f'Expected one active owner, found {len(matches)}'
path, data, song = matches[0]
song.update(publishedUrl=args.public_url, publicationVerified=True,
            publishedAtUtc=datetime.now(timezone.utc).isoformat(), status='published and public playback verified')
path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(f'Recorded {args.source_id}: {args.public_url}')
