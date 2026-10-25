from pathlib import Path
import json,hashlib,shutil
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');records=R/'source/b016_frozen_records';records.mkdir(exist_ok=True)
for p in [R/'native/b016_construction_notes.md',R/'native/README.md']:
 d=records/p.name;assert not d.exists();shutil.copyfile(p,d)
paths=set()
for root in [R/'logs',R/'source/batch_snapshots',R/'source/readback_snapshots',R/'source/engineering_snapshots',R/'native_work']:
 for folder in root.iterdir():
  if folder.is_dir() and ('b016' in folder.name or folder.name.startswith('b016_')):
   paths.update(p for p in folder.rglob('*') if p.is_file())
for root in [R/'source/api_b016',R/'source/solver_official_readonly',records]:paths.update(p for p in root.rglob('*') if p.is_file())
for pat in ['*b016*','clearance*','reopen_clearance*']:
 for root in [R/'scripts',R/'batches']:
  paths.update(p for p in root.glob(pat) if p.is_file())
paths.update(R/f'native_candidates/HI_{v}_clearance_remaining_b016_DRC_PENDING.brd' for v in ['2L','4L'])
paths.update(p for p in (R/'review').glob('b016_*.json') if p.name!='b016_native_artifact_manifest.json')
paths.update([R/'review/final_TOP_GND_b016_readonly_rebase.json',R/'review/NoGroundPlane_official_readonly_research.json'])
paths.update((R/'plans/native_prepared').glob('final_TOP_GND_b016_*_PREPARED.json'))
items=[{'relativePath':p.relative_to(R).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest().upper()} for p in sorted(paths)]
d={'scope':'Onlyb016native+readonlyphase artifacts; evolvingparentnotes/EDA/index andlive nativeREADME excluded. FrozenREADME+constructionnotes copies included. G/b014/b015protected originalSHA facts retainedinguards. ThisisnotoverallHI taskfinalmanifest.','files':items,'count':len(items)};out=R/'review/b016_native_artifact_manifest.json';out.write_text(json.dumps(d,indent=2),encoding='utf8');assert all(hashlib.sha256((R/x['relativePath']).read_bytes()).hexdigest().upper()==x['sha256'] for x in items);print(json.dumps({'manifest':str(out),'files':len(items),'allSHAsVerified':True,'manifestSHA256':hashlib.sha256(out.read_bytes()).hexdigest().upper()}))