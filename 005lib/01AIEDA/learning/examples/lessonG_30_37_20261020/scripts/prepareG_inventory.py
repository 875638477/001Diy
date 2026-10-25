from pathlib import Path
import json,hashlib,shutil
A=Path(r'D:\001DIY\005lib\01AIEDA');R=A/'learning/examples/lessonG_30_37_20261020'
for s in ['source','backups','native','logs','inventory','library']:(R/s).mkdir(parents=True,exist_ok=True)
records=[]
def cp(src,dst):
 shutil.copy2(src,dst)
 records.append({'source':str(src),'copy':str(dst),'sha256':hashlib.sha256(src.read_bytes()).hexdigest().upper()})
F=A/'learning/examples/lessonF_stack_artwork_correction_20261019'
for name,new in [('F29_CONSTRAINTS_v4.brd','G_4L_INPUT.brd'),('F28_2L_USERFIX.brd','G_2L_INPUT.brd')]:cp(F/'current'/name,R/'backups'/new)
cp(F/'scripts/launch_fix.py',R/'scripts/launchG.py')
deps=[A/'learning/scripts/de_board_read.il']
for name in ['build29_v2.il','read29.il','extra_read29.il','specific_proof.il']:deps.append(A/'learning/examples/lesson29_constraints_20261019/scripts'/name)
for name in ['more28.il','mechanical28.il']:deps.append(A/'learning/examples/lesson28_stackup_20261019/scripts'/name)
deps.append(F/'scripts/correction.il')
for d in deps:cp(d,R/'source'/d.name)
for folder in [A/'learning/examples/de_15_26_20261019/library',A/'learning/examples/lesson27_mechanical_20261019/library',A/'learning/examples/lesson28_stackup_20261019/native']:
 for p in folder.iterdir():
  if p.is_file() and p.suffix.lower() in ['.psm','.pad','.dra']:
   dst=R/'library'/p.name
   if not dst.exists():cp(p,dst)
cp(A/'learning/examples/de_15_26_20261019/integrated_circuit.json',R/'source/integrated_circuit.json')
(R/'source/input_manifest.json').write_text(json.dumps(records,indent=2),encoding='utf8')
prefix='set NOCONFIRM\n'+''.join('skill errset(load("'+(R/'source'/d.name).as_posix()+'") t)\n' for d in deps)
prefix+='skill errset(load("'+(R/'scripts/inventoryG.il').as_posix()+'") t)\n'
for key in ['4L','2L']:
 tag='inventory_'+key
 (R/f'scripts/{tag}.scr').write_text(prefix+'skill errset(gInventory("'+(R/'logs'/tag).as_posix()+'" "'+(R/'library').as_posix()+'") t)\nquit\nfillin "yes"\n',encoding='ascii')
print('G_INPUTS_READY',len(records))
