from pathlib import Path
import json
B=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lesson28_stackup_20261019')
mapping=json.loads((B/'film_template_readonly.json').read_text())
for n in (2,4):
 names=['TOP','BOTTOM'] if n==2 else ['TOP','L2','L3','BOTTOM']
 lines=[]
 for f in mapping[str(n)]['films']:
  if f['name'] in names:
   layers=' '.join('"'+v+'"' for v in f['layers'])
   lines.append('unless(axlFilmCreate("%s" ?negative nil ?undefineLineWidth 0.0025 ?sequence %d ?vectorBasedPad t ?domains \'(ipc2581 pdf artwork visibility) ?layers \'(%s)) error("Copper film failed\\n"))'%(f['name'],f['sequence'],layers))
 lines.append('unless(axlFilmCreate("F28_DESIGN_OUTLINE" ?negative nil ?undefineLineWidth 0.0025 ?sequence 100 ?layers \'("BOARD GEOMETRY/DESIGN_OUTLINE")) error("Design outline film failed\\n"))')
 (B/'native'/('copper_films_%d.il'%n)).write_text('\n'.join(lines)+'\n',encoding='ascii')
p=B/'scripts'/'lesson28.il'
s=p.read_text()
s=s.replace('unless(axlSaveDesign(?design board','load(strcat(native if(n==2 then "/copper_films_2.il" else "/copper_films_4.il")))\n fprintf(f "FULL_DRC_RETURN=%L\\n" axlDRCUpdate(t))\n fprintf(f "FINAL_DRC_COUNT=%d STATE=%L\\n" length(axlDBGetDesign()->drcs) axlDBGetDesign()->drcState)\n unless(axlSaveDesign(?design board')
p.write_text(s,encoding='ascii')
