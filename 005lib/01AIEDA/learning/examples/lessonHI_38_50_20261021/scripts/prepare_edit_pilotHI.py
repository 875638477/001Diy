from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
for key in ['4L','2L']:
 src=(R/f'scripts/baseline_{key}_02.scr').read_text()
 h=src[:src.index('skill errset(axlDRCUpdate')]
 h+='skill errset(load("'+(R/'scripts/edit_pilotHI.il').as_posix()+'") t)\n'
 h+='skill errset(hiEditPilot("'+(R/f'logs/edit_pilot_{key}_01').as_posix()+'" "'+(R/'library').as_posix()+'") t)\nquit\nfillin "yes"\n'
 (R/f'scripts/edit_pilot_{key}_01.scr').write_text(h,encoding='ascii')
