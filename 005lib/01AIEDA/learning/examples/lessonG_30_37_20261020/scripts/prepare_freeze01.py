from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonG_30_37_20261020')
(R/'current').mkdir(exist_ok=True)
s=(R/'scripts/finalG_v2.il').read_text().replace("axlCNSGetPhysical(c nil k)","axlCNSGetPhysical(c \"TOP\" k)")
(R/'scripts/finalG_v3.il').write_text(s,encoding='ascii')
for key in ['4L','2L']:
 src=(R/f'scripts/bulk_{key}_01.scr').read_text();h=src[:src.index('skill errset(gBulk(')]
 h=h.replace('finalG.il','finalG_v3.il')
 h+='skill errset(load("'+(R/'scripts/challengesG.il').as_posix()+'") t)\n'
 layer='ETCH/L2' if key=='4L' else 'ETCH/BOTTOM'
 fn=f'gFreeze("{(R/f"logs/freeze_{key}_01").as_posix()}" "{(R/f"current/G_{key}_LAYOUT_v1.brd").as_posix()}" "{(R/"library").as_posix()}" "{layer}")'
 (R/f'scripts/freeze_{key}_01.scr').write_text(h+f'skill errset({fn} t)\nquit\nfillin "yes"\n',encoding='ascii')
 # Final readonly directly on canonical current path.
 fn=f'gSnapshot("{(R/f"logs/final_reopen_{key}_01").as_posix()}" "{(R/"library").as_posix()}")'
 proof=f'gGFinalProof("{(R/f"logs/final_reopen_{key}_01").as_posix()}" "{layer}")'
 (R/f'scripts/final_reopen_{key}_01.scr').write_text(h+f'skill errset(axlDRCUpdate(t) t)\nskill errset({fn} t)\nskill errset({proof} t)\nquit\nfillin "yes"\n',encoding='ascii')
