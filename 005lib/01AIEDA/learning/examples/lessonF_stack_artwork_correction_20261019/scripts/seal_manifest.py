from pathlib import Path
import hashlib,json
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonF_stack_artwork_correction_20261019')
out=R/'artifact_manifest.json'
files=[]
for p in sorted(R.rglob('*')):
 if not p.is_file() or p==out or p.relative_to(R).parts[0]=='review':continue
 files.append({'path':p.relative_to(R).as_posix(),'size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest().upper()})
data={'status':'SEALED_NATIVE_CORRECTION_EVIDENCE','date':'2026-10-19 Asia/Shanghai','root':str(R),'fileCount':len(files),'scope':'Correction-owned files only. Excludes manifest itself, reviewer-owned review subtree and mutable parent learning records. Original canonical source identities remain in input_manifest.json and validation.json.','files':files}
out.write_text(json.dumps(data,indent=2),encoding='utf8')
assert all(hashlib.sha256((R/x['path']).read_bytes()).hexdigest().upper()==x['sha256'] for x in files)
print(json.dumps({'status':data['status'],'files':len(files),'manifestSHA256':hashlib.sha256(out.read_bytes()).hexdigest().upper()}))
