from pathlib import Path
import json,shutil
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
shutil.copyfile(R/'scripts/batchHI.il',R/'source/batchHI_b001_executed.il')
d=json.loads((R/'batches/power_4L_b001.json').read_text())
h=(R/'scripts/power_4L_b001.scr').read_text().split('skill errset(hiBatchProgram()')[0]
h+='skill errset(load("'+(R/'scripts/extraReadHI.il').as_posix()+'") t)\n'
out=(R/'logs/reopen_power_4L_b001').as_posix()
h+='skill errset(hiChallengeNeck("'+out+'" "HI_U2_SW_ESCAPE_P" 1.2 1.0) t)\n'
h+='skill errset(gSnapshot("'+out+'" "'+(R/'library').as_posix()+'") t)\n'
h+='skill errset(hiNetworkInventory("'+out+'") t)\n'
h+='skill errset(hiExtraRead("'+out+'") t)\n'
il='procedure(hiPowerReopenProof()\n let((f)\n  f=outfile("'+out+'/hi_reopen_endpoint_proofs.txt")\n  hiRegistry=nil\n'
for op in d['operations']:
 if op['type']=='via':
  il+='  hiBindExistingVia(f '+json.dumps(op['id'])+' '+json.dumps(op['net'])+' list('+' '.join(repr(float(x)) for x in op['xy'])+') '+json.dumps(op['padstack'])+')\n'
for op in d['operations']:
 if op.get('from') and op.get('to'):il+='  hiProof(f '+json.dumps(op['from'])+' '+json.dumps(op['to'])+' t)\n'
il+='  fprintf(f "HI_REOPEN_ALL_ENDPOINTS_COMPLETE\\n") close(f) t))\n'
(R/'scripts/reopen_power_4L_b001.il').write_text(il,encoding='ascii')
h+='skill errset(load("'+(R/'scripts/reopen_power_4L_b001.il').as_posix()+'") t)\n'
h+='skill errset(hiPowerReopenProof() t)\nquit\nfillin "yes"\n'
(R/'scripts/reopen_power_4L_b001.scr').write_text(h,encoding='ascii')
