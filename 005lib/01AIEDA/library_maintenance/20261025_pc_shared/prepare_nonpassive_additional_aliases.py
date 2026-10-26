"""Freeze exactly the52full-PAD-equivalent relations and67whole-byte groups, plus boundedcurrent81 targets.
Names never prove equivalence; functional mismatches remain preserved. No CAD or public writes.
"""
from pathlib import Path
from collections import defaultdict,Counter
import copy,json,hashlib,re
M=Path(__file__).resolve().parent;O=M/'nonpassive_additional_aliases13';O.mkdir(exist_ok=True)
jr=lambda p:json.loads(Path(p).read_text('utf-8-sig'));sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
put=lambda n,v:(O/n).write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
root=Path(r'D:\001DIY\005lib\01Psm_lib');guard=M/'project81_exact_additions13/PUBLIC_GUARD_13425.json';guards={x['path'].lower():x for x in jr(guard)['files']}
allrows=jr(M/'global_nonpassive_inventory_v1/ALL_PUBLIC_PSM_INVENTORY.json')['files'];files={r['stem'].lower():r for r in allrows}
idx={};padxml={}
for folder in ['global_suffix_native_review_v3','global_nonpassive_native_review13','global_nonpassive_increment_review13','global_canonical_targets_review13','project81_current_targets_review13','project81_exact_targets_review13']:
 for f in (M/folder).glob('e*_SCHEMA_GEOMETRY.json'):
  for e in jr(f):
   for n in [e['stem']]+[Path(x).stem for x in e.get('byte_identical_members',[])]:idx[n.lower()]=e
 for p in jr(M/folder/'FULL_PAD_XML_BINDING.json')['records']:padxml[p['path'].lower()]=p
def physical_key(e):
 out=[]
 for p in e['pins']:
  ds=[x for x in e['actual_loaded_pad_files'] if Path(x['path']).stem.lower()==p['pad_name'].lower()];assert len(ds)==1
  ps=padxml[ds[0]['path'].lower()];assert ps['current_sha256']==ds[0]['sha256']
  out.append([p['number'],p['local_xy_mm'],p['local_rotation'],p['mirror_type'],p['is_mechanical'],p['is_through'],ps['all_classified_manufacturing_fields_signature']])
 return json.dumps(out,sort_keys=True)
parent={}
def find(n):
 parent.setdefault(n,n)
 if parent[n]!=n:parent[n]=find(parent[n])
 return parent[n]
def union(a,b):parent[find(a)]=find(b)
pairs=jr(M/'global_nonpassive_comparison13/CANDIDATE_PAIR_FULL_NATIVE_COMPARISON.json');safe=[r for r in pairs if r['gate'].startswith('FULL_NUMBERED')];assert len(safe)==52
for r in safe:union(r['candidate'],r['possible_base'])
byte=jr(M/'global_nonpassive_comparison13/WHOLE_BYTE_GROUP_NATIVE_REVIEW.json');assert len(byte)==67 and all(r['status'].startswith('ACTUAL_COMPLETE') for r in byte)
for r in byte:
 for n in r['members']:union(n,r['members'][0])
# Two separately named sourcegroups are actually the same numberedSOT23 pad-core, as are the same-slot groups.
# Exact fullmanufacturing core proves these crossrelations; no crossfamily guesses.
families=defaultdict(list)
for n in parent:
 family='SOT23_SINGLE1' if n in {'a3212elhlt-t_sot23w-3','psot24c_sot23-3','tp0610k-t1-e3_sot23-3','ao3413_sot23-3','ao3414_sot23-3'} else 'LEGACY_SLOT' if n.startswith('ole_2f_pth') else None
 if family:families[(family,physical_key(idx[n]))].append(n)
for ns in families.values():
 for n in ns:union(n,ns[0])
