from pathlib import Path
import json,hashlib
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
d=json.loads((R/'batches/power_4L_b001.json').read_text())
d.update(batchId='power_2L_b001',variant='2L',sourceExpectedSHA256=hashlib.sha256((R/'native/HI_2L_PROFILE_b001.brd').read_bytes()).hexdigest().upper())
for op in d['constraintOperations']:
 if op['type']=='csetCopy':op['copyFrom']='HI2L_P_SWITCH'
 if op['type']=='region':op['assignments'][0]['netClass']='HI2L_SWITCH_P'
(R/'batches/power_2L_b001.json').write_text(json.dumps(d,indent=2),encoding='utf8')
