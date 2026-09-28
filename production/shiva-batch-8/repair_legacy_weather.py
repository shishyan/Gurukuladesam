"""Correct rain placement in two unpublished films, resuming completed checks."""
import subprocess
import sys
import json
import concurrent.futures
from pathlib import Path

HERE = Path(__file__).resolve().parent
BATCH6 = HERE.parent / 'shiva-batch-6'
checkpoint = HERE / 'legacy-weather-qc.txt'
existing = checkpoint.read_text(encoding='utf-8') if checkpoint.exists() else ''

def correct(slug):
    manifest_path = BATCH6 / slug / 'manifest.json'
    assert json.loads(manifest_path.read_text(encoding='utf-8'))['rainShots'] == [10]
    if f'PASS {slug}:' in existing:
        return slug, None
    print(f'CORRECTION_START {slug}', flush=True)
    subprocess.run([sys.executable, '-u', str(BATCH6 / 'render_fast.py'), str(BATCH6 / slug / 'manifest.json')], check=True)
    result = subprocess.run([sys.executable, '-X', 'utf8', str(BATCH6 / 'verify.py'), slug], check=True, capture_output=True, encoding='utf-8')
    return slug, result.stdout

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    futures = [pool.submit(correct, slug) for slug in ['nattrunai_vilakkam', 'poovar_senni']]
    for future in concurrent.futures.as_completed(futures):
        slug, report = future.result()
        if report:
            print(report, flush=True)
            with checkpoint.open('a', encoding='utf-8') as handle:
                handle.write(report)
        (BATCH6 / 'weather-correction-qc.txt').write_text(checkpoint.read_text(encoding='utf-8'), encoding='utf-8')
        subprocess.run([sys.executable, str(HERE / 'update_release_queue.py')], check=True)
        print(f'CORRECTION_DONE {slug}', flush=True)
print('LEGACY_CORRECTIONS_COMPLETE', flush=True)
