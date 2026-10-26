"""Publish only a frozen exact OLB list with verified backups and full-root guard.

Does not launch CAD, delete libraries, edit existing file contents in place, or accept
a newly scanned public state as a baseline. Each replacement is atomic separately;
the entire multi-file operation is journaled, not claimed to be a single transaction.
"""
from pathlib import Path
import argparse,copy,hashlib,json,os,zipfile
ROOT=Path('D:/001DIY/005lib')
ROOTS=[ROOT/n for n in ('01Psm_lib','01brdlib','01Pad_lib','01captureLib','01script_file','01env')]
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
load=lambda p:json.loads(Path(p).read_text(encoding='utf-8-sig'))
def need(v,m):
 if not v:raise ValueError(m)
def same(p,q):return str(Path(p).resolve()).casefold()==str(Path(q).resolve()).casefold()
def key(p):return str(Path(p).resolve()).casefold()
def no_reparse(p):need(not Path(p).is_symlink() and not (getattr(Path(p).stat(follow_symlinks=False),'st_file_attributes',0)&0x400),'Reparse point disallowed: '+str(p))
def write_json(path,data):
 need(not path.exists(),'Fresh receipt required '+str(path));tmp=path.with_name(path.name+'.tmp');need(not tmp.exists(),'Temporary receipt already exists')
 with tmp.open('x',encoding='utf-8',newline='\n') as f:json.dump(data,f,ensure_ascii=False,indent=2);f.flush();os.fsync(f.fileno())
 os.rename(tmp,path)
def verify_guard(guard):
 records=guard['files'];expected={key(x['path']):x for x in records};need(len(records)==len(expected),'Duplicate expected public paths');actual={}
 for root in ROOTS:
  no_reparse(root)
  for d,dirs,names in os.walk(root,followlinks=False):
   for n in dirs:no_reparse(Path(d)/n)
   for n in names:
    p=Path(d)/n;no_reparse(p);actual[key(p)]=p
 need(set(actual)==set(expected),'Full six-root public file-set differs from frozen guard')
 bad=[str(actual[k]) for k,r in expected.items() if actual[k].stat().st_size!=r['bytes'] or sha(actual[k])!=r['sha256']]
 need(not bad,'Public bytes differ from expected guard '+str(bad[:12]));return len(actual)
def verify_archive(path,archive_sha,members):
 need(sha(path)==archive_sha,'Backup ZIP changed')
 with zipfile.ZipFile(path) as z:
  names=z.namelist();need(len(names)==len(set(names))==len(members),'ZIP member set/multiplicity differs')
  need(set(names)=={x['member'] for x in members},'ZIP unexpected member')
  for m in members:
   data=z.read(m['member']);need(len(data)==m['bytes'] and hashlib.sha256(data).hexdigest().upper()==m['sha256'],'ZIP roundtrip mismatch '+m['member'])
