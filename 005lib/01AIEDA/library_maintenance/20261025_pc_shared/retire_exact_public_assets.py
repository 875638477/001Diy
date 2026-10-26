"""Exact, reversible-by-ZIP retirement; no recursive delete, no CAD, no PAD changes.

Root invokes after native reference closure. Stage is read-only for public files.
Existing archives are never overwritten or removed. Apply removes only named public
directory entries after SHA and archive roundtrip validation; hardlinked siblings keep
their original bytes. Journal is flushed for each entry.
"""
from pathlib import Path
import argparse,hashlib,json,os,sys,zipfile
ALLOWED_ROOTS=[Path(r'D:\001DIY\005lib')/name for name in ('01Psm_lib','01brdlib','01Pad_lib','01captureLib','01script_file','01env')]
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
jr=lambda p:json.loads(Path(p).read_text('utf-8-sig'))
def require(ok,message):
 if not ok:raise ValueError(message)
def atomic_json(path,data):
 require(not path.exists(),'Fresh receipt path required: '+str(path));temp=path.with_name(path.name+'.tmp');require(not temp.exists(),'Temporary path already exists')
 with temp.open('x',encoding='utf-8',newline='\n') as f:json.dump(data,f,ensure_ascii=False,indent=2);f.flush();os.fsync(f.fileno())
 os.rename(temp,path)
def actual_files():
 files={}
 for root in ALLOWED_ROOTS:
  require(root.is_dir(),'Public root missing '+str(root))
  for d,dirs,names in os.walk(root,followlinks=False):
   # Reject any reparse-point tree before trusting a complete guard.
   for name in dirs:require(not (Path(d)/name).is_symlink(),'Symlink tree requires independent plan '+str(Path(d)/name))
   for n in names:
    p=Path(d)/n;require(not p.is_symlink(),'Symlink file requires independent plan '+str(p));files[str(p.resolve()).casefold()]=p
 return files
def check_guard(path):
 d=jr(path);records=d['files'];expected={str(Path(x['path']).resolve()).casefold():x for x in records};actual=actual_files()
 require(len(expected)==len(records),'Duplicate guard file paths');require(set(expected)==set(actual),'Full six-root guard file set mismatch')
 bad=[]
 for k,r in expected.items():
  if sha(actual[k])!=r['sha256']:bad.append(str(actual[k]))
 require(not bad,'Public guard byte mismatch '+str(bad[:10]));return {'path':str(path),'sha256':sha(path),'files':len(expected)}
def plan_assets(plan):
 require(plan['schema']=='EXACT_PUBLIC_FOOTPRINT_RETIREMENT_PLAN_V1','Unknown retirement schema');root=Path(plan['public_root']).resolve(strict=True);require(root==ALLOWED_ROOTS[0].resolve(),'Only exact public PSM root accepted')
 assets=plan['assets'];seen=set()
 for a in assets:
  p=Path(a['path']);require(p.is_file() and not p.is_symlink(),'Missing/symlink asset '+str(p));require(p.resolve().parent==root,'Resolved asset escapes exact root '+str(p));require(p.suffix.lower() in {'.psm','.dra','.txt'},'Forbidden extension');require(p.stem.casefold()==a['source_stem'].casefold(),'Stem mismatch');require(sha(p)==a['sha256'] and p.stat().st_size==a['bytes'],'Frozen asset changed '+str(p));require(str(p.resolve()).casefold() not in seen,'Duplicate asset');seen.add(str(p.resolve()).casefold())
  require(a.get('target_stem') is None or a['target_stem'].casefold()!=a['source_stem'].casefold(),'Plan attempts to remove same target')
  if p.suffix.lower()=='.txt':require(a.get('self_reference_verification',{}).get('file_sha256')==a['sha256'],'TXT must be proven same-stem self declaration')
 require(len(assets)==plan['asset_count'],'Asset count changed');return assets
def zip_roundtrip(path,assets):
 with zipfile.ZipFile(path,'r') as z:
  names=z.namelist();require(len(names)==len(set(names))==len(assets),'ZIP extra/duplicate/missing members')
  for a in assets:
   name=Path(a['path']).name;data=z.read(name);require(len(data)==a['bytes'] and hashlib.sha256(data).hexdigest().upper()==a['sha256'],'ZIP roundtrip mismatch '+name)
 return {'path':str(path),'sha256':sha(path),'members':len(assets),'all_members_complete_SHA_roundtrip':True}
