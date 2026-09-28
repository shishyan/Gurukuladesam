from pathlib import Path
p=Path(__file__).resolve().parent/'start_group_batch08.py'
s=p.read_text(encoding='utf-8').replace('batch-08','batch-09').replace("replace('07','08')","replace('07','09')")
start=s.index('spec=');end=s.index('\nconflicts=',start)
s=s[:start]+"spec="+repr([
('q2oGlYiV-qg','solvanmai_remix','Solvanmai Remix','eloquent truthful speech that builds understanding and cooperation','an ancient Tamil lake city with open public debating pavilions and flowering gardens'),
('J-mAIpyxy4A','vinai_thitpam_remix','Vinai Thitpam Remix','resolute purpose and perseverance in completing worthwhile work','an ancient Tamil foothill craft settlement with stone workshops and terraced orchards'),
('XRizXIUU57g','vinai_thooymai_remix','Vinai Thooymai Remix','ethical purity of action, fairness and principled service','an ancient Tamil river market town with shaded trade courts and fertile community gardens')])+s[end:]
s=s.replace('assert not batch.exists()',"assert not (batch/'jobs.json').exists()")
s=s.replace('batch.mkdir();(batch/\'source\').mkdir();(batch/\'sheets\').mkdir()',"batch.mkdir(exist_ok=True);(batch/'source').mkdir(exist_ok=True);(batch/'sheets').mkdir(exist_ok=True)")
s=s.replace("'quiet':True,'no_warnings':True,","'quiet':True,'no_warnings':True,'noprogress':True,")
exec(compile(s,str(p),'exec'))
