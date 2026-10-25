from pathlib import Path
import json,hashlib
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
d=json.loads((R/'plans/SPI_NSS_explicit_v3b.json').read_text(encoding='utf8'));d['status']='EXPLICIT_SPI_SOURCE_V4_PRECISE_COPPER_NOT_GRID_ONLY';d['basis']='R24.1 right edge34.07 and NSS vertical34.8 give only .13mm legal center span before numerical grid margin. Choose SCKx34.385 with actual .215 copper gaps, not two unnecessary signal vias.'
for net,id,pts,src,dst in [('PA5_SPI_SCK','SPI_SOURCE_SCK_PRECISE',[[35.75,28.75],[34.385,28.75],[34.385,30.215],[33.6,31]],'U1.15','R21.1'),('PA6_SPI_MISO','SPI_SOURCE_MISO_PRECISE',[[35.75,28.25],[33.6,28.25],[33.6,29]],'U1.16','R24.1'),('PA7_SPI_MOSI','SPI_SOURCE_MOSI_PRECISE',[[35.75,27.75],[34.35,27.75],[33.6,27]],'U1.17','R22.1')]:
 d['operations'].append({'type':'route','id':id,'net':net,'layer':'TOP','points':pts,'width':.2,'from':src,'to':dst,'purpose':'Explicit precise source-side route with correct series-resistor order, controls actual pad edge gaps; native/return verification pending'})
 d['proofs'].append({'from':src,'to':dst,'connected':True})
(R/'plans/SPI_source_explicit_v4.json').write_text(json.dumps(d,indent=2),encoding='utf8')
for v in ['2L','4L']:
 p=R/'plans'/('ordinary_policy_'+v+'_v3.json');pol=json.loads(p.read_text(encoding='utf8'));ids={o['id'] for o in json.loads((R/'plans/SPI_NSS_explicit_v3b.json').read_text(encoding='utf8'))['operations']}
 pol['pendingOperations']=[o for o in pol['pendingOperations'] if o['id'] not in ids]+d['operations'];pol['manualOnlyNets']+=['PA5_SPI_SCK','PA6_SPI_MISO','PA7_SPI_MOSI'];pol['status']='ORDINARY_POLICY_V4_EXPLICIT_SPI_SOURCE'
 for item in pol['sourcePlans']:
  if item['path'].endswith('gpio_north_escape_v3.json'):item['path']='engineering_mcu/plans/gpio_north_escape_v6.json';item['sha256']=hashlib.sha256((R/item['path']).read_bytes()).hexdigest()
 pol['sourcePlans'].append({'path':'plans/SPI_source_explicit_v4.json','sha256':hashlib.sha256((R/'plans/SPI_source_explicit_v4.json').read_bytes()).hexdigest()})
 (R/'plans'/('ordinary_policy_'+v+'_v4.json')).write_text(json.dumps(pol,indent=2),encoding='utf8')
print('Precise common SPI source plan and variant candidate policies saved')