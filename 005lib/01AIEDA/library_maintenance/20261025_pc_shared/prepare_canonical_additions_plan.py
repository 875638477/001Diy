"""Create additions-only canonical copy plan from frozen native reviews; no public mutation."""
from pathlib import Path
from collections import defaultdict
import json,hashlib
M=Path(r'D:\001DIY\005lib\01AIEDA\library_maintenance\20261025_pc_shared');OUT=M/'global_canonical_publish_v1';OUT.mkdir(exist_ok=True)
P=M/'global_suffix_inventory_v1/PSM_NATIVE_AUDIT_PLAN.json';plan=json.loads(P.read_text(encoding='utf-8'));frozen={r['stem'].lower():r for r in plan['representatives']};guard=json.loads(Path(plan['public_guard_manifest']).read_text(encoding='utf-8'))['files'];gf={x['path'].lower():x for x in guard}
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
reviews={e['stem'].lower():e for p in (M/'global_suffix_native_review_v3').glob('e*_SCHEMA_GEOMETRY.json') for e in json.loads(p.read_text(encoding='utf-8'))}
assert len(reviews)==939
raw=json.loads((M/'global_suffix_native_v3/report.json').read_text(encoding='utf-8'));assert raw['public_files_unchanged'] and raw['outputs']==939 and len(raw['failed'])==2
bytarget=defaultdict(list)
for e in reviews.values():
 if e['scope'].startswith('ORDINARY_TWO_TERMINAL'):bytarget[e['canonical_candidate'] or (e['family']+e['size']+'_pc')].append(e)
# Two failed legacy0603 variants retire to an existing canonical after sourceDRA intent proof; they never become definition source.
legacy_failed=[]
for stem,folder in [('c0603-round','failed_c0603_round_intent_v1'),('c0603_fcs','failed_c0603_fcs_intent_v1')]:
 pr=M/folder;report=json.loads((pr/'PROBE_REPORT.json').read_text(encoding='utf-8'));assert report['sources_unchanged']
 table=(pr/'dra_pins/extract.txt').read_text(encoding='utf-8-sig').splitlines();header=next(x for x in table if x.startswith('A!')).split('!')[1:-1];pins=[]
 for l in table:
  if l.startswith('S!'):
   v=l.split('!')[1:-1];pins.append(dict(zip(header,v)))
 assert len(pins)==2 and {p['PIN_NUMBER'] for p in pins}=={'1','2'}
 geo=(pr/'dra_geometry/extract.txt').read_text(encoding='utf-8-sig').splitlines();gh=next(x for x in geo if x.startswith('A!')).split('!')[1:-1]
 body=[]
 for l in geo:
  if l.startswith('S!'):
   r=dict(zip(gh,l.split('!')[1:-1]))
   if r.get('CLASS')=='PACKAGE GEOMETRY' and r.get('SUBCLASS') in ('PLACE_BOUND_TOP','SILKSCREEN_TOP','ASSEMBLY_TOP'):body.append(r)
 assert body
 legacy_failed.append({'stem':stem,'source_sha256':frozen[stem]['sha256'],'canonical':'c0603_pc','classification':'FAILED_LEGACY_TWO_TERMINAL_DRA_INTENT_CONFIRMED_RETIRE_TO_VERIFIED_STANDARD','native_failure':next(x for x in raw['failed'] if x['stem']==stem),'source_dra_pin_rows':pins,'source_dra_package_geometry_rows':body,'probe_report':str(pr/'PROBE_REPORT.json'),'probe_report_sha256':sha(pr/'PROBE_REPORT.json'),'dra_pin_extract':str(pr/'dra_pins/extract.txt'),'dra_pin_extract_sha256':sha(pr/'dra_pins/extract.txt'),'dra_geometry_extract':str(pr/'dra_geometry/extract.txt'),'dra_geometry_extract_sha256':sha(pr/'dra_geometry/extract.txt'),'geometry_equivalence_claim':False,'limits':'CompiledPSM failed to fully load; sourceDRA documents ordinarytwo-terminal0603 intent. Full old PSM geometry is not invented. Canonical target must independently coldload. No repair to broken legacy sharedPAD/SHAPE dependencies.'})
