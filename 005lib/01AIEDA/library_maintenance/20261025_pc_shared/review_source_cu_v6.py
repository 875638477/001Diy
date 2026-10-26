"""Offline evidence review of the narrowly bounded source-Cu native restore.
Does not substitute for the subsequent fresh full-board connectivity/CFX gate.
"""
from pathlib import Path
from decimal import Decimal as D
import csv, collections, hashlib, json

R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025')
M=Path(__file__).parent
N=R/'w/all81_sourcecu11';C=R/'w/all81_cross10'
OUT=R/'w/pcb_migration/SOURCE_CU_V6_NATIVE_EVIDENCE_REVIEW.json'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def js(p): return json.loads(p.read_text(encoding='utf-8-sig'),parse_float=D)
def jsonl(p): return [json.loads(x,parse_float=D) for x in p.read_text(encoding='utf-8-sig').splitlines() if x]
def stable(x): return json.dumps(x,sort_keys=True,default=str,separators=(',',':'))
def require(p,text): assert text in p.read_text(encoding='utf-8-sig'),(p,text)
launch=js(N/'launch_report.json')
assert launch['exit_code']==0 and launch['write_candidate'] and launch['input_unchanged']
assert launch['source_sha256_before']==launch['source_sha256_after']==sha(Path(launch['source']))=='06B8DD73EE20A4C01A0BF36E0BF6CD0FDDFE20CE2F89DA430A2C003414BE9405'
assert launch['compare_source_sha256_before']==launch['compare_source_sha256_after']==sha(Path(launch['compare_source']))=='A9651E39CBD8DAC0B67566686AF3D2CA38B2AA517C5C1ADCD74E81336D563F51'
assert launch['script_sha256']==sha(Path(launch['script']))=='C2C5B3673F8F20E93D3E6A9819D8FC7DA18912A2F910A0876FECFDDF7296EC27'
dep=R/'w/pcb_migration/all81_source_cu_v5/all81_restore_actual_source_cu_v5.il'
assert sha(dep)=='792A34D71ECD8E994EFB843750CF2CCFDBAF91278054285B45111B6784B1FD4D'
board=N/'ALL81_SOURCE_CU_RESTORED.brd';assert board.exists()
require(N/'SOURCE_CU_V6_COMPLETE.txt','SOURCE6521_TYPED_PINS_AND1066_POSE_TEXT_PROPS_UNCHANGED')
require(N/'SOURCE_CU_RESTORE_COMPLETE.txt','EXACT_ORIGINAL_CU_RESTORED_AS_BOARD_OWNED_SHAPES=7')
require(N/'SOURCE_CU_RESTORE_COMPLETE.txt','ORIGINAL_DRC=t')
require(N/'SOURCE_CU_RESTORE_COMPLETE.txt','ORIGINAL_FILL=wysiwyg')
stdout=(N/'stdout.txt').read_text(encoding='utf-8-sig')
assert '*Error*' not in stdout and 'Parser WARNING' not in stdout
source=jsonl(N/'SOURCE_REAL_CU_POLYGONS.jsonl')
assert len(source)==431
roles=collections.Counter(x['side'] for x in source)
assert roles=={'REAL_SOURCE_ROUTE_SEGMENT':424,'EXACT_SOURCE_SYMBOL_ETCH_BRIDGE':7}
with (N/'SOURCE_CU_RESTORE_PREFLIGHT.tsv').open(newline='') as f: rows=list(csv.DictReader(f,delimiter='\t'))
assert len(rows)==431 and len({x['key'] for x in rows})==431
assert {x['key'] for x in rows}=={x['key'] for x in source}
assert all(int(x['other_net_intersections'])==0 for x in rows)
missing=[x for x in rows if int(x['missing_count'])]
assert len(missing)==7 and all(x['key'].startswith('SOURCE_SYMBOL_ETCH_U5.') for x in missing)
recreated=(N/'SOURCE_CU_RESTORED_OBJECTS.tsv').read_text().splitlines()
assert len(recreated)==7 and all(x.endswith('SOURCE_CU_EXACT_BOTH_DIRECTIONS') for x in recreated)
material=jsonl(N/'SOURCE_CU_MISSING_AND_CROSS.jsonl')
assert all(x['side']=='SOURCE_CU_ABSENT_FROM_TARGET_SAME_NET' for x in material)
assert len(material)==sum(int(x['missing_count']) for x in missing)
material_by_key=collections.defaultdict(list)
for x in material: material_by_key[x['key']].append(x['poly'])
for key,values in material_by_key.items():
 assert all(p['area']>0 and not p['holes'] for p in values)
assert set(material_by_key)=={x['key'] for x in missing}
vias=(N/'SOURCE_ALL4541_VIAS_TYPED.ilist').read_text().splitlines()
assert len(vias)==4541
for name in ('TARGET_ALL4541_VIAS_TYPED.ilist','RESTORED_ALL4541_VIAS_TYPED.ilist'):
 assert collections.Counter(vias)==collections.Counter((N/name).read_text().splitlines())
