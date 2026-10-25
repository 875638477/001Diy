from pathlib import Path
import hashlib,json
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonG_30_37_20261020')
# Preserve the exact earlier successful attempt SCR after its reused filename was regenerated.
old=(R/'scripts/place_4L_v1.scr').read_text().replace('/logs/place_4L_v1','/logs/place_4L_v2')
p=R/'source/place_4L_attempt02_original.scr';p.write_text(old,encoding='ascii')
assert hashlib.sha256(p.read_bytes()).hexdigest().upper()==json.loads((R/'logs/place_4L_v2/launch.json').read_text())['scriptSHA256']
for key in ['4L','2L']:
 src=(R/f'scripts/place_{key}_v2.scr').read_text()
 header=src[:src.index('skill errset(gPlace(')]
 header+='skill errset(load("'+(R/'scripts/reconcileG.il').as_posix()+'") t)\n'
 out=(R/f'native/G_{key}_PLACEMENT_v2.brd').as_posix()
 log=(R/f'logs/reconcile_{key}_01').as_posix()
 fn=f'gReconcile(gPlan "{out}" "{log}" "{(R/"library").as_posix()}" '+('t' if key=='2L' else 'nil')+')'
 (R/f'scripts/reconcile_{key}_01.scr').write_text(header+f'skill errset({fn} t)\nquit\nfillin "yes"\n',encoding='ascii')
print('APPROVED_NATIVE_ADJUSTMENTS_READY')