new=[];existing=[];targets=[];errors=[];base=Path(plan['psmpath'])
for target,members in sorted(bytarget.items()):
 dest=base/(target+'.psm');destdra=base/(target+'.dra')
 if dest.exists():
  assert destdra.exists();e=reviews.get(target.lower());assert e and e['scope'].startswith('ORDINARY_TWO_TERMINAL'),'Existing canonical must have actual complete ordinary native evidence'
  for p in (dest,destdra):assert gf[str(p).lower()]['sha256']==sha(p)
  row={'target':target,'existing':True,'psm':str(dest),'psm_sha256':sha(dest),'dra':str(destdra),'dra_sha256':sha(destdra),'source_evidence':e['native_path'],'source_native_sha256':e['native_sha256'],'pin_numbers':e['pin_numbers'],'member_count':len(members)};existing.append(row);targets.append(row);continue
 assert not destdra.exists(),'Unexpected existing targetDRA without PSM'
 fam=members[0]['family'];size=members[0]['size'];generic=(fam+size).lower();sources=[e for e in members if e['stem'].lower()==generic]
 if len(sources)!=1:
  sources=[e for e in members if not e['stem'].lower().endswith('_pc') and 'ANOMALY' not in e['scope']]
 if len(sources)!=1:errors.append({'target':target,'error':'NO_UNIQUE_APPROVED_GENERIC_BASE','source_candidates':[e['stem'] for e in sources]});continue
 e=sources[0];assert e['pin_numbers']==['1','2'];src=Path(e['source']);dra=src.with_suffix('.dra');assert dra.exists();assert gf[str(src).lower()]['sha256']==sha(src) and gf[str(dra).lower()]['sha256']==sha(dra)
 pair=[]
 for srcfile,dstfile in ((src,dest),(dra,destdra)):
  pair.append({'source':str(srcfile),'source_sha256':sha(srcfile),'source_bytes':srcfile.stat().st_size,'target':str(dstfile),'target_expected_sha256':sha(srcfile),'target_must_be_absent':True,'independent_file_required':True})
 row={'target':target,'existing':False,'generic_source':e['stem'],'source_native_path':e['native_path'],'source_native_sha256':e['native_sha256'],'pin_numbers':e['pin_numbers'],'pair':pair,'member_count':len(members),'definition_policy':'Independent byte-identical PSM/DRA copies of approved publicgeneric source; no geometry edit, no hardlink, no existing target overwrite. Name alias cold-native proof follows.'};new.append(row);targets.append(row)
assert not errors,errors
out={'schema':'PUBLIC_CANONICAL_ADDITIONS_ONLY_PLAN_V1','status':'READY_TO_CREATE_NEW_ASSETS_ONLY_NO_EXISTING_FILE_WRITE_OR_DELETE','public_root':str(base),'old_public_guard':plan['public_guard_manifest'],'old_public_guard_sha256':sha(plan['public_guard_manifest']),'old_guarded_files':len(guard),'native_all941_report':str(M/'global_suffix_native_v3/report.json'),'native_all941_report_sha256':sha(M/'global_suffix_native_v3/report.json'),'source_native_plan':str(P),'source_native_plan_sha256':sha(P),'native_complete_exports':939,'native_failed_retired_by_DRA_intent':legacy_failed,'targets':targets,'new_target_count':len(new),'new_file_count':2*len(new),'new_targets':new,'existing_targets_preserved':existing,'ordinary_alias_count':sum(len(x) for x in bytarget.values())+len(legacy_failed),'post_publish_gate':'All existing+new canonical target PSM cold-native audit must pass; complete PAD/ref checks; then exact OLB/BRD application. Oldasset removal deferred until all live references close.','not_in_this_plan':['No oldPSM/DRA/TXT/PAD deletion','No existing generic/_pc overwrite','No OLB/DSN/BRD rewrite','No blanket AO topology equivalence','No DeviceTXT with internally stalePackage identity is created'],'special_cases_preserved':[{'stem':e['stem'],'scope':e['scope'],'pin_numbers':e['pin_numbers']} for e in reviews.values() if e['scope'] in ('FUNCTIONAL_NON_TWO_TERMINAL_PRESERVE','SPECIAL_CAPACITOR_MATERIAL_OR_FORM_PRESERVE_REVIEW')]}
(OUT/'CANONICAL_ADDITIONS_ONLY_PLAN.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'LEGACY_FAILED_INTENT_RETIREMENT_EXCEPTIONS.json').write_text(json.dumps(legacy_failed,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'new_targets':len(new),'new_files':len(new)*2,'existing_preserved':len(existing),'ordinary_aliases':out['ordinary_alias_count'],'target_source_pairs':[(x['target'],x['generic_source']) for x in new],'plan_sha256':sha(OUT/'CANONICAL_ADDITIONS_ONLY_PLAN.json')},ensure_ascii=False,indent=2))
