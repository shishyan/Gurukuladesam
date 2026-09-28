"""Render the three jobs in a batch and verify the finished files."""
import argparse
import json
import subprocess
import sys
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('batch',type=Path)
args = parser.parse_args()
root = args.batch.resolve()
production = root.parent
subprocess.run([sys.executable,str(production/'build-backlog-batch.py'),str(root)],check=True)
jobs = json.loads((root/'jobs.json').read_text(encoding='utf-8'))['songs']
for job in jobs:
    folder = root/job['slug']
    manifest = folder/'manifest.json'
    data = json.loads(manifest.read_text(encoding='utf-8'))
    if not (folder/'qc.json').exists():
        subprocess.run([sys.executable,str(root/'render.py'),str(manifest)],check=True)
subprocess.run([sys.executable,str(root/'qc.py')],check=True)
subprocess.run([sys.executable,str(production/'update-publication-queue.py')],check=True)