def backup_bundle_verify(bundle,assets):
 covered={}
 for archive in bundle['archives']:
  path=Path(archive['path']);require(sha(path)==archive['sha256'],'Existing archive changed '+str(path))
  with zipfile.ZipFile(path,'r') as z:
   rows=archive['members'];names=z.namelist();require(len(names)==len(set(names))==len(rows),'Archive member manifest mismatch')
   for row in rows:
    data=z.read(row['member']);require(len(data)==row['bytes'] and hashlib.sha256(data).hexdigest().upper()==row['sha256'],'Existing archive member roundtrip mismatch '+row['member'])
    covered[str(Path(row['path']).resolve()).casefold()]=(row['sha256'],row['bytes'])
 for a in assets:require(covered.get(str(Path(a['path']).resolve()).casefold())==(a['sha256'],a['bytes']),'Retirement asset is not fully backed up '+a['path'])
 return {'archive_count':len(bundle['archives']),'verified_archive_members':sum(len(r['members']) for r in bundle['archives']),'retirement_assets_all_covered':len(assets)}
def closure(path,planpath,plan):
 d=jr(path);require(d['status']=='PASS_NATIVE_REFERENCE_CLOSURE','Native reference closure not PASS');require(d['retirement_plan_sha256']==sha(planpath),'Closure not exact retirement plan');require(set(d['covered_source_stems'])==set(plan['accepted_source_stems']),'Closure does not cover all retired source stems')
 for stem in plan['accepted_source_stems']:
  counts=d['active_reference_counts'][stem];require(set(counts)==set(plan['required_apply_closure_categories']),'Closure categories incomplete '+stem);require(all(type(n)==int and n==0 for n in counts.values()),'Live references remain '+stem)
 require(d.get('native_evidence'),'Actual native source evidence required')
 for e in d['native_evidence']:require(Path(e['path']).is_file() and sha(e['path'])==e['sha256'],'Native evidence changed '+e['path'])
 for e in d.get('canonical_target_proofs',[]):require(Path(e['path']).is_file() and sha(e['path'])==e['sha256'],'Target proof changed')
 require(d.get('canonical_target_proofs'),'Cold native canonical target proof required');return {'path':str(path),'sha256':sha(path),'all_retired_stems_zero_in_all_8_reference_categories':True}
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--plan',type=Path,required=True);ap.add_argument('--mode',choices=['dry-run','stage','apply'],required=True);ap.add_argument('--guard',type=Path,required=True);ap.add_argument('--work',type=Path,required=True);ap.add_argument('--closure',type=Path);ap.add_argument('--reuse-backup-receipt',type=Path);a=ap.parse_args();plan=jr(a.plan);assets=plan_assets(plan)
 require(a.work.resolve().is_relative_to(Path(r'D:\001DIY\005lib\01AIEDA').resolve()),'Retirement work must stay under learning/maintenance root');a.work.mkdir(exist_ok=True,parents=True)
 guard=check_guard(a.guard);base={'plan':str(a.plan),'plan_sha256':sha(a.plan),'guard':guard,'mode':a.mode,'assets':len(assets),'bytes':sum(x['bytes'] for x in assets),'public_files_written':0,'public_files_removed':0}
 if a.mode=='dry-run':
  atomic_json(a.work/'DRY_RUN.json',dict(base,status='PASS_EXACT_PATH_SHA_AND_FULL_PUBLIC_GUARD_DRY_RUN'));print(json.dumps(base));return
 if a.mode=='stage':
  bundle={'archives':[]};covered={}
  if a.reuse_backup_receipt:
   old=jr(a.reuse_backup_receipt);require(old['status']=='PASS_VERIFIED_BACKUP_ONLY_NO_PUBLIC_MUTATION' and old['all_members_roundtrip_SHA_exact'],'Unsupported external backup receipt')
   oldarchive={'path':old['archive'],'sha256':old['archive_sha256'],'members':old['members'],'origin_receipt':str(a.reuse_backup_receipt),'origin_receipt_sha256':sha(a.reuse_backup_receipt)};bundle['archives'].append(oldarchive)
   backup_bundle_verify(bundle,[])
   covered={str(Path(x['path']).resolve()).casefold():(x['sha256'],x['bytes']) for x in old['members']}
  missing=[x for x in assets if covered.get(str(Path(x['path']).resolve()).casefold())!=(x['sha256'],x['bytes'])]
  if missing:
   archive=a.work/'PUBLIC_LEGACY_INCREMENTAL_ASSETS.zip';require(not archive.exists(),'Never overwrite any existing ZIP');tmp=archive.with_name(archive.name+'.partial');require(not tmp.exists(),'Partial archive exists; preserve and use fresh work directory')
   with zipfile.ZipFile(tmp,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
    for item in missing:z.write(item['path'],arcname=Path(item['path']).name)
   zip_roundtrip(tmp,missing);os.rename(tmp,archive);bundle['archives'].append({'path':str(archive),'sha256':sha(archive),'members':[{'path':x['path'],'member':Path(x['path']).name,'sha256':x['sha256'],'bytes':x['bytes']} for x in missing]})
  backup=backup_bundle_verify(bundle,assets);post=check_guard(a.guard)
  atomic_json(a.work/'BACKUP_STAGE.json',dict(base,status='PASS_ALL_MEMBERS_ZIP_SHA_ROUNDTRIP_PUBLIC_UNCHANGED',backup=backup,backup_bundle=bundle,post_guard=post));print(json.dumps(backup));return
 require(a.closure is not None,'--closure required for apply');cl=closure(a.closure,a.plan,plan);stage=jr(a.work/'BACKUP_STAGE.json');require(stage['status']=='PASS_ALL_MEMBERS_ZIP_SHA_ROUNDTRIP_PUBLIC_UNCHANGED' and stage['plan_sha256']==sha(a.plan),'Stage receipt does not bind plan');backup=backup_bundle_verify(stage['backup_bundle'],assets)
 journal=a.work/'APPLY_EXACT_FILES.jsonl';require(not journal.exists(),'Fresh apply journal required; previous partial run must be audited explicitly')
 completed=[]
 try:
  with journal.open('x',encoding='utf-8',newline='\n') as f:
   f.write(json.dumps(dict(base,status='APPLY_STARTED_AFTER_EXACT_NATIVE_CLOSURE',closure=cl,backup=backup))+'\n');f.flush();os.fsync(f.fileno())
   for item in assets:
    p=Path(item['path']);require(p.resolve().parent==ALLOWED_ROOTS[0].resolve() and sha(p)==item['sha256'],'Source changed during retirement '+str(p))
    # Unlink exactly this verified directory entry. Do not modify file contents or hardlinked siblings.
    p.unlink();completed.append(item);f.write(json.dumps({'path':str(p),'sha256':item['sha256'],'bytes':item['bytes'],'removed_exact_entry':True})+'\n');f.flush();os.fsync(f.fileno())
 except Exception:
  atomic_json(a.work/'APPLY_PARTIAL_PRESERVED_BACKUP.json',dict(base,status='PARTIAL_STOPPED_RESTORE_OR_AUDIT_EXACT_JOURNAL',completed_files=len(completed),backup=backup));raise
 remaining=actual_files();old=jr(a.guard)['files'];expected={str(Path(x['path']).resolve()).casefold():x for x in old if str(Path(x['path']).resolve()).casefold() not in {str(Path(v['path']).resolve()).casefold() for v in assets}}
 require(set(remaining)==set(expected),'Unexpected new/removed public file after retirement')
 require(all(sha(remaining[k])==r['sha256'] for k,r in expected.items()),'Unretired public bytes changed')
 receipt=dict(base,status='PASS_EXACT_RETIRED_ENTRIES_BACKED_UP_OTHER_PUBLIC_BYTES_UNCHANGED',public_files_removed=len(completed),closure=cl,backup=backup,remaining_public_files=len(remaining));atomic_json(a.work/'APPLY_RECEIPT.json',receipt);print(json.dumps(receipt))
if __name__=='__main__':main()
