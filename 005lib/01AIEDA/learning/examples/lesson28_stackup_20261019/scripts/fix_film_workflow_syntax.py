from pathlib import Path
B=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lesson28_stackup_20261019')
p=B/'scripts'/'workflow.py';s=p.read_text();a=s.index("elif mode.startswith('filmfix'):");b=s.index("elif mode.startswith('reopen'):")
s=s[:a]+'''elif mode.startswith('filmfix'):
 n=int(mode[-1]);board=B/'native'/('F28_%dL.brd'%n);out=B/'logs'/tag
 s=script(tag,'skill errset(l28FilmFix(%d "%s" "%s" "%s") t)'%(n,board.as_posix(),out.as_posix(),(B/'native').as_posix()))
 launch('edit',board,s,tag)
 assert 'L28_FILM_FIX COMPLETE' in (out/'fix.txt').read_text()
'''+s[b:]
p.write_text(s,encoding='ascii')
p=B/'scripts'/'lesson28.il';s=p.read_text();a=s.index('procedure(l28FilmFix')
s=s[:a]+r'''procedure(l28FilmFix(n board out native)
 let((f)
 f=outfile(strcat(out "/fix.txt"))
 load(strcat(native if(n==2 then "/copper_films_2_exact.il" else "/copper_films_4_exact.il")))
 fprintf(f "FULL_DRC_RETURN=%L COUNT=%d STATE=%L\n" axlDRCUpdate(t) length(axlDBGetDesign()->drcs) axlDBGetDesign()->drcState)
 unless(axlSaveDesign(?design board ?noMru t ?noConfirm t) error("Film correction save failed\n"))
 fprintf(f "L28_FILM_FIX COMPLETE\n") close(f) t))
'''
p.write_text(s,encoding='ascii')
print('Syntax correction applied')
