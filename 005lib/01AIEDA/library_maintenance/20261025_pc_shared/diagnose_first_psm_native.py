import json,pathlib,shutil,importlib.util
M=pathlib.Path('D:/001DIY/005lib/01AIEDA/library_maintenance/20261025_pc_shared')
R=M/'global_first_probe_v1';R.mkdir(exist_ok=False);(R/'output').mkdir()
spec=importlib.util.spec_from_file_location('auditbase',pathlib.Path('D:/001DIY/004computer/lga1700/13shared_libraries_pc_20261025/w/pcb_migration/run_pc_native_audit.py'));b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
row=json.loads((M/'global_suffix_native_v1/c000/manifest.json').read_text())[0]
blank=R/'blank.brd';shutil.copyfile(M/'fixture4/EMPTY4.brd',blank)
log=R/'step.txt'
skill='load('+b.q(b.B/'psm_native_units.il')+')\n'
skill+='''procedure(psmNativePrepare(blank job)
 let((opened units accuracy extent f)
  f=outfile('''+b.q(log)+''') fprintf(f "BEFORE_OPEN\\n") drain(f)
  opened=axlOpenDesignForBatch(blank "wfl")
  fprintf(f "AFTER_OPEN=%L\\n" opened) drain(f)
  unless(opened error("Cannot open"))
  fprintf(f "SYMBOLS=%L PADS=%L\\n" axlDBGetDesign()->symdefs axlDBGetDesign()->padstacks) drain(f)
  units=nth(2 job) accuracy=nth(3 job) extent=nth(4 job)
  fprintf(f "BEFORE_UNITS %L %L\\n" units accuracy) drain(f)
  axlDBChangeDesignUnits(units accuracy)
  fprintf(f "AFTER_UNITS=%L\\n" axlDBGetDesignUnits()) drain(f)
  fprintf(f "BEFORE_EXTENTS %L\\n" extent) drain(f)
  unless(axlDBChangeDesignExtents(extent) error("Extents failed"))
  fprintf(f "AFTER_EXTENTS\\n") close(f) t))
'''
box=row['original_extents'];lit='(('+' '.join(box[0])+') ('+' '.join(box[1])+'))'
job='('+b.q(row['stem'])+' '+b.q(R/'output/0000.sexp')+' '+b.q(row['original_units'])+' '+str(row['original_accuracy'])+' '+lit+')'
skill+='psmNativeBatch('+b.q(blank)+" '("+job+') '+b.q(R/'status.tsv')+' '+b.q(b.PUBLIC/'01Psm_lib')+' '+b.q(b.PUBLIC/'01Pad_lib')+')\n'
(R/'probe.il').write_text(skill,encoding='ascii')
(R/'run.scr').write_text('set NOCONFIRM\nskill errset(load('+b.q(R/'probe.il')+') t)\nquit\nfillin "yes"\n',encoding='ascii')
e=b.envfor(R)
print(b.launch([b.CAD/'tools/bin/allegro.exe','-product','Allegro_performance','-safe','-nographic','-s',R/'run.scr','-p',R,blank],R,e,60,'probe'))