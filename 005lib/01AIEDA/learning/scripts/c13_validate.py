"""Independent acceptance of native readback, using source pin table and graph rules."""
from pathlib import Path
import csv, json, hashlib

root=Path(__file__).resolve().parents[1]
logs=root/'logs/capture_C_20261019'
def rows(name):
    with (logs/name).open(encoding='utf-8-sig',newline='') as f:
        return list(csv.DictReader(f,delimiter='\t'))
multi=rows('c13_hc00_pins.tsv')
occ=rows('c13_flat_occurrences_v8.tsv')
wires=rows('c13_flat_wires_v8.tsv')
pins=rows('c13_flat_pins_v8.tsv')
fullrefs=rows('c13_fullrefs_v8.tsv')
checks=[]
def check(name,condition,evidence):
    checks.append(dict(name=name,passed=bool(condition),evidence=evidence))
def ids(records): return {r['flat_id'] for r in records}
expected={'A':{'A':'1','B':'2','Y':'3','GND':'7','VCC':'14'},
          'B':{'A':'4','B':'5','Y':'6','GND':'7','VCC':'14'},
          'C':{'A':'9','B':'10','Y':'8','GND':'7','VCC':'14'},
          'D':{'A':'12','B':'13','Y':'11','GND':'7','VCC':'14'}}
actual={d:{r['name']:r['physical_number'] for r in multi if r['device']==d} for d in expected}
check('TI_14pin_four_unit_mapping',actual==expected,actual)
physical={r['physical_number'] for r in multi}
check('four_units_cover_14_unique_physical_terminals',physical=={str(i) for i in range(1,15)},sorted(physical,key=int))
unitrefs=[r for r in fullrefs if r['page']=='TOP1']
check('four_units_share_base_U1_and_have_exact_full_designators',len(unitrefs)==4 and {r['raw_reference'] for r in unitrefs}=={'U1'} and {r['full_reference'] for r in unitrefs}=={'U1A','U1B','U1C','U1D'} and {r['device'] for r in unitrefs}=={'A','B','C','D'},unitrefs)
check('installed_library_has_no_authorized_pin_swap_groups',all(r['swap_id']=='-1' for r in multi),sorted({r['swap_id'] for r in multi}))
same1=[r for r in wires if r['page']=='TOP1' and r['aliases']=='SAME_PAGE']
same2=[r for r in wires if r['page']=='TOP2' and r['aliases']=='SAME_PAGE']
check('same_page_aliases_join',len(same1)==2 and len(ids(same1))==1,same1)
check('same_alias_text_across_pages_stays_separate',len(same2)==1 and ids(same1).isdisjoint(ids(same2)),same2)
cross=[r for r in wires if r['name']=='CROSS_PAGE']
check('off_page_connectors_join_TOP1_and_TOP2',len(ids(cross))==1 and {r['page'] for r in cross}=={'TOP1','TOP2'},cross)
localA=[r for r in occ if r['occ_path']=='HA/LOCAL']
localB=[r for r in occ if r['occ_path']=='HB/LOCAL']
check('hierarchy_local_aliases_remain_separate',len(localA)==len(localB)==1 and ids(localA).isdisjoint(ids(localB)),localA+localB)
for block in ['HA','HB']:
    parent=[r for r in occ if r['occ_path']==f'PARENT_SIG_{block}']
    child=[r for r in occ if r['occ_path']==f'{block}/H_SIG']
    check(f'hierarchical_port_binds_{block}',len(parent)==len(child)==1 and ids(parent)==ids(child),parent+child)
vcc=[r for r in occ if r['name']=='VCC']
vcc_pins=[r for r in pins if r['name']=='VCC' and r['reference'].startswith('U1')]
check('global_VCC_crosses_root_and_children',len(ids(vcc))==1 and {r['occ_path'] for r in vcc}=={'VCC','HA/VCC','HB/VCC'} and all(r['global']=='1' for r in vcc),vcc)
check('hidden_HC00_VCC14_is_global',len(vcc_pins)==4 and all(r['pin_number']=='14' and r['visible']=='0' and r['raw_global']=='1' for r in vcc_pins),vcc_pins)
gnd=[r for r in pins if r['pin_name']=='GND' and r['reference'].startswith('U1')]
check('hidden_HC00_GND7_shared_by_four_units',len(gnd)==4 and len(ids(gnd))==1 and all(r['pin_number']=='7' and r['visible']=='0' for r in gnd),gnd)
power=[r for r in pins if r['pin_name']=='VDDa']
check('visible_wired_POWER_is_local_despite_raw_global_bit',len(power)==2 and len(ids(power))==2 and all(r['pin_number']=='2' and r['type']=='7' and r['visible']=='1' and r['raw_global']=='1' for r in power) and {r['name'] for r in power}=={'LOCAL_PWR_A','LOCAL_PWR_B'} and all(r['global']=='0' for r in occ if r['flat_id'] in ids(power)),power)
data0=[r for r in occ if r['name']=='DATA0'];data1=[r for r in occ if r['name']=='DATA1']
bus=[r for r in wires if 'DATA[0..1]' in r['aliases']]
check('bus_members_are_two_distinct_nets',len(data0)==len(data1)==1 and ids(data0).isdisjoint(ids(data1)) and ids(bus)==ids(data0+data1),dict(data0=data0,data1=data1,bus=bus))
nand=[r for r in pins if r['name'] in ['NAND_IN_A','NAND_IN_B','NAND_OUT_A']]
check('connected_gate_uses_physical_pins_1_2_3',{r['name']:(r['pin_number'],r['type']) for r in nand}=={'NAND_IN_A':('1','0'),'NAND_IN_B':('2','0'),'NAND_OUT_A':('3','2')},nand)
native=root/'examples/lesson13_capture/c13_scope_v8.dsn'
check('native_DSN_compound_file_header',native.read_bytes()[:8]==bytes.fromhex('D0CF11E0A1B11AE1'),str(native))
result=dict(lesson=13,date='2026-10-19',scope='Capture 17.2 native database SDK; GUI not claimed',counts=dict(checks=len(checks),passed=sum(c['passed'] for c in checks),occurrences=len(occ),wire_memberships=len(wires),pin_memberships=len(pins)),checks=checks,dsn_sha256=hashlib.sha256(native.read_bytes()).hexdigest())
(logs/'c13_acceptance.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result['counts']))
raise SystemExit(0 if all(c['passed'] for c in checks) else 1)
