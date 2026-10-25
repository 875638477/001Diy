from pathlib import Path
import json,sys
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');sys.path.insert(0,str(R/'scripts'));from routing_geometry import load
for v in ['2L','4L']:
 d=load(R/'plans'/('ordinary_policy_'+v+'_v2.json'))
 old=load(R/'engineering_mcu/plans/gpio_north_escape_v3.json')['operations'];oldids={o['id'] for o in old}
 d['pendingOperations']=[o for o in d['pendingOperations'] if o['id'] not in oldids]
 d['pendingOperations']+=load(R/'engineering_mcu/plans/gpio_north_escape_v6.json')['operations']
 d['pendingOperations']+=load(R/'plans/SPI_NSS_explicit_v3b.json')['operations']
 d['manualOnlyNets'].append('PA4_SPI_NSS')
 # A direct underlying ground band is required for SCK along the analogue power row.
 d['reservedAreas'].append({'id':'NO_SPI_BOTTOM_IN_PREFILTER_TOP_REFERENCE_VOID','polygon':[[21.2,31.65],[29.0,31.65],[29.0,33.05],[21.2,33.05]],'layers':['BOTTOM'],'allowedNets':['GND','V3V3'],'basis':'Prevents unreviewed parallel SPI line under the existing TOP prefilter power opening; narrow route above requires actual postfill assessment.'})
 d['status']='ORDINARY_POLICY_V3_EXPLICIT_NSS_AND_GPIO6'
 (R/'plans'/('ordinary_policy_'+v+'_v3.json')).write_text(json.dumps(d,indent=2),encoding='utf8')
p=R/'scripts/routing_geometry.py';s=p.read_text(encoding='utf8');s=s.replace("key=('via_'+kind if via else ('line_shape' if kind=='shape' else kind+'_line'))", "key=({'smdpin':'smdpin_via','thrupin':'thrupin_via','via':'via_via','line':'via_line','shape':'via_shape'}.get(kind,'via_'+kind) if via else ('line_shape' if kind=='shape' else kind+'_line'))")
p.write_text(s,encoding='utf8');print('Updated GPIO6, explicitNSS and exact native spacing key order')