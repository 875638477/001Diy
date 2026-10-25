"""Export current values plus procurement specifications; never update CAD here."""
from pathlib import Path
import csv,json
base=Path(__file__).resolve().parents[1]/'examples/de_15_26_20261019'
for filename,outname in [('integrated_circuit.json','BOM_baseline.csv'),('integrated_circuit_eco.json','BOM_eco.csv')]:
    spec=json.loads((base/filename).read_text(encoding='utf-8'))
    columns=['Reference','Module_ID','Value','Specification','MPN','Procurement_Status','Footprint','Assembly','Page','Requirements']
    with (base/outname).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=columns);w.writeheader()
        for c in spec['components']:
            p=c['properties'];desc=p.get('source_description','')
            if desc==c['value']:
                pass
            elif desc:
                words=desc.split(maxsplit=1);desc=c['value']+(' '+words[1] if len(words)>1 else '')
            elif c['model'].startswith('RES'):desc=c['value']+' +/-1% unless explicit tighter source requirement'
            elif c['model'].startswith('CAP'):
                desc=c['value']+(' C0G +/-5% >=10V' if c['value'].endswith('pF') else ' X7R +/-20% >=10V; effective value and bias review required')
            else:desc=c['value']
            w.writerow(dict(Reference=c['ref'],Module_ID=c['id'],Value=c['value'],Specification=desc,MPN=c['mpn'],Procurement_Status=p['MPN_STATUS'],Footprint=spec['models'][c['model']]['footprint'],Assembly=c['populate'],Page=c['page'],Requirements=p.get('REQUIREMENTS','')))
print('BOM baseline/ECO export includes specifications, assembly and procurement status')
