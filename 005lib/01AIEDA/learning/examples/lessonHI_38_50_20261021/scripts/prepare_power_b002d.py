from pathlib import Path
import json
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
for key in ['4L','2L']:
 d=json.loads((R/'engineering_power/power_paths_02d.json').read_text())
 state=json.loads((R/f'inventory/current_{key}.json').read_text())
 d.update(batchId=f'power_{key}_b002d',variant=key,sourceExpectedSHA256=state['sha256'],sourceBoard=state['board'])
 d['constraintOperations']=[]
 if key=='4L':
  d['operations'].insert(0,{'type':'shape','id':'HI_GND_L3','net':'GND','layer':'L3','polygon':'ROUTE_KEEPIN','dynamic':True,'purpose':'Actual adjacent GND reference for BOTTOM signals; no nonGND L2/L3 etch permitted'})
 (R/f'batches/power_{key}_b002d.json').write_text(json.dumps(d,indent=2),encoding='utf8')
print('02D_PREPARED_WITH_4L_L3_ACTUAL_REFERENCE')
