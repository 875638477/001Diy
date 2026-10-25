from pathlib import Path
import json,hashlib,subprocess,sys
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
s=(R/'scripts/batchHI_dynamic_void_and_ground_trial_v3.il').read_text().replace('  hiGroundTrialHealthCount=hiGroundTrialHealthCount+1','  when(expectedVias==84 && hiGroundTrialHealthCount==0 hiRemoveExplicitNorthBottomFragment(out))\n  hiGroundTrialHealthCount=hiGroundTrialHealthCount+1')
s+='''
procedure(hiRemoveExplicitNorthBottomFragment(out)
 let((f matches s mother poly graph allterm ret expected actual ok)
  f=outfile(strcat(out "/hi_explicit_bottom_trial_fragment.txt"))
  expected='(((18.7577 54.2236) 0.9302016) ((18.7018 54.2403) -0.1016011) ((18.6002 54.1388) 0.1016011) ((18.6002 49.3658) 0.0) ((18.6764 49.2896) 0.0) ((18.7482 49.2598) 0.1015894) ((18.8498 49.3614) -0.1015894) ((18.8498 54.1701) 0.0))
  axlDBRefreshId(nil)
  matches=setof(x axlDBGetShapes("ETCH/BOTTOM") x->net && equal(x->net->name "GND") && x->shapeBoundary && hiXYClose(car(x->bBox) list(18.6002 49.2599)) && hiXYClose(cadr(x->bBox) list(18.8498 54.2404)))
  unless(length(matches)==1 error("Explicit authorized BOTTOM island not unique\\n")) s=car(matches) mother=s->shapeBoundary
  unless(equal(mother->layer "BOUNDARY/BOTTOM") && mother->shapeIsBoundary error("Explicit orphan is not application BOTTOM dynamicgenerated\\n"))
  graph=gConnectedObjects(s) allterm=hiAllVias()
  foreach(c axlDBGetDesign()->components foreach(p c->symbol->pins allterm=cons(p allterm)))
  when(exists(p allterm member(p graph)) error("Refuse BOTTOM island removal with real pin/via\\n"))
  poly=car(axlPolyFromDB(s)) actual=poly->vertices ok=length(actual)==length(expected)
  when(ok for(k 0 length(expected)-1 unless(hiXYClose(car(nth(k actual)) car(nth(k expected))) && abs(cadr(nth(k actual))-cadr(nth(k expected)))<0.00001 ok=nil)))
  unless(ok && abs(poly->area-1.228451)<0.00001 error("Explicit authorized BOTTOM island real arc polygon differs\\n"))
  fprintf(f "EXPLICIT_STAGE_BOTTOM_ISLAND_ID=B018_BOTTOM_NORTH_FRAGMENT_01\\nPRE_ACTUAL=%L\\nMOTHER_BEFORE=%L\\nAREA=%L\\nREAL_ARC_POLYGON=%L\\n" s->?? mother->?? poly->area actual)
  ret=axlDBCreateVoid(mother poly) unless(ret error("Cannot create authorized BOTTOM fragment permanentvoid\\n"))
  fprintf(f "NEW_STAGE_VOID=%L\\nORIGINAL_APPLICATION_BOUNDARY_AND_EXISTING_VOIDS_RETAINED=t\\n" ret->??)
  unless(equal(axlShapeDynamicUpdate(mother t) 0) error("Cannot forcefill BOTTOM after stage void\\n")) close(f) t))
'''
(R/'scripts/batchHI_dynamic_void_and_ground_trial_v4.il').write_text(s,encoding='ascii');comp=(R/'scripts/compile_batchHI_v36.py').read_text().replace('batchHI_dynamic_void_and_ground_trial_v3.il','batchHI_dynamic_void_and_ground_trial_v4.il');(R/'scripts/compile_batchHI_v37.py').write_text(comp,encoding='utf8')
v='2L';d=json.loads((R/f'batches/TOP_trial_{v}_b018_PRE_ALL69_DRC_PENDING_try04.json').read_text());cfg=json.loads((R/f'native_work/b018_{v}_try04/guard_configuration.json').read_text());d['explicitAdditionalBottomStageVoid']={'id':'B018_BOTTOM_NORTH_FRAGMENT_01','sourceActualLog':'logs/TOP_trial_2L_b018_PRE_ALL69_DRC_PENDING_try04','bbox':[[18.6002,49.2599],[18.8498,54.2404]],'area':1.228451,'authorization':'Root explicit message permits this one generated no-real-pin/via island only, preserve BOTTOM boundary and prior voids'};work=R/f'native_work/b018_{v}_try05';work.mkdir(exist_ok=False);scratch=work/'input.brd';scratch.write_bytes(Path(d['inputBoardIdentity']['board']).read_bytes());d['executionGuard']['scratchWritableWorkingCopy']=str(scratch);tag=f'TOP_trial_{v}_b018_PRE_ALL69_DRC_PENDING_try05';p=R/f'batches/{tag}.json';p.write_text(json.dumps(d,indent=2));subprocess.run([sys.executable,str(R/'scripts/compile_batchHI_v37.py'),'--plan',str(p),'--variant',v,'--tag',tag],check=True);mp=R/f'scripts/{tag}_compiled.json';m=json.loads(mp.read_text());cfg.update(tag=tag,scratchWritableWorkingCopy=str(scratch),scratchSHA256=sha(scratch),plan=str(p),planSHA256=sha(p),compiledMetadata=str(mp),compiledMetadataSHA256=sha(mp),script=m['script'],scriptSHA256=sha(Path(m['script'])),log=m['log']);(work/'guard_configuration.json').write_text(json.dumps(cfg,indent=2))
