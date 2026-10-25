"""Record the final project budget without changing native CAD or past evidence."""
from pathlib import Path
import json,hashlib,shutil
root=Path(__file__).resolve().parents[2];learning=root/'learning'
base=learning/'examples/de_15_26_20261019'
backup=root/'backups/before_DE_15_26_20261019'
if backup.exists():raise SystemExit('Existing backup preserved; do not replay this mutation')
backup.mkdir(parents=True)
for name in ('EDA.md','课程索引.md'):shutil.copy2(root/name,backup/name)
stage=learning/'staging/de_15_26_20261019/before_final_budget_metadata';stage.mkdir(parents=True,exist_ok=False)
power=json.loads((base/'power_interface_spec.json').read_text(encoding='utf-8'))
assert power['supply_limits']['V3V3_load_max_A']==.15 and power['supply_limits']['ambient_C']==[0,40]
sources={n:hashlib.sha256((base/n).read_bytes()).hexdigest() for n in ('mcu_spec.json','power_interface_spec.json')}
for name in ('integrated_circuit.json','integrated_circuit_eco.json'):
    path=base/name;shutil.copy2(path,stage/name)
    d=json.loads(path.read_text(encoding='utf-8'))
    d['source_hashes_at_native_construction']=d['source_hashes']
    d['source_hashes']=sources;d['constraints']=power['supply_limits']
    d['constraint_revision_note']='Normal150mA/Ta0..40C replaces initial120mA/0..50C after current and thermal review. This document-only project constraint revision does not change native pins, nets, components or values. Old L1 covers nominal120mA source description is preserved as construction history, not the final project current budget.'
    path.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
constraints=dict(date='2026-10-19 Asia/Shanghai',status='Teaching assumptions, not user product requirements or hardware signoff',
    MCU='STM32F103C8T6',normal_supply=power['supply_limits'],
    USB=dict(mode='self-powered Full-Speed device; mutually exclusive with CAN',VBUS='sense and ESD only; no board power/backfeed',bench_VBUS_min_V=4.75),
    CAN=dict(max_rate_bps=500000,max_bench_cable_m=1,bus_fault_outside_normal_budget=True),
    I2C=dict(default_rate_Hz=100000,conditional_max_Hz=400000,total_C_max_pF=100,baseline_R_ohm=2200,ECO_R_ohm=3300,note='RC budget does not validate maximum bus timing; same ST datasheet table/footnote inconsistency retained'),
    SPI=dict(rate_max_Hz=1000000,bench_length_max_m=.1),ADC=dict(input_V=[0,3.0],source_bandwidth_max_Hz=1,source_R_max_ohm=1000,rate_Hz=100),
    board=dict(outline_frozen=False,production_stackup_defined=False,actual_host_conductors=['TOP','BOTTOM'],unplaced=True),
    pending=['GUI ERC/Apply SWP','hardware clock/ADC/USB/CAN tests','thermal/power-off/reverse-current/stability tests','final passive/connector MPN and exact land certification','PCB outline/placement/routing/manufacturing signoff'])
(base/'project_constraints.json').write_text(json.dumps(constraints,ensure_ascii=False,indent=2),encoding='utf-8')
print('Backups and final150mA project constraints saved; native CAD unchanged')