clusters=defaultdict(list)
for n in parent:clusters[find(n)].append(n)
project=jr(M/'project81_final_canonical_plan13/ALL81_PACKAGE_CANONICAL_DECISIONS.json');cur_targets={r['source_package'].lower():r['target'].lower() for r in project};keep={r['target'].lower() for r in project}
ordinary=jr(M/'global_canonical_publish_v1/CANONICAL_ADDITIONS_ONLY_PLAN.json');keep|={r['target'].lower() for r in ordinary['targets']}
new={
 'sot23_3p_single1_pc':('ao3413_sot23-3','Distinctnumbering:pin1on single side,2/3paired. Do not overwrite genericSOT23-3 whosepaired pins1/2.'),
 'th_2p_p2d54_drill0d9906_pc':('ec1p25c_2_12','Actual2pad platedTH pitch2.54mm/drill0.9906mm. No guessedR/C/connector category from legacyECname.'),
 'slot_pth_1d3x0d508_oblong_land1d6x0d762_pc':('ole_2f_pth_2f_r0_762x1_6d0_516','Actualslothole1.299972x0.508mm,allcopperoblong land1.599946x0.762mm. Keepseparatefromrect-top largerland.'),
 'slot_pth_1d35x0d508_rect_land1d6x0d8128_pc':('ole_2f_pth_2f_r0_8128x1_6d0_11','Actualslothole1.35001x0.508mm,rectTOPland1.599946x0.8128mm; differenthole/land preserved.')}
manual={'ao3413_sot23-3':'sot23_3p_single1_pc','ec1p25c_2_12':'th_2p_p2d54_drill0d9906_pc','ole_2f_pth_2f_r0_762x1_6d0_516':'slot_pth_1d3x0d508_oblong_land1d6x0d762_pc','ole_2f_pth_2f_r0_8128x1_6d0_11':'slot_pth_1d35x0d508_rect_land1d6x0d8128_pc','magic_r22':'l_r22_pc','pin05_2d54mm_1x4dip':'pin05_2d54mm_1x5dip','xh-0p-2d54-w-dip':'xh-5p-2d54-w-dip','fix_2d6':'fix_2d5','so8_50_150gv':'sop-8-e-150mil','1n4148ws-7-sod323':'sod323'}
def score(n):
 generic=bool(re.match(r'^(?:sot|sop|tssop|qfn|dfn|lga|lqfp|to-|sod|do-|hdr|pin|gh-|xh-|fpc|zif|tps|usb|sata|isen|prpak|mini|mth|fix|e\d)',n))
 return (0 if n in keep else 1,0 if generic else 1,1 if re.search(r'(?:_\d+)+$',n) else 0,len(n),n)
rows=[];groups=[]
for members in sorted(clusters.values(),key=lambda ns:min(ns)):
 members=sorted(members);choices={manual[n] for n in members if n in manual}
 choices|={cur_targets[n] for n in members if n in cur_targets and cur_targets[n]!=n}
 protected=keep&set(members)
 if choices:
  assert len(choices)==1,(members,choices);target=next(iter(choices))
 elif protected:
  assert len(protected)==1,(members,protected);target=next(iter(protected))
 else:target=min(members,key=score)
 assert target not in set(members)&keep or target in protected
 g={'members':members,'canonical':target,'source_representative':members[0],'native_pin_numbers':idx[members[0]]['pin_numbers'],'native_pin_count':idx[members[0]]['pin_count'],'native_complete_graph_source':idx[members[0]]['native_path'],'full_PAD_XML_equivalent_within_group':True,'graphics_differences_retained_as_evidence':True,'new_exact_semantic_target':target in new,'canonical_target_current81_or_passive_KEEP':target in keep}
 groups.append(g)
 for n in members:
  if n==target:continue
  assert n not in keep,(n,'KEEPtargetwouldberetired')
  e=idx[n];assets=[]
  for ext in ['psm','dra','txt']:
   p=root/(n+'.'+ext)
   if not p.exists():continue
   a=guards.get(str(p).lower());assert a and sha(p)==a['sha256'];assets.append({'path':str(p),'sha256':a['sha256'],'bytes':p.stat().st_size})
  rows.append({'source':n,'target':target,'action':'MIGRATE_NATIVE_REFERENCES_THEN_RETIRE_CONFIRMED_NONPASSIVE_ALIAS','scope':'EXACT_NUMBERED_PIN_AND_FULL_PAD_MANUFACTURING_GROUP' if target in members or target in new else 'CURRENT81_ALREADY_FROZEN_SAME_CASE_STANDARDIZATION_TARGET','geometry_equivalent_claim':False,'physical_numbered_PAD_manufacturing_equivalent_to_final_target':target in members or target in new,'complete_graph_equal_to_existing_target':e['full_ordered_graph_fingerprint']==idx[target]['full_ordered_graph_fingerprint'] if target in idx else None,'native_output':e['native_path'],'native_sha256':e['native_sha256'],'source_psm_sha256':e['source_sha256'],'source_pin_numbers':e['pin_numbers'],'source_asset_set':assets,'retirement_gate':'Finaltargetcoldnative and everypublicOLB/DSN/7BRD/project referenceactualzero, then archiveall exactmembers and atomicallyretireonlyPSM/DRA/selfTXT. NoPAD/SHAPE removal.','group':members})
