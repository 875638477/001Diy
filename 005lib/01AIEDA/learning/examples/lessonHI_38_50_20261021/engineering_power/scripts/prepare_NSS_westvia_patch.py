from pathlib import Path
import json
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_power')
p=json.loads((R/'source/root_SPI_NSS_explicit_v3b.json').read_text(encoding='utf-8'))
p['status']='POWER_REVIEW_PROPOSAL_PATCH_ROOT_NSS3B_WESTVIA_KEEP_ROOT_APPROVAL'
for o in p['operations']:
 if o['id']=='NSS_PULLUP_WEST_VIA':o['xy']=[32.2,22]
 if o['id']=='NSS_PULLUP_BOTTOM':o['points'][-2:]=[[32.2,21.3],[32.2,22]]
 if o['id']=='NSS_PULLUP_RESISTOR':o['points']=[[32.2,22],[32,21]]
(R/'source/root_SPI_NSS_westvia_patch_proposal.json').write_text(json.dumps(p,indent=2)+'\n',encoding='utf-8')
s=(R/'scripts/precheck_prefilter08_NSS3b.py').read_text()
s=s.replace("'source/root_SPI_NSS_explicit_v3b.json'","'source/root_SPI_NSS_westvia_patch_proposal.json'").replace("'readouts/Prefilter08_NSS3b_power_group_precheck.json'","'readouts/Prefilter08_NSS_westvia_patch_power_group_precheck.json'")
(R/'scripts/precheck_prefilter08_NSSpatched.py').write_text(s)
print('preparedNSSpatch')
