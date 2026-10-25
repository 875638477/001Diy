from pathlib import Path
import json,hashlib,datetime
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonG_30_37_20261020')
p=R/'NATIVE_WORKFLOW.md'
if p.exists():
 text=p.read_text();text=text.replace('(current/','(../current/').replace('(review/','(../review/')
 (R/'native/README.md').write_text(text,encoding='utf8');p.unlink()
else: assert (R/'native/README.md').is_file()
# Seal only this subagent's files; parent/root engineering/plans/review artifacts have separate owners.
files=[]
for dirname in ['scripts','source','backups','native','logs','inventory','library','current','exports']:
 files += [p for p in (R/dirname).rglob('*') if p.is_file()]
for name in ['native_final_report','native_validation']:
 for suffix in ['', '_attempt01','_attempt02']:
  p=R/f'review/{name}{suffix}.json'
  if p.is_file():files.append(p)
files=sorted(set(files),key=lambda x:x.as_posix().lower())
rows=[]
for p in files:
 assert p.resolve().is_relative_to(R.resolve())
 rows.append({'path':p.relative_to(R).as_posix(),'size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest().upper()})
manifest={'status':'SEALED_NATIVE_ARTIFACTS','scope':'Owned native/script/log/library/input/inventory/export files and six named native-review JSON files only. Excludes root README/plan/engineering/reviews/images/notes and this manifest itself. The root task seals the full folder separately.','count':len(rows),'totalBytes':sum(x['size'] for x in rows),'files':rows}
out=R/'native_artifact_manifest.json';out.write_text(json.dumps(manifest,indent=2),encoding='utf8')
# Independent second read for every sealed file.
for row in rows:
 p=R/row['path'];assert p.stat().st_size==row['size'] and hashlib.sha256(p.read_bytes()).hexdigest().upper()==row['sha256']
print(json.dumps({'status':manifest['status'],'count':len(rows),'manifest':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest().upper(),'bytes':manifest['totalBytes']},indent=2))
