from pathlib import Path
import json, os, subprocess, datetime,hashlib
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lesson07_completion_20261018')
source=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lesson07_padstacks\library\eda_l07_npth_200_ko.pxml').read_text()
import re
source=source.replace('eda_l07_npth_200_ko','eda_l07c_npth_200_null')
source=re.sub(r'  <pad><type>KEEPOUT</type>.*?</pad>\n','',source)
(R/'library/eda_l07c_npth_200_null.pxml').write_text(source,encoding='utf-8')
s=(R/'scripts/lesson07c.il').read_text()
a=s.index('  drill=make_axlPadStackDrill')
b=s.index('  unless(axlDBCreatePin(ps',a)
s=s[:a]+'''  ps=axlLoadPadstack("eda_l07c_npth_200_null")
  unless(ps error("Pure NULL padstack load failed\\n"))
  fprintf(f "xml_NULL_load=%L hole=%L plating=%L usage=%L\\n" ps ps->drillDiameter ps->plating ps->usage)
'''+s[b:]
(R/'scripts/lesson07c.il').write_text(s,encoding='ascii')
# Package and flash launcher with original official CLI; isolated working directories.
s=(R/'scripts/launch_package17.py').read_text().replace("p.add_argument('--mode'", "p.add_argument('--symbol',choices=['package','flash'],default='package')\np.add_argument('--mode'")
s=s.replace("['-symbol','package']","['-symbol',a.symbol]")
(R/'scripts/launch_symbol17.py').write_text(s,encoding='utf-8')
for stage,fn,args in [
 ('create_package06','l7cPackage',f'"{R.as_posix()}/library" "{R.as_posix()}/logs/create_package06"'),
 ('create_flash','l7cFlash',f'"{R.as_posix()}/library" "{R.as_posix()}/logs/create_flash"'),
 ('create_board','l7cBoard',f'"{R.as_posix()}/library" "{R.as_posix()}/logs/create_board"'),
 ('reopen_package','l7cRead',f'"{R.as_posix()}/logs/reopen_package"'),
 ('reopen_board','l7cRead',f'"{R.as_posix()}/logs/reopen_board"'),
 ('reopen_flash','l7cRead',f'"{R.as_posix()}/logs/reopen_flash"')]:
 (R/f'scripts/{stage}.scr').write_text(f'set NOCONFIRM\nskill errset(load("{R.as_posix()}/scripts/lesson07c.il") t)\nskill errset({fn}({args}) t)\nquit\nfillin "yes"\n',encoding='ascii')
print('Prepared NULL PXML, real launchers and six isolated scripts.')
