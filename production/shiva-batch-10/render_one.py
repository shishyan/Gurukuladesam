import subprocess,sys
from pathlib import Path
here=Path(__file__).resolve().parent
slug=sys.argv[1]
subprocess.run([sys.executable,'-u',str(here/'render_fast.py'),str(here/slug/'manifest.json')],check=True)
r=subprocess.run([sys.executable,'-X','utf8',str(here/'verify.py'),slug],check=True,capture_output=True,encoding='utf-8')
(here/slug/'QC.txt').write_text(r.stdout,encoding='utf-8')
print(r.stdout,flush=True)
print('FILM_COMPLETE',slug,flush=True)
