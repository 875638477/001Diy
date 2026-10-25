from pathlib import Path
import subprocess
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonG_30_37_20261020')
P=Path(r'D:\001DIY\005lib\01AIEDA\learning\tools\python_3_14_0\python.exe')
for key in ['4L','2L']:
 tag=f'{key}_v3'
 subprocess.run([str(P),str(R/'scripts/compile_placement.py'),'--variant',key,'--tag',tag],check=True)
 src=(R/f'scripts/place_{tag}.scr').read_text();header=src[:src.index('skill errset(gPlace(')]
 header+='skill errset(load("'+(R/'scripts/reconcileG.il').as_posix()+'") t)\n'
 fn=f'gReconcile(gPlan "{(R/f"native/G_{key}_PLACEMENT_v3.brd").as_posix()}" "{(R/f"logs/reconcile_{key}_02").as_posix()}" "{(R/"library").as_posix()}" nil)'
 (R/f'scripts/reconcile_{key}_02.scr').write_text(header+f'skill errset({fn} t)\nquit\nfillin "yes"\n',encoding='ascii')
