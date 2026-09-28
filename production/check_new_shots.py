import hashlib,json,sys
from pathlib import Path
root=Path(__file__).resolve().parent
batch=(root/sys.argv[1]).resolve()
new=list(batch.glob('*/S[0-9][0-9].png'))
hashes=[hashlib.sha256(p.read_bytes()).hexdigest() for p in new]
old={hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('S[0-9][0-9].png') if batch not in p.parents}
report={'shots':len(new),'distinct':len(set(hashes)),'reused':len(set(hashes)&old)}
print(report)
expected=int(sys.argv[2]) if len(sys.argv)>2 else 36
assert len(new)==expected and report['distinct']==expected and report['reused']==0
(batch/'uniqueness.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
