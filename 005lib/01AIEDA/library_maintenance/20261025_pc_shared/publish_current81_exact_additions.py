"""Add two frozen exact library clones; never overwrite or remove a public file."""
from pathlib import Path
import hashlib,json,os,shutil
M=Path(__file__).resolve().parent
ROOT=Path(r'D:\001DIY\005lib\01Psm_lib').resolve()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def write(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
def main():
 plan=M/'project81_final_canonical_plan13/ALL81_NEW_EXACT_CANONICAL_ASSETS.json'
 if sha(plan)!='FCFC01977A3E989A16D5B0EC91ABE45D93FA5F2B34F1BE2161C57A1874223421':raise ValueError('Frozen exact additions changed')
 guard=M/'public_canonical_additions_run13/PUBLIC_OLD_PLUS_NEW_GUARD.json'
 before=load(guard)
 for r in before['files']:
  if sha(r['path'])!=r['sha256']:raise ValueError('Public guard changed '+r['path'])
 assets=[v for group in load(plan)['targets'].values() for v in group['assets']]
 for v in assets:
  s,t=Path(v['source']).resolve(),Path(v['target']).resolve()
  if s.parent!=ROOT or t.parent!=ROOT or s.suffix!=t.suffix or t.exists() or sha(s)!=v['source_sha256']:raise ValueError('Additions preflight failed')
 out=M/'project81_exact_additions13'
 out.mkdir(exist_ok=False); added=[]
 for v in assets:
  s,t=Path(v['source']),Path(v['target'])
  with s.open('rb') as src,t.open('xb') as dst:shutil.copyfileobj(src,dst)
  if sha(t)!=v['source_sha256'] or os.path.samefile(s,t) or t.stat().st_nlink!=1:raise ValueError('Independent exact copy failed')
  added.append({'path':str(t),'sha256':sha(t),'bytes':t.stat().st_size,'source':str(s),'nlink':1})
 for r in before['files']:
  if sha(r['path'])!=r['sha256']:raise ValueError('Original public asset modified')
 extended=out/'PUBLIC_GUARD_13425.json';write(extended,{'schema':'EXTENDED_PUBLIC_GUARD_EXACT_ADDITIONS_V1','previous_guard':str(guard),'previous_guard_sha256':sha(guard),'files':before['files']+added})
 template=load(M/'project81_current_target_native_plan/CURRENT81_MISSING_TARGET_NATIVE_PLAN.json')
 seed=template['representatives'][0]; reps=[]
 for r in added:
  p=Path(r['path'])
  if p.suffix.casefold()!='.psm':continue
  row=dict(seed);row.update(stem=p.stem,path=str(p),sha256=r['sha256'],byte_identical_members=[str(p)],family='FUNCTIONAL',size='',classification='FROZEN_EXACT_FUNCTIONAL_CASE_CLONE',canonical_candidate=p.stem);reps.append(row)
 template.update(public_guard_manifest=str(extended),representatives=reps)
 native=out/'EXACT_TWO_TARGETS_NATIVE_PLAN.json';write(native,template)
 report={'status':'NEW_EXACT_FILES_ADDED_ONLY_NATIVE_TARGET_REVIEW_PENDING','plan':str(plan),'plan_sha256':sha(plan),'public_old_files_unchanged':True,'public_files_overwritten':0,'public_files_deleted':0,'added_files':added,'guard':str(extended),'guard_sha256':sha(extended),'native_plan':str(native),'native_plan_sha256':sha(native),'script_sha256':sha(__file__)}
 write(out/'ADDITIONS_ONLY_RESULT.json',report)
 print(json.dumps({k:v for k,v in report.items() if k!='added_files'},ensure_ascii=False))
if __name__=='__main__':main()
