from pathlib import Path
import json
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_power');p=json.loads((R/'SPI_external_2L_engineered_v9.json').read_text());p['batchId']='SPI_external_2L_engineered_v10';p['status']='FINAL_ENGINEERING_CANDIDATE_NEEDS_NATIVE_GLOBAL_INTEGRATION'
u={'SPI_NSS_EAST':{'xy':[29.6,32.46]},'SPI_NSS_EAST_TOP':{'points':[[31.2236,33.02],[30.16,33.02],[29.6,32.46]]},'SPI_NSS_BOTTOM_BRIDGE':{'points':[[29.6,32.46],[29.44,32.3],[20.4,32.3],[20.3,32.4]]},'SPI_GUARD_MISO_NSS':{'points':[[29.9,31.55],[21,31.55]]}}
for o in p['operations']:
 if o['id'] in u:o.update(u[o['id']])
p['engineeringRevision']='v10 freezes one coordinated NSS-source/ground-guard improvement after v9; no further independently-added optimization. Final actual plane refill is acceptance gate.'
(R/'SPI_external_2L_engineered_v10.json').write_text(json.dumps(p,indent=2),encoding='utf-8')
for a,z in [('precheck_SPI_external_2L_v9.py','precheck_SPI_external_2L_v10.py'),('review_SPI2L_v9_return.py','review_SPI2L_v10_return.py')]:
 s=(R/'scripts'/a).read_text().replace('engineered_v9.json','engineered_v10.json').replace('v9_precheck.json','v10_precheck.json').replace('v9_return_plan.json','v10_return_plan.json');(R/'scripts'/z).write_text(s,encoding='utf-8')
# four-layer original candidate actual geometry precheck
s=(R/'scripts/precheck_SPI_external_2L_v9.py').read_text().replace('postcritical_2L_b010','postcritical_4L_b010').replace("(R/'SPI_external_2L_engineered_v9.json')", "(H/'plans/SPI_external_4L_candidate_v5.json')").replace('v9_precheck.json','4L_v5_precheck.json')
(R/'scripts/precheck_SPI_external_4L_v5.py').write_text(s,encoding='utf-8')