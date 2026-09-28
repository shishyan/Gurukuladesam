"""Render and verify the visually reviewed films sequentially."""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
QC = HERE / 'QC.txt'

def read_qc():
    if not QC.exists():
        return ''
    raw = QC.read_bytes()
    return raw.decode('utf-16' if raw.startswith(b'\xff\xfe') else 'utf-8-sig')

for slug in ['pidiyathan_uruvumai', 'vendumey_iththanaiyum', 'anbu_maalai_ii', 'thiruvothur_pathigam', 'natarajar_pathu']:
    if f'PASS {slug}:' in read_qc():
        continue
    print(f'RENDER_START {slug}', flush=True)
    subprocess.run([sys.executable, '-u', str(HERE / 'render_fast.py'), str(HERE / slug / 'manifest.json')], check=True)
    result = subprocess.run([sys.executable, '-X', 'utf8', str(HERE / 'verify.py'), slug], check=True, capture_output=True, encoding='utf-8')
    print(result.stdout, flush=True)
    with QC.open('a', encoding='utf-8') as handle:
        handle.write(result.stdout)
    subprocess.run([sys.executable, str(HERE / 'update_release_queue.py')], check=True)
    print(f'QC_DONE {slug}', flush=True)
assert read_qc().count('PASS ') == 5
print('BATCH_COMPLETE five full-length films passed QC', flush=True)
