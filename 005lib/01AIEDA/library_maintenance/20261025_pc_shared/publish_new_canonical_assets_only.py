"""Root-executed additions only. Never overwrites or removes existing public files."""
from pathlib import Path
import argparse,hashlib,json,os,shutil
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def jr(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def dump(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def child(p,root):return p.resolve().parent==root.resolve()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--plan',type=Path,required=True);ap.add_argument('--expected-plan-sha',required=True);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--execute',action='store_true');a=ap.parse_args()
 assert os.name=='nt','This runner uses Windows non-overwriting rename semantics'
 assert sha(a.plan)==a.expected_plan_sha.upper(),'Frozen plan mismatch'
 plan=jr(a.plan);assert plan['schema']=='PUBLIC_CANONICAL_ADDITIONS_ONLY_PLAN_V1';root=Path(plan['public_root']);guards=jr(plan['old_public_guard'])['files'];assert sha(plan['old_public_guard'])==plan['old_public_guard_sha256']
 pairs=[x for t in plan['new_targets'] for x in t['pair']];assert len(pairs)==plan['new_file_count'];assert len({x['target'].lower() for x in pairs})==len(pairs)
 for x in pairs:
  src,dst=Path(x['source']),Path(x['target']);assert child(src,root) and child(dst,root);assert dst.suffix.lower() in ('.psm','.dra') and dst.stem.lower().endswith('_pc');assert not dst.exists();assert sha(src)==x['source_sha256']==x['target_expected_sha256']
 for t in plan['existing_targets_preserved']:
  assert sha(t['psm'])==t['psm_sha256'] and sha(t['dra'])==t['dra_sha256']
 for x in guards:assert Path(x['path']).is_file() and sha(x['path'])==x['sha256'],'Protected oldfile changed '+x['path']
 print(json.dumps({'status':'PREFLIGHT_PASS','new_files':len(pairs),'existing_preserved':len(plan['existing_targets_preserved']),'old_guarded_files':len(guards),'execute':a.execute}),flush=True)
 if not a.execute:return
 assert not a.output.exists(),'Fresh staging/record directory required';a.output.mkdir(parents=True);stage=a.output/'staged';stage.mkdir();added=[]
 # Stage all copies before creating any public directory entry. New files must be independent nlink1.
 for i,x in enumerate(pairs):
  src=Path(x['source']);p=stage/(f'{i:03}_'+Path(x['target']).name)
  with src.open('rb') as inf,p.open('xb') as outf:shutil.copyfileobj(inf,outf);outf.flush();os.fsync(outf.fileno())
  assert p.stat().st_nlink==1 and sha(p)==x['source_sha256'];x['staged']=str(p)
 dump(a.output/'STAGED_COPIES.json',pairs)
 for x in pairs:
  src,p,dst=Path(x['source']),Path(x['staged']),Path(x['target']);assert not dst.exists() and sha(src)==x['source_sha256'] and sha(p)==x['source_sha256']
  os.rename(p,dst) # Windows raises if destination exists; sameD volume atomic entry, no hardlink.
  assert sha(dst)==x['target_expected_sha256'] and dst.stat().st_nlink==1
  added.append({'source':str(src),'source_sha256':x['source_sha256'],'target':str(dst),'target_sha256':sha(dst),'bytes':dst.stat().st_size,'nlink':dst.stat().st_nlink,'inode':dst.stat().st_ino})
  dump(a.output/'ADDED_FILES_PROGRESS.json',added)
 for x in guards:assert Path(x['path']).is_file() and sha(x['path'])==x['sha256'],'Oldfile changed during newasset creation '+x['path']
 extended=guards+[{'path':r['target'],'sha256':r['target_sha256'],'bytes':r['bytes'],'root':str(root),'relative':Path(r['target']).name} for r in added]
 gp=a.output/'PUBLIC_OLD_PLUS_NEW_GUARD.json';dump(gp,{'status':'EXPECTED_CURRENT_BYTES_AFTER_ADDITIONS_ONLY_OLD_UNCHANGED','files':extended})
 srcplan=jr(plan['source_native_plan']);index={r['stem'].lower():r for r in srcplan['representatives']};auditrows=[]
 canonical_names=[t['target'] for t in plan['targets']]+['sot23-3','sop-8-150mil']
 for i,name in enumerate(sorted(set(canonical_names))):
  p=root/(name+'.psm');h=sha(p);origin=index.get(name.lower())
  if origin is None:
   t=next(t for t in plan['new_targets'] if t['target']==name);origin=index[t['generic_source'].lower()]
  auditrows.append({**origin,'path':str(p),'relative':p.name,'root':str(root),'bytes':p.stat().st_size,'sha256':h,'stem':name,'canonical_candidate':name,'classification':'FINAL_CANONICAL_TARGET_REQUIRE_INDEPENDENT_COLD_NATIVE','byte_identical_members':[str(p)],'representative_index':i})
 audit={**srcplan,'schema':'GLOBAL_SUFFIX_PUBLIC_NATIVE_AUDIT_PLAN_V1','status':'NEW_AND_EXISTING_CANONICAL_TARGETS_NOT_YET_NATIVE_VERIFIED','public_guard_manifest':str(gp),'selected_psm_count':len(auditrows),'exact_byte_group_count':len(auditrows),'native_representative_count':len(auditrows),'representatives':auditrows,'source_addition_plan':str(a.plan),'source_addition_plan_sha256':sha(a.plan)}
 apath=a.output/'CANONICAL_TARGET_NATIVE_AUDIT_PLAN.json';dump(apath,audit)
 result={'status':'NEW_FILES_ADDED_ONLY_COLD_TARGET_NATIVE_AND_REFERENCE_CLOSURE_PENDING','plan':str(a.plan),'plan_sha256':sha(a.plan),'new_files':len(added),'new_targets':plan['new_target_count'],'old_files_unchanged':True,'old_guarded_files':len(guards),'extended_guard_file':str(gp),'extended_guard_file_sha256':sha(gp),'target_native_plan':str(apath),'target_native_plan_sha256':sha(apath),'native_target_count':len(auditrows),'added':added,'not_done':['No oldasset deletion','No existing publicfile replacement','No OLB/DSN/BRD mutation','No overall task release']}
 dump(a.output/'ADDITIONS_ONLY_RESULT.json',result);print(json.dumps({k:v for k,v in result.items() if k!='added'}),flush=True)
if __name__=='__main__':main()
