from pathlib import Path
from collections import defaultdict,Counter
import hashlib,json,re
M=Path(r'D:\001DIY\005lib\01AIEDA\library_maintenance\20261025_pc_shared');OUT=M/'global_nonpassive_inventory_v1';ROOT=Path(r'D:\001DIY\005lib\01Psm_lib')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def dump(n,v):(OUT/n).write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
def need(v,m):
 if not v:raise ValueError(m)
planpath=M/'global_suffix_inventory_v1/PSM_NATIVE_AUDIT_PLAN.json';old=json.loads(planpath.read_text(encoding='utf-8-sig'));gp=Path(old['public_guard_manifest']);guard=json.loads(gp.read_text(encoding='utf-8-sig'))
need(not OUT.exists(),'Fresh output required');OUT.mkdir()
frozen={v['path'].casefold():v for v in guard['files']};files=[]
for p in sorted(ROOT.rglob('*.psm'),key=lambda p:str(p).casefold()):
 v=frozen.get(str(p).casefold());need(v and v['sha256']==sha(p),'Public PSM changed against frozen guard');files.append(dict(v,stem=p.stem,extension='.psm'))
need(sum(Path(v['path']).suffix.casefold()=='.psm' and str(Path(v['path']).parent).casefold()==str(ROOT).casefold() for v in guard['files'])==len(files),'PSM enumeration mismatch')
prior={v['path'].casefold() for v in old['representatives']};byname=defaultdict(list)
for v in files:byname[v['stem'].casefold()].append(v)
left=[v for v in files if v['path'].casefold() not in prior]
family_re=re.compile(r'(?:^|[_-])(sot|sop|soic|ssop|tssop|tsop|msop|dfn|qfn|wson|vqfn|u?qfp|lqfp|tqfp|bga|fbga|tfbga|lga|plcc|dip|sip|sc70)(?=[0-9_-])',re.I)
conn_re=re.compile(r'(?:^|[_-])(con|conn|connector|header|jack|usb|hdmi|rj45|pcie|sata|dimm|fpc|ffc|jst|molex|samtec|he10)(?=$|[0-9_-])',re.I)
relations=[];familyrows=[]
for v in left:
 s=v['stem'];low=s.casefold();family=family_re.search(low);con=conn_re.search(low)
 if family or con:familyrows.append({'path':v['path'],'stem':s,'family':(family or con).group(1).upper(),'kind':'PACKAGE_FAMILY' if family else 'CONNECTOR_FAMILY'})
 numeric=re.sub(r'(?:_+\d+)+$','',low)
 if numeric!=low and numeric in byname:
  relations.append({'kind':'TRAILING_NUMERIC_SUFFIX_WITH_EXISTING_BASE','candidate':s,'possible_bases':[p['stem'] for p in byname[numeric]],'warning':'Digits may encode dimensions, pin count or functional variant. Native pin/geometry required.'})
 for target in byname:
  if len(target)<4 or target==low:continue
  if (low.endswith('_'+target) or low.endswith('-'+target)) and (family_re.match(target) or conn_re.match(target)):
   relations.append({'kind':'MODEL_PREFIX_EXISTING_GENERIC_SUFFIX','candidate':s,'possible_bases':[p['stem'] for p in byname[target]],'warning':'Named chip/connector pin numbering may differ. Complete native pad-number binding is mandatory.'})
 norm=re.sub(r'[-_]','',low)
 for target in byname:
  if target!=low and re.sub(r'[-_]','',target)==norm:
   relations.append({'kind':'PUNCTUATION_ONLY_NAME_CANDIDATE','candidate':s,'possible_bases':[p['stem'] for p in byname[target]],'warning':'No geometric equality inferred from spelling.'})
bg=defaultdict(list)
for v in files:bg[v['sha256']].append(v)
identical=[vs for vs in bg.values() if len(vs)>1 and any(v['path'].casefold() not in prior for v in vs)]
related={r['candidate'].casefold() for r in relations}|{b.casefold() for r in relations for b in r['possible_bases']}
selected=[v for v in files if v['stem'].casefold() in related or any(v['path']==f['path'] for group in identical for f in group)]
selected_unique={v['sha256']:v for v in selected};reps=[]
for i,v in enumerate(sorted(selected_unique.values(),key=lambda v:v['stem'].casefold())):
 reps.append(dict(v,representative_index=i,native_audit=True,classification='NAME_CANDIDATE_ONLY_NATIVE_UNVERIFIED_DO_NOT_MERGE',byte_identical_members=[p['path'] for p in selected if p['sha256']==v['sha256']]))
audit=dict(old,schema='GLOBAL_NONPASSIVE_PUBLIC_NATIVE_AUDIT_PLAN_V1',status='PREPARED_NOT_EXECUTED_NAME_CANDIDATES_NOT_EQUIVALENCE',selected_psm_count=len(selected),exact_byte_group_count=len(reps),native_representative_count=len(reps),representatives=reps,canonical_policy={'policy':'Do not merge based on name. Preserve pin-number, G/S/D, thermal pad, drill/mask/paste/copper/SHAPE/full properties; functional/connector pin count and geometry require full native proof.'})
dump('PSM_NATIVE_AUDIT_PLAN.json',audit);dump('ALL_PUBLIC_PSM_INVENTORY.json',{'public_guard':str(gp),'sha256':sha(gp),'files':files});dump('NAME_CANDIDATE_RELATIONS.json',{'relations':relations,'exact_byte_groups':identical,'all_remaining_family_members':familyrows,'all_nonprior_941_remaining_files':left})
summary={'status':'READONLY_INVENTORY_COMPLETE_NO_EQUIVALENCE_NO_PUBLIC_CHANGE','all_psm':len(files),'previous_plan_representatives':len(prior),'remaining_nonprior_psm':len(left),'remaining_family_name_members':len(familyrows),'family_counts':dict(Counter(v['family'] for v in familyrows)),'name_relation_counts':dict(Counter(v['kind'] for v in relations)),'distinct_candidate_names':len({v['candidate'] for v in relations}),'exact_byte_duplicate_groups_involving_remaining':len(identical),'native_candidate_union_psm':len(selected),'native_representatives_by_full_SHA':len(reps),'all_psm_current_SHA_equal_original_guard':True,'public_guard':str(gp),'public_guard_sha256':sha(gp),'prior_native_plan':str(planpath),'prior_native_plan_sha256':sha(planpath),'candidate_plan':str(OUT/'PSM_NATIVE_AUDIT_PLAN.json'),'script_sha256':sha(__file__),'policy':'Read-only inventory. Candidate relations are not approved aliases. No public deletion or mutation. Native source/pin schema proof mandatory. 941 cohort stays separate; selected union includes any counterpart from that cohort for cross-boundary native comparison.'}
dump('NONPASSIVE_INVENTORY_SUMMARY.json',summary);print(json.dumps(summary,ensure_ascii=False))
