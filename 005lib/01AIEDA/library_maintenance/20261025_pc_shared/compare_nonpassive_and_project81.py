"""Offline complete native graphs, full PAD XML and actual project package review. No CAD."""
from pathlib import Path
from collections import defaultdict,Counter
from decimal import Decimal
import csv,json,hashlib,importlib.util,re
M=Path(__file__).resolve().parent;R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025');O=M/'global_nonpassive_comparison13';O.mkdir(exist_ok=True)
S=importlib.util.spec_from_file_location('native_reader',M/'review_global_suffix_native_chunks.py');N=importlib.util.module_from_spec(S);S.loader.exec_module(N)
jr=N.jread;sha=N.sha;dump=N.dump
sets=['global_suffix_native_review_v3','global_nonpassive_native_review13','global_nonpassive_increment_review13','global_canonical_targets_review13']
index={};padxml={};bysha={};all_native=[]
for folder in sets:
 d=M/folder
 binding=jr(d/'FULL_PAD_XML_BINDING.json');assert not binding['errors']
 for p in binding['records']:
  key=p['path'].lower()
  if key in padxml:assert padxml[key]['current_sha256']==p['current_sha256']
  padxml[key]=p
 for f in sorted(d.glob('e[0-9]*_SCHEMA_GEOMETRY.json')):
  for e in jr(f):
   all_native.append(e);index[e['stem'].lower()]=e;bysha[e['source_sha256']]=e
   for n in e.get('byte_identical_members',[]):index[Path(n).stem.lower()]=e
# Earlier941 schemas did not carry bytealiases, but every one was fullSHA unique.
allrows=jr(M/'global_nonpassive_inventory_v1/ALL_PUBLIC_PSM_INVENTORY.json')['files']
for r in allrows:
 if r['sha256'] in bysha:index[r['stem'].lower()]=bysha[r['sha256']]
closurepath=R/'w/pcb_migration/SOURCE_ACTUAL_CACHE_PAD_GEOMETRY_CLOSURE.json';finalclosurepath=R/'w/pcb_migration/FINAL_ALT_PUBLIC_CACHE_REVIEW.json'
closure=jr(closurepath);finalclosure=jr(finalclosurepath)
assert closure['status']=='PASS_ORIGINAL_PCB93_CACHED_PAD_GEOMETRY_CLOSURE'
assert finalclosure['status']=='PASS_PUBLIC_COMPATIBILITY_WITH_EXPLICIT_INHERITED_BOUND_METADATA'
for path,h in closure['proofs'].items():assert sha(path)==h
padbyname=defaultdict(list)
for p in padxml.values():padbyname[Path(p['path']).stem.lower()].append(p)
def padrecord(e,p):
 deps=[d for d in e['actual_loaded_pad_files'] if Path(d['path']).stem.lower()==p['pad_name'].lower()]
 if len(deps)!=1:
  if e.get('project_pad_closure_binding'):
   possible=padbyname[p['pad_name'].lower()]
   if len(possible)==1:return possible[0]
  return None
 r=padxml.get(deps[0]['path'].lower())
 return r if r and r['current_sha256']==deps[0]['sha256'] else None
def core(e):
 result=[]
 for p in e['pins']:
  r=padrecord(e,p)
  if r is None:return None
  rot=p['local_rotation'];rot=str(Decimal(rot['number']).normalize()) if isinstance(rot,dict) and 'number' in rot else rot
  result.append({'number':p['number'],'xy_mm':[str(Decimal(v).normalize()) for v in p['local_xy_mm']],'rotation':rot,'mirror':p['mirror_type'],'mechanical':p['is_mechanical'],'through':p['is_through'],'full_PAD_manufacturing_signature':r['all_classified_manufacturing_fields_signature']})
 return result
def rigid(a,b):
 if a['duplicate_pin_numbers'] or b['duplicate_pin_numbers'] or Counter(a['pin_numbers'])!=Counter(b['pin_numbers']):return []
 ap={p['number']:tuple(map(Decimal,p['local_xy_mm'])) for p in a['pins']};bp={p['number']:tuple(map(Decimal,p['local_xy_mm'])) for p in b['pins']}
 if not ap:return []
 first=next(iter(ap));solutions=[]
 for mat in [((1,0),(0,1)),((0,-1),(1,0)),((-1,0),(0,-1)),((0,1),(-1,0)),((-1,0),(0,1)),((1,0),(0,-1)),((0,1),(1,0)),((0,-1),(-1,0))]:
  rot=lambda p:(mat[0][0]*p[0]+mat[0][1]*p[1],mat[1][0]*p[0]+mat[1][1]*p[1])
  q=rot(ap[first]);delta=(bp[first][0]-q[0],bp[first][1]-q[1]);errors=[]
  for n,p in ap.items():
   r=rot(p);errors.extend([abs(r[0]+delta[0]-bp[n][0]),abs(r[1]+delta[1]-bp[n][1])])
  if max(errors,default=0)<=Decimal('0.000000001'):solutions.append({'D4_matrix':mat,'translation_source_to_target_mm':list(map(str,delta)),'max_error_mm':str(max(errors,default=0))})
 return solutions
