from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonG_30_37_20261020')
for key in ['4L','2L']:
 src=(R/f'scripts/reconcile_{key}_02.scr').read_text()
 h=src[:src.index('skill errset(gReconcile(')]
 h+='skill errset(load("'+(R/'scripts/local_copperG.il').as_posix()+'") t)\n'
 h+='skill errset(load("'+(R/'scripts/local_loops01.il').as_posix()+'") t)\n'
 layer='ETCH/L2' if key=='4L' else 'ETCH/BOTTOM'
 fn=f'gLocalLoops("{(R/f"logs/loops_{key}_01").as_posix()}" "{(R/f"native/G_{key}_LOOPS_v1.brd").as_posix()}" "{(R/"library").as_posix()}" "{layer}")'
 (R/f'scripts/loops_{key}_01.scr').write_text(h+f'skill errset({fn} t)\nquit\nfillin "yes"\n',encoding='ascii')