# Preserve all distinct current81 targetnames; include their approved source redirects without expanding84-bound project scope.
existing={r['source']:r for r in rows}
for p in project:
 n=p['source_package'].lower();target=p['target'].lower()
 if n==target or n in existing:continue
 if n in keep:raise ValueError('CurrentKEEP source must not retire '+n)
 if n not in files:continue
 assets=[]
 for ext in ['psm','dra','txt']:
  f=root/(n+'.'+ext)
  if f.exists():a=guards[str(f).lower()];assert sha(f)==a['sha256'];assets.append({'path':str(f),'sha256':a['sha256'],'bytes':f.stat().st_size})
 rows.append({'source':n,'target':target,'action':'MIGRATE_NATIVE_REFERENCES_THEN_RETIRE_FROZEN_CURRENT81_STANDARDIZATION_SOURCE','scope':'CURRENT81_BOUNDED_84REF_EXPLICIT_NON_EQUIVALENT_STANDARDIZATION','geometry_equivalent_claim':False,'native_output':p.get('target_native_path'),'native_sha256':p.get('target_native_sha256'),'source_psm_sha256':files[n]['sha256'],'source_pin_numbers':p['pin_numbers'],'source_asset_set':assets,'retirement_gate':'Same complete native closures as above; respect all84 pad/stub proofs, preserveoriginalSCH/PCBdifferences.'})
assert len({r['source'] for r in rows})==len(rows)
mapping={r['source']:r['target'] for r in rows};assert not set(mapping)&set(mapping.values()),'Nochains/cycles;targetsareKEEP'
preserved=[{k:r.get(k) for k in ['candidate','possible_base','name_relation','gate','source_pin_count','target_pin_count','source_pin_numbers','target_pin_numbers','source_pin_summary','target_pin_summary','missing_native']} for r in pairs if not r['gate'].startswith('FULL_NUMBERED')]
plan={'status':'FROZEN_NATIVE_CONFIRMED_NONPASSIVE_ALIAS_MAPPINGS','basis_52_full_PAD_equivalent_pair_relations':52,'basis_67_full_byte_groups':67,'source_group_clusters_before_cross_exact_core':82,'clusters_after_same_family_full_PAD_exact_cross_merge':len(groups),'full_group_names':len(parent),'row_count':len(rows),'rows':rows,'KEEP_canonical_targets':sorted(keep|set(mapping.values())),'groups':groups,'preserved_non_equivalent_or_failed_candidates':preserved,'native_failed_preserve':['sot-23','smb'],'new_semantic_exact_targets':{k:{'source':v[0],'reason':v[1]} for k,v in new.items()},'root_requirement':'Root publishes4new exactsemantic targets andcoldreads; baseline scans all37OLB/2DSN/7BRD, includingVCU16; no existingtarget overwritten, no PADremoved. Current81samecasetargetchoices alreadyfrozen.'};put('NONPASSIVE_ADDITIONAL_ALIAS_PLAN.json',plan)
# Root's proven additions-only publisher; only four newtargets. Same source parent+exactPSM/DRA bytes, no hardlinks.
sourceplans=[jr(M/'global_suffix_inventory_v1/PSM_NATIVE_AUDIT_PLAN.json'),jr(M/'global_nonpassive_plan_review_v1/NONPASSIVE_351_275_EXEC_PLAN.json'),jr(M/'global_nonpassive_increment_v1/INCREMENTAL_ALIAS_NATIVE_EXEC_PLAN.json')]
combined=copy.deepcopy(sourceplans[0]);byname={r['stem'].lower():r for p in sourceplans for r in p['representatives']}
for target,(source,reason) in new.items():
 if source not in byname:
  origin=copy.deepcopy(byname[idx[source]['stem'].lower()]);f=files[source];origin.update(path=f['path'],relative=f['relative'],stem=source,sha256=f['sha256'],bytes=f['bytes'],byte_identical_members=[f['path']]);byname[source]=origin
