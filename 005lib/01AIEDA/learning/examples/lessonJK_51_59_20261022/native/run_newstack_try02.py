import pathlib,shutil,json,hashlib,subprocess,sys
R=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonJK_51_59_20261022');H=R.parent/'lessonHI_38_50_20261021';v='4L';tag='newstack_4L_build_try02';log=R/'logs'/('native_'+tag);out=R/'exports/newstack_4L_TRAINING_NOT_FOR_FAB';assert out.is_dir()
base=R/'native/4L/JK_4L_J55_text_height_review_NOT_RELEASED.brd';work=R/'native/4L/newstack_4L_try02_WORKING_COPY.brd';assert not work.exists();shutil.copy2(base,work)
new=R/'native/4L/JK_4L_L2_GND_L3_V3V3_STACK_TRAINING_NOT_RELEASED.brd';assert not new.exists()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper();assert sha(base)=='9DEC773FE106E09C9844FEF5F160E1A1B3348BFC693926579F0CAF0A6A18DCF0'
proof=H/'source/readback_snapshots/reopen_padentry_4L_b019_stored/16_reopen_padentry_4L_b019_stored.il';s=proof.read_text().replace((H/'logs/reopen_padentry_4L_b019_stored').as_posix(),log.as_posix());(R/'native/newstack_endpoint_proofs_try02.il').write_text(s,encoding='ascii')
loads=sorted((R/'source/j55_readback_helpers/4L').glob('*.il'))+[R/'native/newstack_endpoint_proofs_try02.il',R/'native/native56_probe.il',R/'native/j55_plan_static.il',R/'native/j55_apply_core_v2.il',R/'native/j55_outer.il',R/'native/newstack.il']
scr='set NOCONFIRM\n'+''.join('skill errset(load("'+p.as_posix()+'") t)\n' for p in loads)+'skill errset(jkNewStack("'+log.as_posix()+'" "'+new.as_posix()+'") t)\nskill axlKillDesign()\nquit\n';(R/'native/newstack_build_try02.scr').write_text(scr,encoding='ascii')
(R/'native/newstack_provenance.json').write_text(json.dumps({'correctedSource':str(base),'sourceSHA256':sha(base),'scratch':str(work),'scratchSHA256':sha(work),'newOutput':str(new),'contract':'audits/j52_53_newstack_native_contract.json','contractSHA256':sha(R/'audits/j52_53_newstack_native_contract.json'),'architecture':'TOP components/signals, L2 continuous common GND, L3 single V3V3 power, BOTTOM signals; old HSE sole-anchor disconnection retired'},indent=2),encoding='utf8')
subprocess.run([sys.executable,str(R/'native/run_native56_v8.py'),'--variant','4L','--action','skill','--tag',tag,'--board',str(work),'--outdir',str(out),'--script',str(R/'native/newstack_build_try02.scr')],check=True)
assert new.exists(),'Native checks failed: no new board saved; inspect actual log.'
assert sha(base)=='9DEC773FE106E09C9844FEF5F160E1A1B3348BFC693926579F0CAF0A6A18DCF0'
print('NEWSTACK_SAVED',sha(new))
