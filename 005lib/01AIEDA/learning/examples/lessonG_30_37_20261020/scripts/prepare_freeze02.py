from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonG_30_37_20261020')
s=(R/'scripts/challengesG.il').read_text().replace('axlDRCUpdate(t)','axlDRCUpdate(t) axlDBRefreshId(nil)')
(R/'scripts/challengesG_v2.il').write_text(s,encoding='ascii')
for key in ['4L','2L']:
 s=(R/f'scripts/freeze_{key}_01.scr').read_text().replace('challengesG.il','challengesG_v2.il').replace(f'freeze_{key}_01',f'freeze_{key}_02')
 (R/f'scripts/freeze_{key}_02.scr').write_text(s,encoding='ascii')
