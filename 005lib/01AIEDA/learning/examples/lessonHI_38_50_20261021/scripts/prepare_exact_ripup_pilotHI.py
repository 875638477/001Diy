from pathlib import Path
import json
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
p=R/'scripts/batchHI_exact_ripup_v2.il';s=p.read_text();s=s.replace('targets=cons(selected targets))','drain(f) targets=cons(selected targets))').replace('mark=axlDBTransactionStart()','drain(f) mark=axlDBTransactionStart()').replace('after=hiExactRipupInventory(nil)','fprintf(f "HI_EXACT_NATIVE_LIST_DELETE_RETURNED\\n") drain(f)\n    after=hiExactRipupInventory(nil)');p.write_text(s,encoding='ascii')
m=json.loads((R/'scripts/source_service_2L_b015_guarded_try02_compiled.json').read_text());plan=json.loads((R/'batches/source_service_2L_b015_guarded_try02.json').read_text());ds=[]
q=json.dumps
pt=lambda x:'list('+' '.join(map(str,x))+')'
for d in plan['operations']:
 if d['type'] not in ['deleteVia','deleteSegment']:break
 if d['type']=='deleteVia':ds.append('list('+q(d['type'])+' '+q(d['id'])+' '+q(d['net'])+' "" '+pt(d['xy'])+' '+q(d['padstack'])+')')
 else:ds.append('list('+q(d['type'])+' '+q(d['id'])+' '+q(d['net'])+' '+q(d['layer'])+' list('+' '.join(pt(v) for v in d['points'])+') '+str(d['width'])+')')
out=R/'logs/exact_batch_ripup_pilot_2L_05';il=R/'scripts/exact_batch_ripup_pilot_2L_05.il'
il.write_text('procedure(hiExactPilot() let((f mark) f=outfile('+q((out/'pilot.txt').as_posix())+') mark=axlDBTransactionStart() unwindProtect(progn(axlDBControl(\'drcEnable nil) hiDeleteExactBatch(f list('+' '.join(ds)+')) t) progn(axlDBTransactionRollback(mark) axlDBRefreshId(nil) axlDBControl(\'drcEnable t))) fprintf(f "EXACT_BATCH_PILOT_ROLLBACK_COMPLETE_NO_SAVE\\n") close(f) t))\n',encoding='ascii')
loads=[x['snapshot'] for x in m['helperSnapshots'][:-2]]+[str(p),str(il)]
scr=R/'scripts/exact_batch_ripup_pilot_2L_05.scr';scr.write_text('set NOCONFIRM\n'+''.join('skill errset(load('+q(Path(x).as_posix())+') t)\n' for x in loads)+'skill errset(hiExactPilot() t)\nquit\nfillin "yes"\n',encoding='ascii');print(scr)
