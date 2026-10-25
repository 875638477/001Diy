from pathlib import Path
import hashlib,json,datetime
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonJK_51_59_20261022');M=R/'native/native56_artifact_manifest.json';roots=[R/'native',R/'source/env_oO_chain',R/'source/native56_official',R/'source/j55_official',R/'source/j55_readback_helpers',R/'source/newstack_official',R/'eco/DE_REPLAY_ONLY'];roots+=list((R/'logs').glob('native_*'));roots+=list((R/'exports').glob('native_*'));roots+=list((R/'exports').glob('J55_corrected_*'));roots+=list((R/'exports').glob('supplement_*'));roots+=list((R/'exports').glob('newstack_*'));roots+=list((R/'exports').glob('devicevalues_*'))
files=set()
for root in roots:
 assert root.resolve().is_relative_to(R.resolve())
 for p in root.rglob('*'):
  if p.is_file() and p!=M and '__pycache__' not in p.parts:files.add(p)
items=[{'path':p.relative_to(R).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest().upper()} for p in sorted(files)]
report={'status':'SEALED_NATIVE_TASK_OWNED_ARTIFACTS','createdUTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'lessonRoot':str(R),'fileCount':len(items),'totalBytes':sum(x['bytes'] for x in items),'scope':'This native executor owned scripts/source snapshots/private scratch+savedboards/native logs/CAM/deviceVALUE/ECO replay. Excludes itself, other agents review/assembly/audits, root mutable mainnotes/EDA/policy. Parent supplies total lesson inventory.','files':items}
M.write_text(json.dumps(report,indent=2),encoding='utf8')
for x in items:assert hashlib.sha256((R/x['path']).read_bytes()).hexdigest().upper()==x['sha256']
print(json.dumps({'fileCount':len(items),'totalBytes':report['totalBytes'],'manifest':str(M),'sha256':hashlib.sha256(M.read_bytes()).hexdigest().upper(),'verifiedAll':True}))