def compare(a,b):
 ca,cb=core(a),core(b);schema=lambda e:Counter((p['number'],p['is_mechanical'],p['is_through']) for p in e['pins'])
 same_schema=schema(a)==schema(b)
 return {'source_stem':a['stem'],'target_stem':b['stem'],'source_native':a['native_path'],'source_native_sha256':a['native_sha256'],'target_native':b['native_path'],'target_native_sha256':b['native_sha256'],'source_pin_count':a['pin_count'],'target_pin_count':b['pin_count'],'source_pin_numbers':a['pin_numbers'],'target_pin_numbers':b['pin_numbers'],'same_numbered_pin_schema':same_schema,'same_full_ordered_native_graph':a['full_ordered_graph_fingerprint']==b['full_ordered_graph_fingerprint'],'same_current_source_bytes':a['source_sha256']==b['source_sha256'],'full_PAD_XML_available':ca is not None and cb is not None,'same_exact_numbered_pin_local_xy_orientation_and_full_PAD_XML':ca==cb if ca is not None and cb is not None else False,'numbered_pin_centers_D4_rigid_solutions':rigid(a,b),'source_pin_summary':N.pin_summary(a),'target_pin_summary':N.pin_summary(b)}
relations=jr(M/'global_nonpassive_inventory_v1/NAME_CANDIDATE_RELATIONS.json')['relations'];pairs=[]
for row in relations:
 for b in row['possible_bases']:pairs.append((row['candidate'].lower(),b.lower(),row['kind']))
for row in jr(M/'global_nonpassive_increment_v1/INCREMENTAL_ALIAS_REVIEW.json')['relations']:pairs.append((row['candidate'],row['possible_base'],row['kind']))
comparisons=[]
for a,b,k in sorted(set(pairs)):
 x={'candidate':a,'possible_base':b,'name_relation':k}
 if a not in index or b not in index:x['gate']='MISSING_OR_FAILED_NATIVE_PRESERVE';x['missing_native']=[n for n in (a,b) if n not in index]
 else:
  x.update(compare(index[a],index[b]))
  if not x['same_numbered_pin_schema']:x['gate']='FUNCTIONAL_NUMBERED_PIN_SCHEMA_DIFFERENCE_PRESERVE'
  elif x['same_exact_numbered_pin_local_xy_orientation_and_full_PAD_XML']:x['gate']='FULL_NUMBERED_PAD_MANUFACTURING_EQUIVALENT_GRAPHICS_DIFFERENCES_RECORDED'
  else:x['gate']='PHYSICAL_DIFFERENCE_REQUIRES_SPECIFIC_STANDARDIZATION_PLAN_OR_PRESERVE'
 comparisons.append(x)
dump(O/'CANDIDATE_PAIR_FULL_NATIVE_COMPARISON.json',comparisons)
# Whole byte-duplicate classes are independently actual-native verified; no text/header stripping.
bytegroups=[]
for group in jr(M/'global_nonpassive_inventory_v1/NAME_CANDIDATE_RELATIONS.json')['exact_byte_groups']:
 members=group.get('members',group.get('paths',[])) if isinstance(group,dict) else group
 if not members:
  # Preserve source schema for future readers; unrecognized does not mean no groups.
  bytegroups.append({'source_group':group,'status':'UNRECOGNIZED_GROUP_SCHEMA_PRESERVE'});continue
 stems=[Path(x['path'] if isinstance(x,dict) else x).stem.lower() for x in members];available=[s for s in stems if s in index]
 e=index[available[0]] if available else None
 bytegroups.append({'members':stems,'current_byte_sha256':group.get('sha256') if isinstance(group,dict) else None,'actual_native_available':e is not None,'native_path':e['native_path'] if e else None,'full_PAD_XML_available':core(e) is not None if e else False,'pin_count':e['pin_count'] if e else None,'pin_numbers':e['pin_numbers'] if e else None,'status':'ACTUAL_COMPLETE_NATIVE_FULL_PAD_BYTE_DUPLICATE_GROUP' if e is not None and core(e) is not None else 'NATIVE_OR_PAD_MISSING_PRESERVE'})