combined['representatives']=list(byname.values());combined['public_guard_manifest']=str(guard);cp=O/'COMBINED_ORIGINAL_NATIVE_INPUT_PLAN.json';put(cp.name,combined)
targets=[]
for target,(source,reason) in new.items():
 assert source in byname and not(root/(target+'.psm')).exists() and not(root/(target+'.dra')).exists();pair=[]
 for ext in ['psm','dra']:
  f=root/(source+'.'+ext);assert f.exists();pair.append({'source':str(f),'source_sha256':sha(f),'source_bytes':f.stat().st_size,'target':str(root/(target+'.'+ext)),'target_expected_sha256':sha(f),'target_must_be_absent':True,'independent_file_required':True})
 targets.append({'target':target,'existing':False,'generic_source':source,'source_native_path':idx[source]['native_path'],'source_native_sha256':idx[source]['native_sha256'],'pin_numbers':idx[source]['pin_numbers'],'pair':pair,'reason':reason})
publish={'schema':'PUBLIC_CANONICAL_ADDITIONS_ONLY_PLAN_V1','status':'EXACT_FOUR_SEMANTIC_NATIVE_CONFIRMED_CASE_ADDITIONS_ONLY_NOT_EXECUTED','public_root':str(root),'old_public_guard':str(guard),'old_public_guard_sha256':sha(guard),'old_guarded_files':13425,'source_native_plan':str(cp),'source_native_plan_sha256':sha(cp),'targets':targets,'new_targets':targets,'new_target_count':len(targets),'new_file_count':2*len(targets),'existing_targets_preserved':[],'post_publish_gate':'Everytarget cold-native fullgraph+fullPADXML before reference migration; source oldassets untouched.'};put('NONPASSIVE_FOUR_EXACT_CANONICAL_ADDITIONS_PLAN.json',publish)
summary={'status':'ADDITIONAL_NONPASSIVE_ALIAS_AND_NATIVE_REF_REDIRECTS_FROZEN_NO_PUBLIC_WRITES','groups':len(groups),'names':len(parent),'additional_redirects_including_bounded_current81':len(rows),'new_exact_semantic_canonical_targets':len(targets),'new_PSM_DRA_files':8,'preserved_distinct_or_failed_candidate_relations':len(preserved),'nonpassive_alias_plan':str(O/'NONPASSIVE_ADDITIONAL_ALIAS_PLAN.json'),'nonpassive_alias_plan_sha256':sha(O/'NONPASSIVE_ADDITIONAL_ALIAS_PLAN.json'),'new_exact_additions_plan':str(O/'NONPASSIVE_FOUR_EXACT_CANONICAL_ADDITIONS_PLAN.json'),'new_exact_additions_plan_sha256':sha(O/'NONPASSIVE_FOUR_EXACT_CANONICAL_ADDITIONS_PLAN.json'),'protected_KEEP_count':len(plan['KEEP_canonical_targets']),'no_target_is_retired':True,'no_canonical_chains_or_cycles':True};put('ADDITIONAL_ALIASES_READY.json',summary);print(json.dumps(summary,indent=2))
