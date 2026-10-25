from pathlib import Path
import json
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_power');p=json.loads((R/'SPI_external_2L_engineered_v8.json').read_text());p['batchId']='SPI_external_2L_engineered_v9'
u={'SPI_SCK_EAST':{'xy':[30.8,29.95]},'SPI_SCK_EAST_TOP':{'points':[[32.0252,31],[31.85,31],[30.8,29.95]]},'SPI_SCK_BOTTOM_BRIDGE':{'points':[[30.8,29.95],[21.85,29.95]]},'SPI_MISO_EAST':{'xy':[31.65,29.77]},'SPI_MISO_EAST_TOP':{'points':[[32.0252,29],[31.65,29.3752],[31.65,29.77]]},'SPI_MISO_BOTTOM_BRIDGE':{'points':[[31.65,29.77],[31.42,30],[31.42,30.23],[30.85,30.8],[20.5,30.8]]}}
for o in p['operations']:
 if o['id'] in u:o.update(u[o['id']])
(R/'SPI_external_2L_engineered_v9.json').write_text(json.dumps(p,indent=2),encoding='utf-8');s=(R/'scripts/precheck_SPI_external_2L_v7.py').read_text().replace('engineered_v7.json','engineered_v9.json').replace('v7_precheck.json','v9_precheck.json');(R/'scripts/precheck_SPI_external_2L_v9.py').write_text(s,encoding='utf-8')