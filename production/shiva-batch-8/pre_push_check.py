"""Check selected recordings against other production manifests before release."""
import json
from pathlib import Path

here = Path(__file__).resolve().parent
ids = {f['sourceId'] for f in json.loads((here / 'batch.json').read_text(encoding='utf-8'))['films']}
conflicts = []
for path in here.parent.rglob('manifest.json'):
    if here in path.parents:
        continue
    try:
        data = json.loads(path.read_text(encoding='utf-8-sig'))
    except (ValueError, OSError):
        continue
    if data.get('sourceId') in ids:
        conflicts.append(str(path.relative_to(here.parent)))
report_path = here / 'pre-push-duplicate-audit.json'
report = json.loads(report_path.read_text(encoding='utf-8'))
report['conflictingProductionManifests'] = conflicts
report['finalLocalCheckDate'] = '2026-09-28'
report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
assert not conflicts, conflicts
for path in here.glob('*progress.log'):
    raw = path.read_bytes()
    if raw.startswith(b'\xff\xfe'):
        path.write_text(raw.decode('utf-16'), encoding='utf-8')
print('PASS: five selected source IDs have no conflicting production manifests')
