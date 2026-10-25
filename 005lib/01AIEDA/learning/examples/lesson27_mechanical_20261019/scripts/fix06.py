from pathlib import Path
B=Path(r'D:/001DIY/005lib/01AIEDA/learning/examples/lesson27_mechanical_20261019')
p=B/'scripts/lesson27.il';s=p.read_text();(B/'logs/create05/rejected_source.il').write_text(s)
s=s.replace('l27_npth_d200_v2','l27_npth_d200_mech')
s=s.replace('  f=outfile(strcat(out "/package.txt"))','  axlSetSymbolType("mechanical")\n  f=outfile(strcat(out "/package.txt"))')
a=s.index('  style=make_axlTextOrientation');z=s.index('  unless(axlSaveDesign',a);s=s[:a]+s[z:]
s=s.replace('list("l27_npth_d200_mech" "PACKAGE")','list("l27_npth_d200_mech" "MECHANICAL")')
p.write_text(s)
p=B/'scripts/package.scr';p.write_text(p.read_text().replace('/logs/package02','/logs/package03'))
p=B/'scripts/run27.py';p.write_text(p.read_text().replace('library/l27_npth_d200_v2.dra','library/l27_npth_d200_mech.dra').replace("'package02')","'package03')"))
p=B/'scripts/create.scr';p.write_text(p.read_text().replace('/logs/create05','/logs/create06'))
(B/'F27_MECHANICAL.brd').rename(B/'logs/create05/F27_REJECTED_05.brd')
