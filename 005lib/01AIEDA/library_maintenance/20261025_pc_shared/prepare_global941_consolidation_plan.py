from pathlib import Path
from collections import Counter
import csv,json,hashlib,xml.etree.ElementTree as ET
M=Path(r'D:\001DIY\005lib\01AIEDA\library_maintenance\20261025_pc_shared');R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025');OUT=M/'global_canonical_publish_v1'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper();jr=lambda p:json.loads(Path(p).read_text(encoding='utf-8-sig'))
plan=jr(M/'global_suffix_inventory_v1/PSM_NATIVE_AUDIT_PLAN.json');guard=jr(plan['public_guard_manifest'])['files'];g={x['path'].lower():x for x in guard};frozen={r['stem'].lower():r for r in plan['representatives']};rv={e['stem'].lower():e for p in (M/'global_suffix_native_review_v3').glob('e*_SCHEMA_GEOMETRY.json') for e in jr(p)}
addition=jr(OUT/'CANONICAL_ADDITIONS_ONLY_PLAN.json');failed={r['stem']:r for r in addition['native_failed_retired_by_DRA_intent']};olb=jr(R/'verification/public_olb_footprint_audit13_v4/PUBLIC_OLB_FOOTPRINT_REFERENCE_AUDIT.json');oc=Counter()
for n,v in olb['all_PCB_Footprint_value_counts'].items():oc[n.lower()]+=v
pubdsn=jr(R/'verification/public_dsn_footprint_audit13/PUBLIC_DSN_FOOTPRINT_REFERENCE_AUDIT.json');dc=Counter()
for d in pubdsn['designs']:
 for n,v in d['all_PCB_Footprint_value_counts'].items():dc[n.lower()]+=v
old=jr(Path(r'D:\001DIY\004computer\lga1700\cadence_library_cleanup_20261025\usage_audit\usage_counts.json'));bs=[s for s in old['sources'] if '\\01brdlib\\' in s['source'].lower()]
xml=R/'w/xn1/native_design.xml';xc=Counter()
for p in ET.parse(xml).getroot().iter('PartInst'):
 props={d.get('name'):d.get('val','') for d in p.findall('./PartInstUserProp/Defn')};xc[props.get('PCB Footprint','').lower()]+=1
with (R/'w/final_alt13/symbols.tsv').open(encoding='utf-8-sig',newline='') as f:
 pc=Counter(r['symbol_name'].strip('"').lower() for r in csv.DictReader(f,delimiter='\t',quoting=csv.QUOTE_NONE))
rows=[]
for stem,item in frozen.items():
 e=rv.get(stem);exception=failed.get(stem);refs={'public37_OLB_fields':oc[stem],'public2_DSN_fields':dc[stem],'public7_BRD_declared':sum(s['counts']['declared_psm'].get(stem,0) for s in bs),'public7_BRD_placed':sum(s['counts']['psm'].get(stem,0) for s in bs),'project13_capture_instances':xc[stem],'project13_PCB_placed':pc[stem]};target=None;eq=False
 if exception:scope=exception['classification'];target='c0603_pc';action='RETIRE_BROKEN_UNUSED_LEGACY_AFTER_REFERENCE_CLOSURE'
 elif e['scope'].startswith('ORDINARY_TWO_TERMINAL'):
  scope=e['scope'];target=e['canonical_candidate'] or e['family']+e['size']+'_pc';action='KEEP_EXISTING_CANONICAL' if stem==target.lower() else 'MIGRATE_REFERENCES_THEN_RETIRE_OLD_ASSET_SET'
 elif e['scope'] in ('FUNCTIONAL_NON_TWO_TERMINAL_PRESERVE','SPECIAL_CAPACITOR_MATERIAL_OR_FORM_PRESERVE_REVIEW'):
  scope=e['scope'];target=item['stem'];action='PRESERVE_DISTINCT_FUNCTIONAL_OR_MATERIAL_SCHEMA'
 elif e['scope']=='CATEGORY_AMBIGUOUS_KEEP_UNTIL_ALL_REFERENCE_REDIRECTION':
  scope=e['scope'];action='RESOLVE_CATEGORY_PER_REFERENCED_COMPONENT_THEN_RETIRE' if sum(refs.values()) else 'RETIRE_UNUSED_CATEGORY_AMBIGUOUS_ALIAS_AFTER_FINAL_REFERENCE_SCAN'
 elif stem in ('ao3414_sot23-3','ao4468_so8'):
  scope=e['scope'];target={'ao3414_sot23-3':'sot23-3','ao4468_so8':'sop-8-150mil'}[stem];assert sum(refs.values())==0;action='RETIRE_UNUSED_MODEL_PREFIX_ALIAS_WITH_PIN_TOPOLOGY_WARNING'
 elif stem=='sot23_123':scope=e['scope'];target='sot23-3';action='MIGRATE_34_ACTIVE_PROJECT_INSTANCES_AND_NATIVE_PCB_THEN_RETIRE'
 else:scope=e['scope'];target=item['stem'];action='KEEP_GENERIC_CANONICAL'
 assets=[]
 for ext in ('.psm','.dra','.txt'):
  p=Path(item['path']).with_suffix(ext)
  if p.is_file():assets.append({'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size})
 rows.append({'source':item['stem'],'source_psm_sha256':item['sha256'],'target':target,'action':action,'scope':scope,'geometry_equivalent_claim':eq,'active_reference_counts':refs,'native_output':e['native_path'] if e else None,'native_sha256':e['native_sha256'] if e else None,'source_pin_numbers':e['pin_numbers'] if e else ['1','2'],'source_asset_set':assets,'retirement_gate':'Backup verified; all intended OLB/DSN/BRD logical+placed references redirected and rechecked; every final target cold-native passes; no sourcePAD removal by this plan.','exception_proof':exception if exception else None})
result={'schema':'PUBLIC941_FROZEN_ALIAS_CONSOLIDATION_PLAN_V1','status':'REVIEWED_SOURCE_CLASSIFICATION_AND_NEW_TARGET_PLAN_OLD_REMOVAL_NOT_EXECUTED','source_count':len(rows),'complete_native_outputs':939,'native_failed_with_two_terminal_DRA_intent':2,'all941_source_public_guard_unchanged':True,'new_target_plan':str(OUT/'CANONICAL_ADDITIONS_ONLY_PLAN.json'),'new_target_plan_sha256':sha(OUT/'CANONICAL_ADDITIONS_ONLY_PLAN.json'),'new_canonical_targets':30,'existing_canonical_targets_preserved':8,'ordinary_two_terminal_aliases':924,'action_counts':dict(Counter(r['action'] for r in rows)),'rows':rows,'not_covered':'Other2442publicPSM candidates are independently inventoried in global_nonpassive_inventory_v1; not silently included in941 or merged by names.','warnings':['All geometry_equivalent_claim fields false by default; user authorizes ordinarysize standardization with explicit physical delta, not falsified identical-geometry claims.','AO3414 alias has different physical pin-number topology; audited current refs0 permits unused retirement but unknown routed-design substitution is not safe.','13SOT34 source/target label topology matches; unchangedpose actualendpoint geometry preflight passed, but nativeGetConnect and full electrical/PST gates remain required.','True multi-terminal/multi-pin and specialcaps are preserved; a common size prefix alone does not justify replacing them.']}
(OUT/'ALIAS_CONSOLIDATION_PLAN_941.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in result.items() if k not in ('rows','warnings')},ensure_ascii=False,indent=2));print(sha(OUT/'ALIAS_CONSOLIDATION_PLAN_941.json'))
