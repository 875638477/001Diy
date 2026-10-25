"""Prepare explicit, bounded A4 placements without modifying original CAD files."""
from pathlib import Path
from collections import defaultdict
import copy, json

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'examples/de_15_26_20261019'
OUT = ROOT / 'staging/a4_review_20261019'
OUT.mkdir(parents=True, exist_ok=True)
spec = copy.deepcopy(json.loads((BASE/'integrated_circuit.json').read_text(encoding='utf-8')))
groups = {
 'ADC_GPIO': ['J10','R32','C24','J11','J12','J13'],
 'RESET_BOOT': ['R27','C21','J7','R28','R29','R30','J8'],
 'CLOCK_DEBUG': ['J9','Y1','R31','C22','C23'],
 'UART_I2C': ['J4','R16','R17','R18','J5','R19','R20'],
 'SPI': ['J6','R21','R22','R23','R24','R25'],
 'MCU_CORE': ['U1'],
 'MCU_SUPPLY': ['C13','C14','C15','C16','C17','R26','C18','C19','C20'],
 'POWER_INPUT_LDO': ['J1','F1','D1','C1','C2','C3','U3','C8','C9'],
 'POWER_BUCK': ['U2','C4','L1','C5','C6','R1','R2','C7'],
 'USB_PORT': ['J2','R3','R4','U4','C10','R5','R6'],
 'USB_SENSE_ATTACH': ['R7','R8','Q1','R9','Q2','R10','R11'],
 'CAN': ['U5','C11','C12','R12','R13','R14','R15','J3'],
}
by_ref = {c['ref']:c for c in spec['components']}
assert sorted(r for refs in groups.values() for r in refs) == sorted(by_ref)
components = []
boxes = []
for page, refs in groups.items():
    cursor = [100,100]
    # Wide symbols occupy the left column; small parts balance column heights.
    ordered = sorted(refs, key=lambda r: -spec['models'][by_ref[r]['model']]['width'])
    for ref in ordered:
        c = by_ref[ref]
        model = spec['models'][c['model']]
        col = 0 if model['width'] > 80 else min(range(2), key=cursor.__getitem__)
        x, y = (240,860)[col], cursor[col]
        h = model['height']
        assert y+h+60 <= 782, (page, ref, x, y, h)
        c['properties']['SOURCE_MODULE_PAGE'] = c['page']
        c['page'] = page
        c['layout'] = [x,y]
        cursor[col] += h+100
        boxes.append(dict(page=page,name=ref,left=x-190,top=y-30,
                          right=x+model['width']+190,bottom=y+h+60))
        components.append(c)
spec['components'] = components
spec['pages'] = list(groups)
net_pages = defaultdict(set)
for c in components:
    for net in c['pins'].values():
        if net: net_pages[net].add(c['page'])
spec['cross_page_nets'] = {n:sorted(p) for n,p in net_pages.items() if len(p)>1}
spec['schematic_style'] = 'A4 landscape 297x210 mm; explicit 100 mil pin pitch; 12 functional pages'
(OUT/'a4_spec.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'layout_plan.json').write_text(json.dumps({'modules':boxes},indent=2),encoding='utf-8')

def tcl(v):
    if isinstance(v, dict): return '[dict create '+' '.join(tcl(str(k))+' '+tcl(w) for k,w in v.items())+']'
    if isinstance(v, list): return '[list '+' '.join(tcl(w) for w in v)+']'
    if v is None: return '{}'
    if isinstance(v,bool): return '1' if v else '0'
    if isinstance(v,(int,float)): return str(v)
    # Tcl double-quote escaping; no substitutions from sourced device data.
    return '"'+str(v).replace('\\','\\\\').replace('"','\\"').replace('$','\\$').replace('[','\\[').replace(']','\\]').replace('\n','\\n').replace('\r','\\r')+'"'
(OUT/'a4_spec.tcl').write_text('set ::DEspec '+tcl(spec)+'\n',encoding='utf-8')
print(json.dumps({'pages':len(groups),'components':len(components),'cross_page_nets':len(spec['cross_page_nets'])}))
