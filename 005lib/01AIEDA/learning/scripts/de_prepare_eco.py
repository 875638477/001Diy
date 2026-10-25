from pathlib import Path
import csv,json,copy
base=Path(__file__).resolve().parents[1]/'examples/de_15_26_20261019'
original=json.loads((base/'integrated_circuit.json').read_text(encoding='utf-8'))
eco=copy.deepcopy(original)
for c in eco['components']:
    if c['ref'] in ('R19','R20'):
        c['value']='3.3k'
        c['properties']['source_description']='3.3k 1%'
    if c['ref']=='J13':c['pins']['7'],c['pins']['8']=c['pins']['8'],c['pins']['7']
eco['schema']='DE_integrated_circuit_ECO1'
eco['expected_ECO_changes']={'values':{'R19':['2.2k','3.3k'],'R20':['2.2k','3.3k']},'pins':{'J13.7':['GPIO_PB8','GPIO_PB9'],'J13.8':['GPIO_PB9','GPIO_PB8']},'i2c_rise_time_100pF_ns':0.8473*3300*1e-10*1e9,'i2c_rise_time_1pct_resistor_ns':0.8473*3333*1e-10*1e9}
(base/'integrated_circuit_eco.json').write_text(json.dumps(eco,ensure_ascii=False,indent=2),encoding='utf-8')
rows=list(csv.DictReader((base/'BOM_baseline.csv').open(encoding='utf-8-sig',newline='')))
for row in rows:
    if row['Reference'] in ('R19','R20'):row['Value']='3.3k'
with (base/'BOM_eco.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print(json.dumps(eco['expected_ECO_changes']))
