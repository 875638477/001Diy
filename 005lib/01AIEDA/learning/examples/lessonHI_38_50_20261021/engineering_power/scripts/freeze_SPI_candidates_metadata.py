from pathlib import Path
import json
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_power')
for v,fn in [('2L','SPI_external_2L_engineered_v10.json'),('4L','SPI_external_4L_engineered_v6.json')]:
 f=R/fn;p=json.loads(f.read_text());p['sourceNativeLog']=str(R.parent/f'logs/reopen_postcritical_{v}_b010');p['sourceCheckpoint']=str(R.parent/f'inventory/checkpoints/postcritical_{v}_b010');p['requiredProofs']=[dict(net=net,source=src,target=tgt) for net,src,tgt in [('SPI_SCK','R21.2','J6.2'),('SPI_MOSI','R22.2','J6.3'),('SPI_MISO','R24.2','J6.4'),('SPI_NSS','R23.2','J6.5')]];f.write_text(json.dumps(p,indent=2),encoding='utf-8')
f=R/'scripts/precheck_SPI_external_4L_v6.py';f.write_text(f.read_text().replace('SPI_external_2L_4L_v6_precheck','SPI_external_4L_v6_precheck'),encoding='utf-8')
print('4Lops',len(json.loads((R/'SPI_external_4L_engineered_v6.json').read_text())['operations']))