"""Freeze published12-to-Capture13 superset and exact PCB34 expected pads. No CAD/write to designs."""
from pathlib import Path
from collections import Counter,defaultdict
from decimal import Decimal,ROUND_HALF_UP
import copy,csv,hashlib,json
M=Path(__file__).resolve().parent
R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025')
O=M/'sot34_superset_pst_and_pins_v1';O.mkdir(exist_ok=True)
load=lambda p:json.loads(Path(p).read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def put(name,obj):
 p=O/name;p.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8');return p
basepath=R/'w/capture_native_frozen/CAPTURE13_FROZEN_PLAN.json'
addpath=M/'capture_sot34_plan_v1/compiled_v2/CAPTURE13_FROZEN_PLAN.json'
base=load(basepath);add=load(addpath)
assert sha(base['source_design_xml'])==base['source_xml_sha256']=='8481A465622DDB1B8C5BE020A7711291E0A06A80E42F1E6E137D8C95A49E32E2'
assert sha(add['source_design_xml'])==add['source_xml_sha256']=='9ED7877D0F942A42ECE44499F7C35F7483939B1494DC4D8193A4E945F27E444D'
assert len(base['pcb_footprint_changes'])==941 and len(add['pcb_footprint_changes'])==34
key=lambda x:(x['page'],x['id'])
assert not ({key(x) for x in base['pcb_footprint_changes']}&{key(x) for x in add['pcb_footprint_changes']})
sup=copy.deepcopy(base);sup['pcb_footprint_changes']+=copy.deepcopy(add['pcb_footprint_changes'])
sup['status']='FROZEN_PUBLISHED12_TO_CAPTURE13_975_FP_AND_PUBLIC_SOURCE_SUPERSET_FOR_INDEPENDENT_XML_PST_REVIEW_ONLY'
sup['scope']='Original941 explicit FP and same source identities, plus34 SOT23_123 to sot23-3 explicit FP. No additional design mutations authorized.'
sup['superset_binding']={'base_plan':str(basepath),'base_plan_sha256':sha(basepath),'additional_plan':str(addpath),'additional_plan_sha256':sha(addpath),'candidate_DSN':str(R/'w/sot34_cn2/LGA1700.DSN'),'candidate_DSN_sha256':sha(R/'w/sot34_cn2/LGA1700.DSN'),'candidate_XML':str(R/'w/sot34_xn2/native_design.xml'),'candidate_XML_sha256':sha(R/'w/sot34_xn2/native_design.xml'),'not_a_native_apply_plan':True}
sup['native_script']=None
sp=put('CAPTURE13_PUBLISHED12_SUPERSET_PLAN.json',sup)

prepath=M/'global_canonical_publish_v1/PROJECT13_SOT34_DELTA_PREFLIGHT.json';pre=load(prepath)
assert pre['source_board_sha256']==sha(pre['source_board'])=='49AF5EE7252CA9E8C4C48D8F60AD4D1113DA559814585356B14F6150A195C063'
oldpath=R/'w/pcb_migration/EXPECTED_BOARD_PINS_V3.json';old=load(oldpath)
tsv=R/'w/final_alt13/all_symbol_pins.tsv'
actual=list(csv.DictReader(tsv.open(encoding='utf-8'),delimiter='\t'))
def norm(d):
 v=Decimal(d);q=v.quantize(Decimal('0.01'),rounding=ROUND_HALF_UP)
 assert abs(v-q)<Decimal('0.00000001'),(d,'not board mils2 coordinate')
 return str(q.normalize())
def oldkey(x):
 return(x['ref'],x['pin'],norm(x['expected_x']),norm(x['expected_y']),x['net'],x['isMech'],x['isThrough'],x['new_padstack'])
def actualkey(x):
 return(x['refdes'],x['number'],norm(x['x']),norm(x['y']),x['net'],x['mechanical'],x['through'],x['padstack'])
# Keep actual native nil-vs-empty metadata from validated V3; TSV alone cannot replace this information.
assert len(old)==len(actual)==6521 and Counter(map(oldkey,old))==Counter(map(actualkey,actual))
rows={(x['ref'],p['number']):(x,p) for x in pre['rows'] for p in x['pins']}
assert len(rows)==102 and {x['ref'] for x in add['pcb_footprint_changes']}=={r for r,p in rows}
new=copy.deepcopy(old);changes=[]
for x in new:
 k=(x['ref'],x['pin'])
 if k not in rows:continue
 pose,p=rows[k]
 assert tuple(map(norm,[x['expected_x'],x['expected_y']]))==tuple(map(norm,p['source_world_mils']))
 assert x['net']==p['net'] and x['isMech']==x['isThrough']=='nil'
 before=copy.deepcopy(x)
 x['old_x'],x['old_y']=x['expected_x'],x['expected_y']
 x['old_padstack']=x['new_padstack']
 q=[str(Decimal(v).quantize(Decimal('0.01'),rounding=ROUND_HALF_UP)) for v in p['target_ideal_world_mils']]
 x['expected_x'],x['expected_y']=q;x['new_padstack']='PAD_36_47';x['target']='sot23-3'
 changes.append({'ref':x['ref'],'pin':x['pin'],'before':before,'after':copy.deepcopy(x),'ideal_world_mils':p['target_ideal_world_mils'],'expected_board_units':'mils','expected_board_accuracy':2,'quantization':'nearest0.01mil; no half-grid ties in102 coordinates','actual_readback_required':True})
assert len(changes)==102
# Prove unselected6419 raw row dictionaries survive byte-value semantics, including special/duplicate pins.
assert [x for x in old if (x['ref'],x['pin']) not in rows]==[x for x in new if (x['ref'],x['pin']) not in rows]
assert len({x['ref'] for x in new})==1066
jp=put('EXPECTED_BOARD_PINS_SOT34.json',new)
quote=lambda x:json.dumps(x,ensure_ascii=False)
byref=defaultdict(list)
for x in new:
 net='nil' if x['native_net_type']=='NIL' else quote(x['net'])
 byref[x['ref']].append('('+quote(x['pin'])+' ('+x['expected_x']+' '+x['expected_y']+') '+net+' '+x['isMech']+' '+x['isThrough']+' '+quote(x['new_padstack'])+')')
ip=O/'EXPECTED_PINS_SOT34.ilist'
ip.write_text('\n'.join('('+quote(ref)+' ('+' '.join(byref[ref])+'))' for ref in sorted(byref))+'\n',encoding='utf-8')
cp=put('SOT34_102_EXPECTED_CHANGES.json',changes)
report={'status':'FROZEN_SUPERSET975_AND_EXPECTED6521_PREPARED_NO_CAD','published12_FP_instances':941,'additional_FP_instances':34,'total_FP_instances':len(sup['pcb_footprint_changes']),'physical_FP_refs':len({x['ref'] for x in sup['pcb_footprint_changes']}),'source_cache_identity_entries':len(sup['object_mappings']),'source_instance_identity_entries':len(sup['instance_source_changes']),'expected_physical_pads':len(new),'expected_physical_components':len(byref),'changed_expected_pad_records':len(changes),'unchanged_expected_pad_records':len(new)-len(changes),'source_board':pre['source_board'],'source_board_sha256':pre['source_board_sha256'],'source_snapshot':str(tsv),'source_snapshot_sha256':sha(tsv),'source_expected_ledger':str(oldpath),'source_expected_ledger_sha256':sha(oldpath),'actual_all6521_matches_validated_V3':True,'source_SC37_pad_coordinates_preserved':True,'source_pads_net_nil_empty_string_type_preserved':True,'limits':'New pad world positions are exact expected mils2 quantization of native public definition at unchanged poses; root must run actual native readback/GetConnect gate. This is not connection approval.','outputs':{str(p):sha(p) for p in (sp,jp,ip,cp)}}
rp=put('PREPARATION_REPORT.json',report);print(json.dumps(report,indent=2))
