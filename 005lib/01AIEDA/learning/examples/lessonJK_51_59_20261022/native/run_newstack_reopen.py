from pathlib import Path
import subprocess,sys,hashlib
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonJK_51_59_20261022');H=R.parent/'lessonHI_38_50_20261021';s=(R/'native/run_native56_v8.py').read_text().replace("P.add_argument('--script');a=P.parse_args()","P.add_argument('--script');P.add_argument('--readonly',action='store_true');a=P.parse_args()")
s=s.replace("if a.action=='params_gui':", "if a.action=='skill' and a.readonly:args.insert(-1,'-readonly')\nif a.action=='params_gui':");(R/'native/run_native56_v9.py').write_text(s,encoding='utf8')
log=R/'logs/native_newstack_4L_reopen_01';proof=H/'source/readback_snapshots/reopen_padentry_4L_b019_stored/16_reopen_padentry_4L_b019_stored.il';p=R/'native/newstack_fresh_proofs.il';p.write_text(proof.read_text().replace((H/'logs/reopen_padentry_4L_b019_stored').as_posix(),log.as_posix()),encoding='ascii')
loads=sorted((R/'source/j55_readback_helpers/4L').glob('*.il'))+[p,R/'native/native56_probe.il',R/'native/j55_plan_static.il',R/'native/j55_apply_core_v2.il',R/'native/j55_outer.il',R/'native/newstack.il',R/'native/newstack_read.il']
scr=R/'native/newstack_reopen.scr';scr.write_text('set NOCONFIRM\n'+''.join('skill errset(load("'+p.as_posix()+'") t)\n' for p in loads)+'skill errset(jkNewStackRead("'+log.as_posix()+'") t)\nskill axlKillDesign()\nquit\n',encoding='ascii')
board=R/'native/4L/JK_4L_L2_GND_L3_V3V3_STACK_TRAINING_NOT_RELEASED.brd';subprocess.run([sys.executable,str(R/'native/run_native56_v9.py'),'--variant','4L','--action','skill','--tag','newstack_4L_reopen_01','--board',str(board),'--outdir',str(R/'exports/newstack_4L_TRAINING_NOT_FOR_FAB'),'--script',str(scr),'--readonly'],check=True)
assert (log/'newstack_fresh_plane_contract.txt').exists() and 'NEW_STACK_CENTERLINE_REFERENCE_SAMPLES_COMPLETE' in (log/'newstack_reference_samples.tsv').read_text()
print('NEWSTACK_FRESH_PASSED',hashlib.sha256(board.read_bytes()).hexdigest().upper())
