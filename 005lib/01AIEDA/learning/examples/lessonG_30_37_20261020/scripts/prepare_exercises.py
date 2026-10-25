from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonG_30_37_20261020')
for key in ['4L','2L']:
 src=(R/f'scripts/reconcile_{key}_02.scr').read_text()
 h=src[:src.index('skill errset(gReconcile(')]
 h+='skill errset(load("'+(R/'scripts/operation_exercisesG.il').as_posix()+'") t)\n'
 (R/f'scripts/exercises_{key}_01.scr').write_text(h+'skill errset(gOperationExercises("'+(R/f'logs/exercises_{key}_01').as_posix()+'") t)\nquit\nfillin "yes"\n',encoding='ascii')
