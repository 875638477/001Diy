from pathlib import Path
import json,hashlib
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');d=json.loads((R/'plans/SPI_source_explicit_v4.json').read_text(encoding='utf8'))
for o in d['operations']:
 if o['id']=='NSS_PULLUP_WEST_VIA':o['xy']=[32.2,22]
 if o['id']=='NSS_PULLUP_BOTTOM':o['points']=[[39,26.2],[39,21.3],[32.2,21.3],[32.2,22]]
 if o['id']=='NSS_PULLUP_RESISTOR':o['points']=[[32.2,22],[32,21]]
d['status']='EXPLICIT_SPI_SOURCE_V5_WESTVIA_CLEAR_BOOT1';d['errata']+=' West signalvia32,22.2 also left only .114418 to BOOT1 pad; moved32.2,22 after independent full-copper screen before native.'
(R/'plans/SPI_source_explicit_v5.json').write_text(json.dumps(d,indent=2),encoding='utf8')
for v in ['2L','4L']:
 pol=json.loads((R/'plans'/('ordinary_policy_'+v+'_v4.json')).read_text(encoding='utf8'));old=json.loads((R/'plans/SPI_source_explicit_v4.json').read_text(encoding='utf8'));oldids={o['id'] for o in old['operations']}
 pol['pendingOperations']=[o for o in pol['pendingOperations'] if o['id'] not in oldids]+d['operations'];pol['status']='ORDINARY_POLICY_V5_EXPLICIT_SPI_SOURCE'
 for item in pol['sourcePlans']:
  if item['path']=='plans/SPI_source_explicit_v4.json':item['path']='plans/SPI_source_explicit_v5.json';item['sha256']=hashlib.sha256((R/item['path']).read_bytes()).hexdigest()
 (R/'plans'/('ordinary_policy_'+v+'_v5.json')).write_text(json.dumps(pol,indent=2),encoding='utf8')
print('NSS west signalvia corrected in source plan v5')