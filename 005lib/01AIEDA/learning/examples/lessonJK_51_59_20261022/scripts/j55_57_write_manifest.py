"""Snapshot selected J55/K57 evidence files and exact hashes; read existing source hashes, no CAD operation."""
from pathlib import Path
import json,hashlib,datetime,re
R=Path('D:/001DIY/005lib/01AIEDA');J=R/'learning/examples/lessonJK_51_59_20261022';note=R/'learning/notes/lessonJK_55_57_20261022.md';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
files=set(p for p in (J/'assembly').rglob('*') if p.is_file())
for pattern in ['j55_*.json','j55_*.csv','j55_*.md','j57_*.json']:files.update(p for p in (J/'audits').glob(pattern) if p.name!='j55_57_artifact_manifest.json')
files.update((J/'scripts').glob('j55*.py'));files.update([J/'native/j55_apply_core.il',J/'native/j55_plan_static.il',J/'eco/K58_DE_native_replay_reference.json',note]);files.update((J/'source/j55_official').glob('*'));files.update(p for p in [J/'native/j55_apply_core_v2.il',J/'native/j55_outer.il',J/'native/run_j55.py',J/'native/j55_source_manifest.json'] if p.exists())
refs=[]
for l in re.findall(r'\[[^\]]+\]\(([^)]+)\)',note.read_text(encoding='utf-8-sig')):
 if l.startswith(('http://','https://')):continue
 p=note.parent/l;refs.append(dict(target=l,exists=p.exists()));assert p.exists(),l
summary=json.loads((J/'audits/j55_57_summary_b019.json').read_text());sources=summary['sourceHashes']
for s in sources:assert sha(Path(s['path']))==s['sha256'],s['path']
# Current corrective native products and original fresh evidence are references, not invented derived results.
freshInput=J/'audits/j55_fresh_inputs.json';nativeRefs=[]
if freshInput.exists():
 for variant,data in json.loads(freshInput.read_text(encoding='utf-8-sig')).items():
  board=Path(data['board']);log=Path(data['log'])
  if board.exists():nativeRefs.append(dict(variant=variant,path=str(board),sha256=sha(board)))
  for fn in ['launch.json','board_instance_texts.tsv','g_actual_geometry.tsv','jk55_instance_properties.tsv','components.tsv','component_pins.tsv','stackup_full.tsv','films_full.tsv','placed_pins.tsv','physical_pad_layers.tsv','hi_network_summary.txt','hi_reopen_endpoint_proofs.txt']:
   q=log/fn
   if q.exists():nativeRefs.append(dict(variant=variant,path=str(q),sha256=sha(q)))
new=J/'audits/j55_corrected_independent_summary.json';stage='NATIVE_CORRECTION_FRESH_REVIEW_COMPLETE_TRAINING_ONLY' if new.exists() else 'BASELINE_REVIEW_AND_CSV_COMPLETE_AWAITING_NATIVE_CORRECTION'
out=dict(status=stage,createdUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),scope='Selected J55/K57 baseline/current evidence, core scripts and note; all files inside01AIEDA. Training not assembly/fabrication release. Does not enumerate other agents entire JK outputs or sealed HI history.',files=[dict(path=str(p),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(files)],sourceHashes=sources,nativeCorrectionSources=nativeRefs,noteLinkChecks=refs)
p=J/'audits/j55_57_artifact_manifest.json';p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
for f in out['files']:assert sha(Path(f['path']))==f['sha256']
print('manifest',len(out['files']),'file hashes matched;',len(refs),'local note links exist; status',stage)