def preflight(plan,planpath):
 need(plan['schema']=='EXACT_PUBLIC_OLB_REPLACEMENT_PLAN_V1','Unexpected OLB publish schema');need(len(plan['replacements'])==13,'Exactly thirteen approved OLBs required')
 need(same(plan['publisher']['path'],__file__) and sha(__file__)==plan['publisher']['sha256'],'Publisher code differs from frozen exact plan')
 for e in plan['evidence']:
  need(sha(e['path'])==e['sha256'],'Immutable proof changed '+e['path'])
 need(sha(plan['source_guard']['path'])==plan['source_guard']['sha256'],'Original full guard file changed')
 guard=load(plan['source_guard']['path']);g={key(x['path']):x for x in guard['files']};seen=set()
 for r in plan['replacements']:
  p,c=Path(r['public']),Path(r['candidate']);need(p.resolve().is_relative_to(ROOTS[3].resolve()) and p.suffix.casefold()=='.olb','Publication escapes approved capture root');need(c.resolve().is_relative_to((ROOT/'01AIEDA').resolve()),'Candidate outside maintenance tree');no_reparse(p);no_reparse(c)
  need(key(p) not in seen,'Duplicate public replacement');seen.add(key(p));need(g[key(p)]['sha256']==r['old_sha256'] and g[key(p)]['bytes']==r['old_bytes'],'Guard old OLB differs from exact plan')
  need(sha(p)==r['old_sha256'] and p.stat().st_size==r['old_bytes'],'Original public OLB changed');need(sha(c)==r['new_sha256'] and c.stat().st_size==r['new_bytes'],'Candidate OLB changed')
  proof=load(r['review']);need(proof['status']=='PASS_COMPLETE_ORDERED_OLB_FP_FIELDS_AND_NATIVE_ALL_FONT_FIELDS_STAGING_ONLY','Missing strict staging proof')
  need(proof['candidate_sha256']==r['new_sha256'] and proof['public_original_unchanged_sha256']==r['old_sha256'],'Proof OLB SHA mismatch')
  need(proof['case_sha256']==sha(r['case']) and same(proof['case'],r['case']),'Proof case mismatch')
  need(len(proof['negative_controls'])>=10 and all(x['status']=='PASS_REJECTED' for x in proof['negative_controls']),'Strict negative controls incomplete')
  need(proof['native_fonts']['native_fields_equal']==337,'Complete native defaults/font proof missing')
 verify_archive(plan['backup']['path'],plan['backup']['sha256'],plan['backup']['members'])
 need(sum(r['field_count'] for r in plan['replacements'])==46,'Expected exactly forty-six frozen fields')
 return guard
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--plan',required=True,type=Path);ap.add_argument('--mode',required=True,choices=['dry-run','apply']);ap.add_argument('--work',required=True,type=Path);a=ap.parse_args();need(not a.work.exists(),'Fresh work directory required');need(a.work.resolve().is_relative_to((ROOT/'01AIEDA').resolve()),'Receipt directory must stay under 01AIEDA');a.work.mkdir(parents=True)
 plan=load(a.plan);base={'plan':str(a.plan),'plan_sha256':sha(a.plan),'script_sha256':sha(__file__),'mode':a.mode,'public_files_replaced':0,'CAD_started':False}
 guard=preflight(plan,a.plan);base['source_guard']=plan['source_guard'];base['protected_files']=verify_guard(guard)
 if a.mode=='dry-run':
  write_json(a.work/'PUBLIC_OLB_PUBLISH_DRY_RUN.json',dict(base,status='PASS_EXACT_THIRTEEN_OLB_PROOFS_ZIP_AND_FULL_GUARD_READONLY'));print(json.dumps(base));return
 expected=copy.deepcopy(guard);records={key(x['path']):x for x in expected['files']};done=[];journal=a.work/'ATOMIC_OLB_REPLACEMENTS.jsonl'
 try:
  with journal.open('x',encoding='utf-8',newline='\n') as f:
   f.write(json.dumps(dict(base,status='START_EXACT_ATOMIC_DIRECTORY_ENTRY_REPLACEMENTS'))+'\n');f.flush();os.fsync(f.fileno())
   for i,r in enumerate(plan['replacements']):
    p,c=Path(r['public']),Path(r['candidate']);tmp=p.with_name(p.name+'.pcpublish_'+base['plan_sha256'][:12]+'.tmp');need(not tmp.exists(),'Public staging entry already exists')
    need(sha(p)==r['old_sha256'] and sha(c)==r['new_sha256'],'Source changed just before atomic replacement')
    with c.open('rb') as src,tmp.open('xb') as dst:
     while data:=src.read(1024*1024):dst.write(data)
     dst.flush();os.fsync(dst.fileno())
    need(tmp.stat().st_size==r['new_bytes'] and sha(tmp)==r['new_sha256'],'Independent temporary copy failed SHA');need(sha(p)==r['old_sha256'],'Public OLB changed during copy')
    os.replace(tmp,p);need(sha(p)==r['new_sha256'],'Published OLB failed SHA readback');done.append(r['public']);records[key(p)]['sha256']=r['new_sha256'];records[key(p)]['bytes']=r['new_bytes']
    f.write(json.dumps({'index':i,'path':str(p),'old_sha256':r['old_sha256'],'new_sha256':r['new_sha256'],'atomic_replace_complete':True})+'\n');f.flush();os.fsync(f.fileno())
 except Exception as ex:
  write_json(a.work/'PUBLIC_OLB_PUBLISH_PARTIAL.json',dict(base,status='PARTIAL_REPLACEMENTS_PRESERVE_BACKUP_AND_JOURNAL',completed=done,error=repr(ex)));raise
 verify_guard(expected)
 expected.update(status='EXPECTED_CURRENT_BYTES_BY_EXACT_THIRTEEN_OLB_REPLACEMENT_OF_FROZEN_GUARD',source_guard=plan['source_guard'],replacement_plan={'path':str(a.plan),'sha256':sha(a.plan)},explicit_replacements=[{k:r[k] for k in ('public','old_sha256','new_sha256','old_bytes','new_bytes')} for r in plan['replacements']])
 write_json(a.work/'PUBLIC_GUARD_AFTER_EXACT13_OLB.json',expected)
 receipt=dict(base,status='PASS_EXACT_THIRTEEN_OLB_ATOMIC_REPLACEMENTS_OTHER_PUBLIC_FILES_UNCHANGED_PENDING_ACTUAL_PUBLIC_NATIVE_REOPEN',public_files_replaced=len(done),new_guard={'path':str(a.work/'PUBLIC_GUARD_AFTER_EXACT13_OLB.json'),'sha256':sha(a.work/'PUBLIC_GUARD_AFTER_EXACT13_OLB.json')},actual_native_reopen_required=True)
 write_json(a.work/'PUBLIC_OLB_PUBLISH_RECEIPT.json',receipt);print(json.dumps(receipt))
if __name__=='__main__':main()