dump(O/'WHOLE_BYTE_GROUP_NATIVE_REVIEW.json',bytegroups)
# Actual81 cached definitions from source board, not merely filename heuristics.
symrows=list(csv.DictReader((R/'w/final_alt13/symbols.tsv').open(encoding='utf-8'),delimiter='\t'))
refs=defaultdict(list)
for x in symrows:
 name=x.get('symbol_name',x.get('name','')).lower();ref=x.get('refdes',x.get('ref',''));refs[name].append(ref)
defrows=list(csv.DictReader((R/'w/final_alt13/manifest.tsv').open(encoding='utf-8'),delimiter='\t'));project=[]
for d in defrows:
 name=d['name'].lower();cached=N.inspect(Path(d['file']));cached.update(stem=d['name'],source_sha256=sha(Path(d['file'])),source=str(d['file']),project_pad_closure_binding=True)
 candidates={b if a==name else a for a,b,k in pairs if a==name or b==name}
 # Include structural comparison with existing genericSOT even when long-model naming eluded relation grammar.
 if 'sot23' in re.sub('[^a-z0-9]','',name) or name.startswith('ot-23-3'):candidates.add('sot23-3')
 if name.startswith('so8_50_150gv'):candidates|={'so8_50_150gv','so8_50_150gv_2','sop-8-150mil'}
 if re.fullmatch(r'[crlfb]+\d{4}.*_pc',name):candidates={name}
 row={'source_cached_name':d['name'],'actual_project_refdes':refs.get(name,[]),'actual_project_ref_count':len(refs.get(name,[])),'cached_pin_count':cached['pin_count'],'cached_pin_numbers':cached['pin_numbers'],'candidate_comparisons':[],'default_decision':'KEEP_UNIQUE_FUNCTIONAL_PACKAGE_UNLESS_ACTUAL_CANDIDATE_GATE_PASSES'}
 for target in sorted(candidates):
  if target==name and target not in index:continue
  if target not in index:row['candidate_comparisons'].append({'target':target,'gate':'NATIVE_FAILED_OR_NOT_AUDITED_PRESERVE'});continue
  comp=compare(cached,index[target]);comp['target']=target
  if not comp['same_numbered_pin_schema']:comp['gate']='FUNCTIONAL_NUMBERED_PIN_SCHEMA_DIFFERENCE_CANNOT_MERGE'
  elif comp['same_exact_numbered_pin_local_xy_orientation_and_full_PAD_XML']:comp['gate']='EXACT_PAD_SCHEMA_MATCH_MERGE_CANDIDATE'
  else:comp['gate']='SAME_NUMBERED_SCHEMA_PHYSICAL_DELTA_REQUIRES_PER_REF_PLAN'
  row['candidate_comparisons'].append(comp)
 project.append(row)
dump(O/'PROJECT81_ACTUAL_CACHED_PACKAGE_CANDIDATES.json',project)
summary={'status':'READONLY_NATIVE_AND_FULL_PAD_CANDIDATE_REVIEW_NOT_FINAL_RETIREMENT_APPROVAL','all_public_name_SHA_inventory':len(allrows),'candidate_pair_count':len(comparisons),'pair_gate_counts':dict(Counter(x['gate'] for x in comparisons)),'whole_byte_duplicate_groups':len(bytegroups),'byte_group_gate_counts':dict(Counter(x['status'] for x in bytegroups)),'project_cached_definitions':len(project),'project_actual_placed_components':sum(x['actual_project_ref_count'] for x in project),'project_candidate_package_count':sum(bool(x['candidate_comparisons']) for x in project),'unique_current_loaded_PAD_XML':len(padxml),'native_failed_preserved':['sot-23','smb'],'project_embedded_PAD_manufacturing_closure':{str(p):sha(p) for p in (closurepath,finalclosurepath)},'limits':['Fullgraph comparison keeps shape/text/font/order and fullPADXML; physical-equivalence comparison deliberately records graphics differences and never overrides a different numbered pin schema.','Project embedded PAD manufacturing identity inherits the exact source-cache/internal18-layer/native fullPADXML closure and final49AF cache gate. Missing PLACE_BOUND of68 inherited definitions remains explicitly distinct from PAD physical identity.','D4 pin-center fit is a pose hint, not complete copper/pad orientation equivalence or GetConnect proof.','Current project cached data binds board49AF5E...; root final copper/pad readback is required for any later candidate.'],'outputs':{str(p):sha(p) for p in O.glob('*.json') if p.name!='NATIVE_COMPARISON_SUMMARY.json'}}
dump(O/'NATIVE_COMPARISON_SUMMARY.json',summary);print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__!='__main__':raise RuntimeError('Do not import execution script')
