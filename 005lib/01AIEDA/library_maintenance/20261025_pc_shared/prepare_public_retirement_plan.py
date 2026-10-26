"""Prepare exact legacy footprint assets only; do not delete or mutate public files."""
from pathlib import Path
from collections import Counter
import argparse,hashlib,json,re,shlex
M=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
jr=lambda p:json.loads(Path(p).read_text('utf-8-sig'))
ROOT=Path(r'D:\001DIY\005lib\01Psm_lib').resolve()
def validate_device(path,stem):
 text=path.read_text('utf-8-sig');declared=[]
 for line in text.splitlines():
  fields=shlex.split(line,posix=True)
  if not fields:continue
  if fields[0].upper() in {'PACKAGE','PINORDER','PINUSE'} and len(fields)>=2:declared.append(fields[1])
  elif fields[0].upper()=='FUNCTION' and len(fields)>=3:declared.append(fields[2])
 if not declared or any(x.casefold()!=stem.casefold() for x in declared):raise ValueError('Device TXT is not a same-stem self declaration: '+str(path))
 return {'self_referenced_stem':stem,'declarations_verified':declared,'file_sha256':sha(path)}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--additional-aliases',type=Path);ap.add_argument('--out',type=Path,default=M/'public_retirement_plan13');a=ap.parse_args();a.out.mkdir(exist_ok=True)
 original=M/'global_canonical_publish_v1/ALIAS_CONSOLIDATION_PLAN_941.json';p=jr(original);assets=[];accepted=[];preserved=[]
 for row in p['rows']:
  if row['action'].startswith('KEEP_') or row['action'].startswith('PRESERVE_'):preserved.append(row);continue
  accepted.append(row)
 extra=[]
 if a.additional_aliases:
  addition=jr(a.additional_aliases)
  if addition['status']!='FROZEN_NATIVE_CONFIRMED_NONPASSIVE_ALIAS_MAPPINGS':raise ValueError('Additional aliases must have frozen actual native proof')
  extra=addition['rows'];by_source={r['source']:r for r in accepted}
  for r in extra:
   if r['source'] in by_source:
    before=by_source[r['source']];oldassets={a['path'].lower():a['sha256'] for a in before['source_asset_set']};newassets={a['path'].lower():a['sha256'] for a in r['source_asset_set']}
    if oldassets!=newassets:raise ValueError('Overlappingsourceassetset differs '+r['source'])
   by_source[r['source']]=r
  accepted=list(by_source.values())
 pathset=set()
 for row in accepted:
  for item in row['source_asset_set']:
   path=Path(item['path']);resolved=path.resolve(strict=True)
   if path.is_symlink() or resolved.parent!=ROOT or path.suffix.lower() not in {'.psm','.dra','.txt'}:raise ValueError('Asset leaves exact public PSM root or extension: '+str(path))
   if path.stem.casefold()!=row['source'].casefold():raise ValueError('Asset is not exact same stem')
   if sha(path)!=item['sha256'] or path.stat().st_size!=item['bytes']:raise ValueError('Source changed: '+str(path))
   if str(resolved).casefold() in pathset:raise ValueError('Duplicate retirement path')
   pathset.add(str(resolved).casefold());x=dict(item,source_stem=row['source'],target_stem=row.get('target'),reason=row['action'],root=str(ROOT))
   if path.suffix.lower()=='.txt':x['self_reference_verification']=validate_device(path,row['source'])
   assets.append(x)
 plan={'schema':'EXACT_PUBLIC_FOOTPRINT_RETIREMENT_PLAN_V1','status':'PREPARED_NOT_APPLIED_REQUIRES_FINAL_NATIVE_REFERENCE_CLOSURE_AND_BACKUP','public_root':str(ROOT),'source_alias_plan':str(original),'source_alias_plan_sha256':sha(original),'additional_alias_plan':str(a.additional_aliases) if a.additional_aliases else None,'additional_alias_plan_sha256':sha(a.additional_aliases) if a.additional_aliases else None,'accepted_alias_count':len(accepted),'accepted_source_stems':[x['source'] for x in accepted],'ordinary_or_explicit_standardization_rows':accepted,'asset_count':len(assets),'asset_bytes':sum(x['bytes'] for x in assets),'assets':assets,'preserved_functional_or_existing_canonical_rows':preserved,'allowed_extensions':['.psm','.dra','.txt'],'explicit_no_touch':['All PAD, SHAPE, FLASH and shared dependencies','All existing release/raw/ZIP archives','All design, OLB and DSN files; reference changes are independently published before retirement','Every current canonical target'],'required_apply_closure_categories':['project_capture','project_brd_declared','project_brd_placed','public_olb','public_dsn','public_brd_declared','public_brd_placed','active_device_map'],'runner_behavior':'dry-run verifies only; stage ZIP every member with SHA roundtrip and exact source guard; apply requires exact-plan closure for every source stem and approved fresh complete six-root guard. Exact single files only; no recursive deletion.'}
 out=a.out/'PUBLIC_RETIREMENT_EXACT_PLAN.json';out.write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps({'plan':str(out),'sha256':sha(out),'accepted_aliases':len(accepted),'assets':len(assets),'bytes':plan['asset_bytes'],'extensions':dict(Counter(Path(x['path']).suffix.lower() for x in assets))},indent=2))
if __name__=='__main__':main()
