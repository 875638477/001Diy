from pathlib import Path
import re
B=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lesson28_stackup_20261019')
for n in (2,4):
 src=Path(r'D:\001DIY\005lib\01env')/('drill%d.txt'%n)
 s=src.read_text(encoding='utf-8',errors='replace');res=[]
 names=['TOP','BOTTOM'] if n==2 else ['TOP','L2','L3','BOTTOM']
 for m in re.finditer(r'axlFilmCreate\(\s*"([^"]+)"([\s\S]*?)(?=axlFilmCreate|\Z)',s):
  if m[1] in names:res.append(m[0].strip())
 res.append('axlFilmCreate("F28_DESIGN_OUTLINE" ?negative nil ?undefineLineWidth 0.0025 ?sequence 100 ?rotation 0 ?xOffset 0 ?yOffset 0 ?shapeBoundingBox 2.54 ?mirrored nil ?fullContact nil ?suppressUnconnectPads nil ?drawMissingPadApertures nil ?useApertureRotation nil ?suppressShapeFill nil ?vectorBasedPad t ?drawHolesOnly nil ?layers \'("BOARD GEOMETRY/DESIGN_OUTLINE"))')
 (B/'native'/('copper_films_%d_exact.il'%n)).write_text('\n'.join(res)+'\n',encoding='ascii')
p=B/'scripts'/'lesson28.il'
old=p.read_text();(B/'logs'/'build4_01'/'executed_source.il').write_text(old,encoding='ascii')
s=old+'''
procedure(l28FilmFix(n board out native)
 let((f)
 f=outfile(strcat(out "/fix.txt"))
 load(strcat(native if(n==2 then "/copper_films_2_exact.il" else "/copper_films_4_exact.il")))
 fprintf(f "FULL_DRC_RETURN=%L COUNT=%d STATE=%L\\n" axlDRCUpdate(t) length(axlDBGetDesign()->drcs) axlDBGetDesign()->drcState)
 unless(axlSaveDesign(?design board ?noMru t ?noConfirm t) error("Film correction save failed\\n"))
 fprintf(f "L28_FILM_FIX COMPLETE\\n") close(f) t))
'''
p.write_text(s,encoding='ascii')
w=B/'scripts'/'workflow.py'
s=w.read_text()
s=s.replace("elif mode.startswith('reopen'):","elif mode.startswith('filmfix'):\\n n=int(mode[-1]);board=B/'native'/('F28_%dL.brd'%n);out=B/'logs'/tag\\n s=script(tag,'skill errset(l28FilmFix(%d \\\"%s\\\" \\\"%s\\\" \\\"%s\\\") t)'%(n,str(board).replace('\\\\\\\\','/'),str(out).replace('\\\\\\\\','/'),str(B/'native').replace('\\\\\\\\','/')))\\n launch('edit',board,s,tag)\\n assert 'L28_FILM_FIX COMPLETE' in (out/'fix.txt').read_text()\\nelif mode.startswith('reopen'):")
w.write_text(s,encoding='ascii')
print('Exact films prepared')
