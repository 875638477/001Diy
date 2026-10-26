from pathlib import Path
from collections import Counter,defaultdict
import csv,hashlib,json
M=Path(r'D:\001DIY\005lib\01AIEDA\library_maintenance\20261025_pc_shared')
OUT=M/'global_suffix_reference_audit_v1'
base=Path(r'D:\001DIY\004computer\lga1700\cadence_library_cleanup_20261025\usage_audit')
info=json.loads((OUT/'PUBLIC_BRD_REFERENCE_AUDIT.json').read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
def tab(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter='\t',quoting=csv.QUOTE_NONE))
def unquote(v):
 if v=='nil':return None
 if v.startswith('"') and v.endswith('"'):return v[1:-1]
 return v
boards=[]
for b in info['public_boards']:
 job=base/'jobs'/b['native_snapshot_id'];pins=tab(job/'all_symbol_pins.tsv');vias=tab(job/'vias.tsv');comps=tab(job/'components.tsv')
 names={n['name'] for n in b['candidate_declared_packages']}|{n['name'] for n in b['candidate_placed_symbols']}
 cp=[p for p in pins if unquote(p['symbol_name']).lower() in names]
 perref=defaultdict(list)
 for p in cp:perref[unquote(p['refdes'])].append({k:unquote(p[k]) for k in ('symbol_name','number','padstack','net','x','y')})
 logical=[{'refdes':unquote(c['refdes']),'package':unquote(c['package']),'placed':c['placed']=='t','logical_pin_count':int(c['logical_pin_count'])} for c in comps if unquote(c['package']).lower() in names]
 b2={'source':b['source'],'source_sha256':b['sha256'],'native_snapshot_id':b['native_snapshot_id'],'all_physical_pin_count':len(pins),'all_named_net_pin_count':sum(unquote(p['net']) not in (None,'') for p in pins),'all_named_pin_net_names':len({unquote(p['net']) for p in pins if unquote(p['net']) not in (None,'')}),'native_via_objects_total':len(vias),'native_vias_with_named_net':sum(unquote(v['net']) not in (None,'') for v in vias),'candidate_logical_components':len(logical),'candidate_logical_placed':sum(c['placed'] for c in logical),'candidate_logical_unplaced':sum(not c['placed'] for c in logical),'candidate_physical_pins':len(cp),'candidate_physical_pins_named_net':sum(unquote(p['net']) not in (None,'') for p in cp),'candidate_physical_pins_nil_net':sum(unquote(p['net']) is None for p in cp),'candidate_physical_pins_empty_net':sum(unquote(p['net'])=='' for p in cp),'candidate_unique_named_nets':len({unquote(p['net']) for p in cp if unquote(p['net']) not in (None,'')}),'candidate_physical_pin_details_by_ref':dict(perref),'candidate_logical_components_details':logical,'source_table_hashes':{str(p):sha(p) for p in (job/'all_symbol_pins.tsv',job/'vias.tsv',job/'components.tsv')}}
 b2['classification']='ACTIVE_ELECTRICAL_BOARD_REQUIRE_CONNECTIVITY_PROOF' if b2['candidate_physical_pins_named_net'] or b2['native_vias_with_named_net'] else 'NO_CANDIDATE_PLACEMENT_IN_SNAPSHOT_LOGICAL_DEPENDENCIES_STILL_PRESENT'
 b2['etch_statistics']='NOT_EXPORTED_BY_EXISTING_USAGE_SNAPSHOT; no zero-route claim is made'
 boards.append(b2)
report={'status':'READONLY_SHA_BOUND_NATIVE_SNAPSHOT_SCOPE_ASSESSMENT','public_board_count':len(boards),'boards':boards,'rules':['Named net pin and branch-owned via evidence disproves all-NC palette assumptions.','No routed-etch-count information was exported in the existing snapshot; absence of an etch field is not proof of no route.','Unplaced candidates have no physical pad endpoints to reconnect, but their logical packages need redirection before external aliases disappear.','No CAD or file mutation performed.']}
(OUT/'PUBLIC_BRD_CONNECTION_SCOPE.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps([{k:b[k] for k in ('source','classification','candidate_logical_components','candidate_logical_placed','candidate_physical_pins','candidate_physical_pins_named_net','candidate_unique_named_nets','native_via_objects_total')} for b in boards],ensure_ascii=False,indent=2))
