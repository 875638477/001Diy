from pathlib import Path
import json,hashlib,subprocess,sys,shutil
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
helper=(R/'scripts/batchHI_dynamic_void_and_ground_trial_v2.il').read_text();helper=helper.replace('polygon differs\\n"))) shape))','polygon differs\\n")))\n  when(equal(id "B018_APP_TOP_TRIAL") hiRemoveActualUnconnectedTopFragments(f shape)) shape))')
helper+='''
procedure(hiRemoveActualUnconnectedTopFragments(f mother)
 let((common candidates allterm graph poly ret)
  axlDBRefreshId(nil) common=gConnectedObjects(gPin("C1" "2")) candidates=nil allterm=hiAllVias()
  foreach(c axlDBGetDesign()->components foreach(p c->symbol->pins allterm=cons(p allterm)))
  foreach(s axlDBGetShapes("ETCH/TOP")
   when(s->shapeBoundary && equal(s->shapeBoundary mother) && !member(s common)
    graph=gConnectedObjects(s)
    when(exists(p allterm member(p graph)) error("Refuse to delete isolated copper with any real pin or via\\n"))
    poly=car(axlPolyFromDB(s)) unless(poly error("Cannot read actual generated island polygon\\n"))
    fprintf(f "HI_TOP_GENERATED_NO_TERMINAL_FRAGMENT_PRE_VOID attributes=%L polyArea=%L realArcPolygon=%L\\n" s->?? poly->area poly->vertices)
    candidates=append(candidates list(poly))))
  foreach(poly candidates
   ret=axlDBCreateVoid(mother poly)
   unless(ret error("Cannot create permanent void from actual no-terminal fragment\\n"))
   fprintf(f "HI_TOP_ISLAND_REMOVAL_PERMANENT_VOID actual=%L originalArea=%L\\n" ret->?? poly->area))
  unless(equal(axlShapeDynamicUpdate(mother t) 0) error("Cannot refill after controlled real island removal\\n"))
  fprintf(f "HI_TOP_FRAGMENT_CLEANUP_COUNT=%d PRESERVED_ORIGINAL_QUIET_VOID=t GLOBAL_PARAMETERS_UNCHANGED=t\\n" length(candidates)) t))
'''
assert 'hiRemoveActualUnconnectedTopFragments(f shape)' in helper;(R/'scripts/batchHI_dynamic_void_and_ground_trial_v3.il').write_text(helper,encoding='ascii');s=(R/'scripts/compile_batchHI_v35.py').read_text().replace('batchHI_dynamic_void_and_ground_trial_v2.il','batchHI_dynamic_void_and_ground_trial_v3.il');(R/'scripts/compile_batchHI_v36.py').write_text(s,encoding='utf8')
api=R/'source/api_b018_TOP_trial';api.mkdir(exist_ok=True);records=[]
for p in [Path(r'C:\Program0\Cadence\SPB172\doc\algroshapes\algroshapes.html'),Path(r'C:\Program0\Cadence\SPB172\share\pcb\examples\skill\DOC\FUNCS\axlDBCreateVoid.txt'),Path(r'C:\Program0\Cadence\SPB172\share\pcb\examples\skill\DOC\FUNCS\axlPolyFromDB.txt')]:
 dest=api/p.name;shutil.copyfile(p,dest);records.append({'original':str(p),'copy':str(dest),'sha256':sha(dest)})
(api/'manifest.json').write_text(json.dumps(records,indent=2))
for v in ['4L','2L']:
 d=json.loads((R/f'batches/TOP_trial_{v}_b018_PRE_ALL69_DRC_PENDING_try03.json').read_text());cfg=json.loads((R/f'native_work/b018_{v}_try03/guard_configuration.json').read_text());d['controlledTrialGeneratedIslandRemoval']={'scope':'Only new B018_APP_TOP_TRIAL generated TOP fragments without any real component pin or via and outside common C1.2 graph','method':'Actual axlPolyFromDB arc polygon copied as permanent BOUNDARY void via axlDBCreateVoid; global dynamic parameters and old manual copper unchanged','primaryDocumentation':'source/api_b018_TOP_trial/algroshapes.html#1035489','futureSouthRework':'Trial fragment voids must be reconsidered after South reroute; never claim they are final immutable keepouts'};work=R/f'native_work/b018_{v}_try04';work.mkdir(exist_ok=False);scratch=work/'input.brd';scratch.write_bytes(Path(d['inputBoardIdentity']['board']).read_bytes());d['executionGuard']['scratchWritableWorkingCopy']=str(scratch);tag=f'TOP_trial_{v}_b018_PRE_ALL69_DRC_PENDING_try04';p=R/f'batches/{tag}.json';p.write_text(json.dumps(d,indent=2));subprocess.run([sys.executable,str(R/'scripts/compile_batchHI_v36.py'),'--plan',str(p),'--variant',v,'--tag',tag],check=True);mp=R/f'scripts/{tag}_compiled.json';m=json.loads(mp.read_text());cfg.update(tag=tag,scratchWritableWorkingCopy=str(scratch),scratchSHA256=sha(scratch),plan=str(p),planSHA256=sha(p),compiledMetadata=str(mp),compiledMetadataSHA256=sha(mp),script=m['script'],scriptSHA256=sha(Path(m['script'])),log=m['log']);(work/'guard_configuration.json').write_text(json.dumps(cfg,indent=2))
