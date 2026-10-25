from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
s=(R/'scripts/compile_batchHI_v6.py').read_text()
s=s.replace(" if typ=='bindShape':", " if typ=='deleteSegment':statements.append(f'hiDeleteSegment(f {q(ident)} {q(net)} {q(op[\"layer\"])} {points(op[\"points\"])} {num(op[\"width\"])})')\n elif typ=='bindShape':")
(R/'scripts/compile_batchHI_v7.py').write_text(s,encoding='ascii')
s=(R/'scripts/prepare_readbackHI_v4.py').read_text()
s=s.replace("h+='skill errset(hiShapeBoundaryRead(\"'+out+'\") t)\\n'","h+='skill errset(hiShapeBoundaryRead(\"'+out+'\") t)\\n'\nh+='skill errset(hiRouteRoles(\"'+out+'\") t)\\n'")
(R/'scripts/prepare_readbackHI_v5.py').write_text(s,encoding='ascii')
for v in ['4L','2L']:
 tag='roles_mcu_'+v+'_b006'
 out=(R/'logs'/tag).as_posix()
 scr='set NOCONFIRM\nskill errset(load("'+(R/'scripts/batchHI_shapes_v3.il').as_posix()+'") t)\nskill errset(hiRouteRoles("'+out+'") t)\nquit\nfillin "yes"\n'
 (R/f'scripts/{tag}.scr').write_text(scr,encoding='ascii')
print('exact segment deletion and native thermal relief exporter prepared')
