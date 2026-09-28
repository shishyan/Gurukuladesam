import json
import shutil
from pathlib import Path

root = Path(__file__).resolve().parent
changes = [
    ('parasiva_vanakkam', 3, 'siva_pathi_vilakkam', 'S10.png'),
    ('siva_pathi_vilakkam', 0, 'parasiva_vanakkam', 'S11.png'),
    ('thiruchathana_deiva_thiram', 0, 'siva_pathi_vilakkam', 'S07.png'),
]
for name, index, source, image in changes:
    folder = root / name
    shutil.copyfile(root / source / image, folder / 'GROUP-SCENE-v2.png')
    data = json.loads((folder / 'manifest.json').read_text(encoding='utf-8'))
    data['output'] = data['output'].replace('-v1.mp4', '-groups-v2.mp4')
    data['shots'][index].update(image='GROUP-SCENE-v2.png', role='community learning gathering', artOrigin='existing project imagegen artwork', assetSource=str(root / source / image))
    data['groupSceneRevision'] = {'scene': index + 1, 'reason': 'Add a community gathering in place of a lone portrait', 'source': str(root / source / image)}
    (folder / 'manifest-groups-v2.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
shutil.copyfile(root.parent / 'thirukkural-backlog-08/qc-groups-v2.py', root / 'qc-groups-v2.py')
