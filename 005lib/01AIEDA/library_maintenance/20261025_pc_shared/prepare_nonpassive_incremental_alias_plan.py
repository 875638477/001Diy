"""Read-only actual-name relation increment. Names are candidates, never merge proof."""
from pathlib import Path
from collections import defaultdict,Counter
import json,re,hashlib,copy
M=Path(__file__).resolve().parent;O=M/'global_nonpassive_increment_v1';O.mkdir(exist_ok=True)
jr=lambda p:json.loads(Path(p).read_text('utf-8-sig'))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
I=M/'global_nonpassive_inventory_v1';P=M/'global_nonpassive_plan_review_v1/NONPASSIVE_351_275_EXEC_PLAN.json'
allrows=jr(I/'ALL_PUBLIC_PSM_INVENTORY.json')['files'];prior=jr(M/'global_suffix_inventory_v1/PSM_NATIVE_AUDIT_PLAN.json');first=jr(P)
byname={r['stem'].lower():r for r in allrows};bysha=defaultdict(list)
for x in allrows:bysha[x['sha256']].append(x)
seen={x['sha256'] for plan in (prior,first) for x in plan['representatives']}
norm=lambda x:re.sub(r'[^a-z0-9]','',x.lower())
normalized=defaultdict(list)
for n in byname:normalized[norm(n)].append(n)
relations=[]
def add(a,b,kind,explanation):
 if a==b or a not in byname or b not in byname:return
 if byname[a]['sha256'] in seen and byname[b]['sha256'] in seen:return
 relations.append({'candidate':a,'possible_base':b,'kind':kind,'evidence':explanation,'automatic_equivalence':False,'required_gate':'Actual numbered-pin/complete geometry + PAD native manufacturing identity; topology/functional differences are preserved.'})
# Existing generic suffix under an actual part model. Expand prior family grammar to SO/SOD/TO/SON/MLP.
generic=re.compile(r'^(?:so(?:ic)?[-_]?\d|sod[-_]?\d|to[-_]?\d|(?:x|u)?son[-_]?\d|(?:u|t|p)?dfn[-_]?\d|ml[fp]\d|sma$|smb$|smc$)',re.I)
for a in byname:
 for idx,ch in enumerate(a):
  if ch not in '_- ' or idx==0:continue
  tail=a[idx+1:]
  if not generic.match(tail):continue
  # Exact existing generic, or punctuation-only spelling of that generic.
  for b in normalized.get(norm(tail),[]):add(a,b,'MODEL_PREFIX_EXISTING_EXPANDED_GENERIC','Actual generic stem equals full suffix after punctuation normalization; no dimensional suffix was discarded.')
  # -2 or -2p explicitly denotes a possible two-pin SOD variant, subject to native proof.
  if re.fullmatch(r'sod[-_]?\d+[-_]2p?',tail):
   stem=re.sub(r'[-_]2p?$','',tail)
   for b in normalized.get(norm(stem),[]):add(a,b,'MODEL_PREFIX_SOD2_WITH_EXISTING_GENERIC','Named SOD model suffix with explicit 2/2p token; generic exists. Pin count/topology and actual pad differences still require native check.')
# Case-family variants with a literal existing parent stem; retain all suffix semantics in report.
for a in byname:
 if not generic.match(a):continue
 for b in byname:
  if a.startswith(b) and a!=b and generic.match(b):
   tail=a[len(b):]
   if tail and (tail[0] in '_- ' or tail in ('f','fl','w','bi')):
    add(a,b,'LITERAL_EXISTING_CASE_PARENT_PLUS_EXPLICIT_SUFFIX','Parent is an actual full public stem; suffix '+repr(tail)+' may be functional and is never silently dropped.')
