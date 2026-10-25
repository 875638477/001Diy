from pathlib import Path
import json
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
m=json.loads((R/'scripts/source_service_2L_b015_guarded_compiled.json').read_text())
p=json.loads((R/'batches/source_service_2L_b015_guarded.json').read_text())
q=lambda x:json.dumps(x)
pt=lambda x:'list('+' '.join(map(str,x))+')'
ops=[]
for o in p['operations']:
 if o['type']=='deleteVia':ops.append('hiDeleteVia(f '+q(o['id'])+' '+q(o['net'])+' '+pt(o['xy'])+' '+q(o['padstack'])+')')
 elif o['type']=='deleteSegment':
  ops.append('hiDeleteSegment(f '+q(o['id'])+' '+q(o['net'])+' '+q(o['layer'])+' list('+' '.join(pt(v) for v in o['points'])+') '+str(o['width'])+')')
  break
out=R/'logs/ripup_topology_diagnostic_2L_02'
il=R/'scripts/ripup_topology_diagnostic_2L_02.il'
il.write_text('''procedure(hiRipupDiagnostic()
 let((f mark)
 f=outfile('''+q((out/'diagnostic.txt').as_posix())+''')
 mark=axlDBTransactionStart()
 unwindProtect(
 progn(
 axlDBControl('drcEnable nil)
 fprintf(f "BEFORE\\n")
 hiRouteRoles('''+q((R/'review/ripup_diagnostic_before').as_posix())+''')
 '''+'\n '.join(ops)+'''
 fprintf(f "AFTER_FIRST_TARGET_DELETE\\n")
 hiRouteRoles('''+q((R/'review/ripup_diagnostic_after').as_posix())+''')
 foreach(o axlExtractMap("C:/Program0/Cadence/SPB172/share/pcb/text/views/fgeo_bv.txt" nil)
 when(equal(o->objType "line") && equal(o->layer "ETCH/BOTTOM") && o->startEnd && (equal(o->startEnd list(list(40.3 30.3) list(35.4 30.3))) || equal(reverse(o->startEnd) list(list(40.3 30.3) list(35.4 30.3))))
 fprintf(f "REMAINING_TARGET actual=%L parent=%L\\n" o->?? o->parent->??)))
 t)
 progn(axlDBTransactionRollback(mark) axlDBRefreshId(nil) axlDBControl('drcEnable t)))
 fprintf(f "DIAGNOSTIC_COMPLETE_NO_SAVE_ROLLBACK_DRC_RESTORED=%L\\n" axlDBControl('drcEnable))
 close(f) t))
''',encoding='ascii')
loads=[x['snapshot'] for x in m['helperSnapshots'][:-1]]+[str(il)]
scr=R/'scripts/ripup_topology_diagnostic_2L_02.scr'
scr.write_text('set NOCONFIRM\n'+''.join('skill errset(load('+q(str(Path(x).as_posix()))+') t)\n' for x in loads)+'skill errset(hiRipupDiagnostic() t)\nquit\nfillin "yes"\n',encoding='ascii')
for n in ['before','after']:(R/('review/ripup_diagnostic_'+n)).mkdir(parents=True,exist_ok=True)
print(scr)


