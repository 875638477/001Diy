from pathlib import Path
import hashlib,json
r=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonF_stack_artwork_correction_20261019\review')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
files=[{'path':str(p.relative_to(r)).replace('\\','/'),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(r.rglob('*')) if p.is_file() and p.name!='artifact_manifest.json']
manifest={'scope':'Independent read-only correction review files only; excludes this manifest and parent/native artifacts.','files':files}
(r/'artifact_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
report=json.loads((r/'review.json').read_text(encoding='utf-8'))
native={p.name:sha(p) for p in sorted((r.parent/'current').glob('*.brd'))}
print(json.dumps({'status':report['status'],'checks':report['checks'],'failed':report['failed'],'reviewSHA256':sha(r/'review.json'),'manifestSHA256':sha(r/'artifact_manifest.json'),'manifestFiles':len(files),'native':native},ensure_ascii=False))
