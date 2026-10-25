from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
s=(R/'scripts/edit_pilotHI.il').read_text()
s=s.replace(' "SOLDERMASK_TOP" "SOLDERMASK_BOTTOM"','')
s=s.replace('shape=car(axlDBCreateRectangle(list(50:48 55:52) t "ETCH/TOP" "GND"))','path=axlPathStart(list(50:48 55:48 55:52 50:52 50:48) 0.0)\n  shape=axlDBCreateOpenShape(path t "ETCH/TOP" "GND")')
s=s.replace('  unless(axlDBOpenShape(shape) error("Cannot open plane to create permanent void\\n"))\n','')
s=s.replace('ret=axlDBCreateCloseShape(shape)','ret=axlDBCreateCloseShape(shape t)')
(R/'scripts/edit_pilotHI_v2.il').write_text(s,encoding='ascii')
for key in ['4L','2L']:
 s=(R/f'scripts/edit_pilot_{key}_01.scr').read_text().replace('edit_pilotHI.il','edit_pilotHI_v2.il').replace(f'edit_pilot_{key}_01',f'edit_pilot_{key}_02')
 (R/f'scripts/edit_pilot_{key}_02.scr').write_text(s,encoding='ascii')
