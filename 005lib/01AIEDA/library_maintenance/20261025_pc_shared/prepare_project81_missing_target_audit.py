"""Only explicit current81 generic target candidates not already independently cold-read."""
from pathlib import Path
import json,hashlib,copy
M=Path(__file__).resolve().parent
jr=lambda p:json.loads(Path(p).read_text('utf-8-sig'));sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
P=M/'global_nonpassive_increment_v1/INCREMENTAL_ALIAS_NATIVE_EXEC_PLAN.json';p=jr(P)
allr=jr(M/'global_nonpassive_inventory_v1/ALL_PUBLIC_PSM_INVENTORY.json')['files'];idx={r['stem'].lower():r for r in allr}
seen=set()
for d in ['global_suffix_native_review_v3','global_nonpassive_native_review13','global_nonpassive_increment_review13','global_canonical_targets_review13']:
 for f in (M/d).glob('e*_SCHEMA_GEOMETRY.json'):
  for e in jr(f):seen.add(e['source_sha256'])
names=['sop-8-e-150mil','sop-8-e','sop-8e-spad','ot-23-3_l2_9-w1_3-p1_90-ls2_1','sot23-akak','smd_bd5_6-d3_6','smd_bd5_6-d3_6_1','smd_bd5_6-d3_6_2','qfn32_4x4','qfn32_4x4_minpad','qfn32_5x5','qfn32_5x5mm_ep3p3mm','rtl8111g_qfn32']
reps=[];selected=[]
for n in names:
 if n not in idx:continue
 r=copy.deepcopy(idx[n]);selected.append(n)
 if r['sha256'] in seen:continue
 members=[x['path'] for x in allr if x['sha256']==r['sha256']]
 assert sha(r['path'])==r['sha256'];r.update(representative_index=len(reps),canonical_candidate=None,family='NONPASSIVE_UNCLASSIFIED',size='',suffix='',native_audit=True,classification='ACTUAL_CURRENT81_TARGET_CANDIDATE_NO_EQUIVALENCE_ASSUMED',byte_identical_members=members);reps.append(r);seen.add(r['sha256'])
p.update(status='CURRENT81_ONLY_MISSING_EXPLICIT_TARGET_CANDIDATE_NATIVE_PLAN',representatives=reps,selected_psm_count=sum(len(x['byte_identical_members']) for x in reps),exact_byte_group_count=len(reps),native_representative_count=len(reps),scope_original_candidate_files=sum(len(x['byte_identical_members']) for x in reps),scope_native_representatives=len(reps),current81_explicit_names=selected)
O=M/'project81_current_target_native_plan';O.mkdir(exist_ok=True);out=O/'CURRENT81_MISSING_TARGET_NATIVE_PLAN.json';out.write_text(json.dumps(p,indent=2),encoding='utf-8');print(json.dumps({'plan':str(out),'sha256':sha(out),'native_representatives':len(reps),'stems':[r['stem'] for r in reps]},indent=2))
