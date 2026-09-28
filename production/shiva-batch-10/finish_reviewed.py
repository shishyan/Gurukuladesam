import concurrent.futures, json, subprocess, sys
from pathlib import Path
here=Path(__file__).resolve().parent
films=json.loads((here/'batch.json').read_text(encoding='utf-8'))['films']
def finish(film):
    slug=film['slug'];folder=here/slug;manifest=folder/'manifest.json'
    existing=(here/'QC.txt').read_text(encoding='utf-8-sig') if (here/'QC.txt').exists() else ''
    for line in existing.splitlines():
        if line.startswith('PASS '+slug+':') and 'no long black passages' in line:
            return line+'\n'
    assert (folder/'scene-review.jpg').exists()
    assert slug in json.loads((here/'visual-review.json').read_text(encoding='utf-8'))['acceptedSlugs']
    data=json.loads(manifest.read_text(encoding='utf-8'))
    if not (folder/data['output']).exists():
        print('RENDER_START',slug,flush=True)
        subprocess.run([sys.executable,'-u',str(here/'render_fast.py'),str(manifest)],check=True)
    result=subprocess.run([sys.executable,'-X','utf8',str(here/'verify.py'),slug],check=True,capture_output=True,encoding='utf-8')
    print(result.stdout,flush=True)
    return result.stdout
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    results=list(pool.map(finish,films))
(here/'QC.txt').write_text(''.join(results),encoding='utf-8')
assert len(results)==5
print('BATCH_COMPLETE five verified films',flush=True)
