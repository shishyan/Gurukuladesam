import json,subprocess,sys
from pathlib import Path
root=Path(__file__).resolve().parent
batch=root/sys.argv[1];slug=sys.argv[2]
subprocess.run([sys.executable,str(batch/'render.py'),str(batch/slug/'manifest.json'),'--ritual-effects'],check=True)
subprocess.run([sys.executable,str(root/'verify_queue_film.py'),sys.argv[1],slug],check=True)
print('RENDER AND TECHNICAL QC COMPLETE',sys.argv[1],slug,flush=True)
