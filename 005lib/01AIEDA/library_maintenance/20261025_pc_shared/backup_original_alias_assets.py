"""Back up the frozen 941-cohort sidecars; never delete or change public assets."""
from pathlib import Path
import hashlib,json,zipfile

M=Path(__file__).resolve().parent
ROOT=Path(r'D:\001DIY\005lib\01Psm_lib').resolve()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def main():
 plan=M/'global_canonical_publish_v1/ALIAS_CONSOLIDATION_PLAN_941.json'
 guard=M/'global_suffix_inventory_v1/PUBLIC_ALL_SIX_ROOTS_SHA256.json'
 out=M/'original941_asset_backup13'
 if out.exists():raise ValueError('Fresh backup output required')
 names={r['source'].casefold() for r in load(plan)['rows']}
 rows=[]
 for r in load(guard)['files']:
  p=Path(r['path']).resolve()
  if p.parent==ROOT and p.suffix.casefold() in {'.psm','.dra','.txt'} and p.stem.casefold() in names:
   if sha(p)!=r['sha256']:raise ValueError('Source guard changed '+str(p))
   rows.append({'path':str(p),'member':p.name,'sha256':r['sha256'],'bytes':p.stat().st_size})
 if len({r['member'].casefold() for r in rows})!=len(rows):raise ValueError('Duplicate archive identity')
 if len([r for r in rows if Path(r['path']).suffix.casefold()=='.psm'])!=941:raise ValueError('Incomplete source cohort')
 out.mkdir(); archive=out/'ORIGINAL_941_PSM_DRA_DEVICE_ASSETS.zip'
 with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED) as z:
  for r in rows:z.write(r['path'],r['member'])
  z.writestr('SHA256_MANIFEST.json',json.dumps(rows,ensure_ascii=False,indent=2))
 with zipfile.ZipFile(archive) as z:
  if z.testzip() is not None:raise ValueError('ZIP CRC error')
  for r in rows:
   if hashlib.sha256(z.read(r['member'])).hexdigest().upper()!=r['sha256']:raise ValueError('ZIP roundtrip hash mismatch')
 for r in rows:
  if sha(r['path'])!=r['sha256']:raise ValueError('Source changed during backup')
 result={'status':'PASS_VERIFIED_BACKUP_ONLY_NO_PUBLIC_MUTATION','plan':str(plan),'plan_sha256':sha(plan),'guard':str(guard),'guard_sha256':sha(guard),'archive':str(archive),'archive_sha256':sha(archive),'archive_bytes':archive.stat().st_size,'files':len(rows),'original_bytes':sum(r['bytes'] for r in rows),'all_members_roundtrip_SHA_exact':True,'public_originals_unchanged':True,'public_files_deleted':0,'script_sha256':sha(__file__),'members':rows}
 (out/'BACKUP_ONLY_RESULT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps({k:v for k,v in result.items() if k!='members'},ensure_ascii=False))
if __name__=='__main__':main()