# Well-known nomenclature candidate families. These are comparison hints, not asserted interchangeability.
explicit=[
 ('so8','sop-8-150mil'),('so8-25x75','so8'),('so-8w','so8'),
 ('do-214aa_smb','smb'),('do-214ac_sma','do-214ac'),
 ('sod-323f_sc-90','sod-323f'),('sod-523_sc-79','sod-523'),
 ('osc3225','osc_smd_3225'),('xtal3225','xtal_32x25_4p'),
 ('xtal-smd_2f_3_2x2_5','xtal-smd_3_2x2_5'),
 ('son-8_5x6m-9pin','son-8p-5x6_9ps'),('son-8p-5x6mm','son-8p-5x6_9ps'),
 ('to-92-1e2b3c','to-92-3'),('to-92-1e2c3b','to-92-3')]
for a,b in explicit:add(a,b,'EXPLICIT_INDUSTRY_OR_SAME_LITERAL_DIMENSION_CANDIDATE','Spelling/family/dimension suggests comparison only. Includes deliberately different pin-map/extra-pad risks; a native mismatch must preserve both definitions.')
# All byte identity is already covered by prior351 inventory. Verify rather than claim a new duplicate set.
relations=list({(r['candidate'],r['possible_base'],r['kind']):r for r in relations}.values())
names={r[k] for r in relations for k in ('candidate','possible_base')}
newhashes={byname[n]['sha256'] for n in names}-seen
reps=[]
for idx,h in enumerate(sorted(newhashes,key=lambda h:min(x['stem'].lower() for x in bysha[h]))):
 members=sorted(bysha[h],key=lambda x:x['stem'].lower());r=copy.deepcopy(members[0]);r.update(representative_index=idx,byte_identical_members=[x['path'] for x in members],canonical_candidate=None,family='NONPASSIVE_UNCLASSIFIED',size='',suffix='',native_audit=True,classification='ACTUAL_NAME_RELATION_INCREMENT_NOT_EQUIVALENCE');reps.append(r)
plan=copy.deepcopy(first);plan.update(status='RUNNABLE_ADDITIONAL_TRUE_NAME_RELATION_CANDIDATES_NOT_MERGE_PROOF',representatives=reps,selected_psm_count=sum(len(r['byte_identical_members']) for r in reps),exact_byte_group_count=len(reps),native_representative_count=len(reps),scope_original_candidate_files=sum(len(r['byte_identical_members']) for r in reps),scope_native_representatives=len(reps),original_nonpassive_plan=str(P),original_nonpassive_plan_sha256=sha(P),candidate_relations=relations,excluded_prior_native_sha256_count=len(seen))
for r in reps:
 for n in r['byte_identical_members']:assert sha(n)==r['sha256']
pp=O/'INCREMENTAL_ALIAS_NATIVE_EXEC_PLAN.json';pp.write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
coverage=jr(M/'global_nonpassive_plan_review_v1/NONPASSIVE_PLAN_REVIEW.json')
uncovered=[x for x in coverage['additional_family_candidates'] if not x['already_selected_by_name_or_byte_relation']]
report={'status':'READONLY_INCREMENTAL_CANDIDATES_PREPARED_NO_CAD_NO_LIBRARY_MUTATION','all_original_public_psm_name_and_sha_inventory':len(allrows),'first_native_name_byte_candidates':351,'first_native_representatives':275,'additional_family_hints_not_selected_before':len(uncovered),'new_actual_name_relations':len(relations),'additional_native_representatives':len(reps),'additional_files_in_full_byte_groups':sum(len(r['byte_identical_members']) for r in reps),'relation_kind_counts':dict(Counter(r['kind'] for r in relations)),'uncovered85_selected_by_new_actual_relation':[r['stem'] for r in uncovered if r['stem'].lower() in names],'uncovered85_retained_no_new_actual_relation':[r['stem'] for r in uncovered if r['stem'].lower() not in names],'coverage_limit':'All3383 names/SHA were inventoried. Only actual name/byte relation candidates are submitted to native audit; unique functional packages are retained. This is not a claim all3383 full geometries were deduplicated.','relations':relations,'outputs':{str(pp):sha(pp)},'public_guard_manifest':plan['public_guard_manifest'],'public_guard_sha256':sha(plan['public_guard_manifest'])}
(O/'INCREMENTAL_ALIAS_REVIEW.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ('relations','uncovered85_retained_no_new_actual_relation')},indent=2))
