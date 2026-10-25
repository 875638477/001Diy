from pathlib import Path
import json
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_power');p=json.loads((R/'SPI_external_2L_engineered_v7.json').read_text());p['batchId']='SPI_external_2L_engineered_v8'
u={'SPI_SCK_EAST':{'xy':[30.62,29.87]},'SPI_SCK_EAST_TOP':{'points':[[32.0252,31],[31.75,31],[30.62,29.87]]},'SPI_SCK_BOTTOM_BRIDGE':{'points':[[30.62,29.87],[30.54,29.95],[21.85,29.95]]},'SPI_MISO_WEST':{'xy':[20.5,30.8]},'SPI_MISO_BOTTOM_BRIDGE':{'points':[[31.5,29.85],[31.1,30.25],[31.1,30.35],[30.65,30.8],[20.5,30.8]]},'SPI_MISO_WEST_TOP':{'points':[[20.5,30.8],[17.68,33.62],[7,33.62]]},'SPI_NSS_WEST':{'xy':[20.3,32.4]},'SPI_NSS_BOTTOM_BRIDGE':{'points':[[29.8,32.3],[20.4,32.3],[20.3,32.4]]},'SPI_NSS_WEST_TOP':{'points':[[20.3,32.4],[16.54,36.16],[7,36.16]]},'SPI_RETURN_SCK_E':{'xy':[30.9,29.1]},'SPI_GUARD_CLOCK_MOSI':{'points':[[28.6,29],[28.85,29.25],[22.8,29.25]]}}
p['operations']=[o for o in p['operations'] if o['id']!='SPI_RETURN_MISO_W']
for o in p['operations']:
 if o['id'] in u:o.update(u[o['id']])
(R/'SPI_external_2L_engineered_v8.json').write_text(json.dumps(p,indent=2),encoding='utf-8')
s=(R/'scripts/precheck_SPI_external_2L_v7.py').read_text().replace('engineered_v7.json','engineered_v8.json').replace('v7_precheck.json','v8_precheck.json')
(R/'scripts/precheck_SPI_external_2L_v8.py').write_text(s,encoding='utf-8')