route=(N/'ROUTE_TAG_REPAIR.tsv').read_text().splitlines()
assert route==[
 'USB_SOURCE3_TARGET15_TOTAL_CU_ANDNOT_BOTH_DIRECTIONS_EMPTY',
 'USB_PATH_ORIGINAL_NET_RESTORED\tUSB_FRONT__USB3_RXP4__AD17\t1\tCUPOLY_EXACT',
 'USB_PATH_ORIGINAL_NET_RESTORED\tUSB3_RXP4\t10\tCUPOLY_EXACT',
 'USB_PATH_ORIGINAL_NET_RESTORED\tUSB3_RXP4\t6\tCUPOLY_EXACT',
 'VDD_SOURCE_NET_ANCHOR_PHYSICAL_ADDED_CU_ZERO',
 'SOURCE_USB_PREEXISTING_ALIAS_CONTACT_RETAINED_NOT_NEW_SHORT',
 'ALL6521_TYPED_PINS_UNCHANGED']
routepoly=jsonl(N/'ROUTE_TAG_PHYSICAL_CU.jsonl')
old=[x['poly'] for x in routepoly if x['side']=='SOURCE_FULL_PHYSICAL_CU']
new=[x['poly'] for x in routepoly if x['side']=='RESTORED_ORIGINAL_FULL_PATH_CU']
assert len(old)==len(new)==3 and collections.Counter(map(stable,old))==collections.Counter(map(stable,new))
merged=[x['poly'] for x in routepoly if x['side']=='TARGET_BEFORE_PHYSICAL_CU'];assert len(merged)==1
cross_launch=js(C/'launch_report.json');assert cross_launch['exit_code']==0 and not cross_launch['write_candidate'] and cross_launch['input_unchanged']
require(C/'CROSS_DIAGNOSTIC_COMPLETE.txt','TARGET_INTERSECTING_OTHER_NET_OBJECTS=2')
preexisting=jsonl(C/'SOURCE_OTHER_NET_INTERSECTIONS.jsonl')
assert len(preexisting)==2 and all('SOURCE_ALREADY_INTERSECTS_NET_"USB3_RXP4"_KIND_path'==x['side'] for x in preexisting)
overlap=sum((x['poly']['area'] for x in preexisting),D(0))
assert sum((p['area'] for p in old),D(0))-merged[0]['area']==overlap
proofs=[p for p in N.iterdir() if p.is_file() and p.suffix.lower() in ('.json','.jsonl','.ilist','.tsv','.txt','.scr')]
report={
 'status':'PASS_BOUNDED_NATIVE_SOURCE_CU_ROUTE_TAG_AND_VIA_RESTORE_EVIDENCE_NOT_FINAL_BOARD_GATE',
 'candidate_board':str(board),'candidate_sha256':sha(board),
 'source_board_sha256':launch['source_sha256_before'],'input_candidate_sha256':launch['compare_source_sha256_before'],
 'source_objects_native_detached_exact':431,'source_route_segments':424,'source_symbol_etch_bridges':7,
 'route_restore':{'original_usb_paths':3,'merged_target_segments':15,'original_usb_segments':[1,10,6],
 'all_three_recreated_polygon_records_exact':True,'native_full_union_ANDNOT_both_directions_empty':True,
 'vdd_existing_source_route_cu_anchor_physical_added_area':0,
 'source_preexisting_usb_alias_contacts':preexisting,'overlap_area_mil2':str(overlap),
 'scope':'Preserves pre-existing contact between two differently named USB routes; no claim that this original alias/short is repaired.'},
 'restored_old_symbol_cu_objects':7,'source_missing_fragments':len(material),
 'restored_missing_cu_area_mil2':str(sum((x['poly']['area'] for x in material),D(0))),
 'per_source_object_missing':{key:{'fragments':len(ps),'area_mil2':str(sum((p['area'] for p in ps),D(0))),'bounds':[p['bbox'] for p in ps]} for key,ps in material_by_key.items()},
 'all_original4541_vias_xy_pad_typed_net_properties_exact_after_two_frozen_net_repairs':True,
 'all6521_typed_pins_and1066_pose_text_compdefprops_strict':True,'drc':'t','fill':'wysiwyg',
 'limitations':['Fresh complete6521 typed/2020 physical partitions/1118 netstatus and fullCFX must be reviewed separately.',
 'This proves the431 frozen old-route/source-symbol-Cu objects and exact3path repair, not a total-board copper-union comparison.',
 'New standard pad copper geometry is governed by the separately frozen246-center/all84 package ledger.'],
 'evidence_sha256':{str(p):sha(p) for p in proofs},'loaded_v5_dependency_sha256':sha(dep)}
assert not OUT.exists();OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2,default=str),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ('evidence_sha256','per_source_object_missing','route_restore')},indent=2))
print('REPORT',OUT,'SHA256',sha(OUT))
