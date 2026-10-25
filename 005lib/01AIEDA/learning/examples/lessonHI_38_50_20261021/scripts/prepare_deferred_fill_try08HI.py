from pathlib import Path
import json,hashlib,stat,subprocess,sys
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
s=(R/'scripts/compile_batchHI_v24.py').read_text();s=s.replace(" elif typ=='replaceShape':", " elif typ=='removeConstructionShape':statements.append(f'hiRemoveExactConstructionShape(f {q(ident)} {q(net)} {q(op[\"layer\"])} {points(op[\"polygon\"])} '+('t' if op.get('dynamic',False) else 'nil')+')')\n elif typ=='replaceShape':")
(R/'scripts/compile_batchHI_v25.py').write_text(s,encoding='utf8')
for v in ['2L','4L']:
 old=json.loads((R/f'native_work/source_b015_{v}_try07/guard_configuration.json').read_text());work=R/f'native_work/source_b015_{v}_try08';work.mkdir(exist_ok=False);scratch=work/'input.brd'
 with scratch.open('xb') as f:f.write(Path(old['scratchReadonlyInput']).read_bytes())
 scratch.chmod(stat.S_IREAD);plan=json.loads(Path(old['plan']).read_text());plan['executionGuard']['scratchReadonlyInput']=str(scratch);plan['executionGuard']['inputSHA256']=sha(scratch)
 deferred=[]
 for i,o in enumerate(plan['operations']):
  if o['id']=='HI_GPIO_TOP_PATCH_RECLIP':
   assert o['type']=='replaceShape' and o['dynamic'] and o['net']=='GND' and o['layer']=='TOP'
   deferred.append({'type':'shape','id':o['id']+'_RESTORE_AFTER_NEW_SIGNAL_COPPER','net':'GND','layer':'TOP','polygon':o['newPolygon'],'dynamic':True,'voids':o.get('voids',[])})
   plan['operations'][i]={'type':'removeConstructionShape','id':o['id']+'_DEFER_NEW_FILL','net':'GND','layer':'TOP','polygon':o['oldPolygon'],'dynamic':True,'reason':'Defer approved reclip fill to after signal creation; frozen expected final polygon restored before full DRC and all proofs.'}
 plan['operations'].extend(deferred);plan['dynamicConstructionDefer']={'variant':v,'deferredBoundaryCount':len(deferred),'restoredOperations':deferred,'actualFailureGeometryEvidence':str(R/'engineering_power/readouts/actual_BOOT_failure07_geometry.json'),'evidenceSHA256':sha(R/'engineering_power/readouts/actual_BOOT_failure07_geometry.json'),'finalFullFillDrcPhysicalHseGatesUnchanged':True}
 dest=R/f'batches/source_service_{v}_b015_guarded_try08.json';dest.write_text(json.dumps(plan,indent=2),encoding='utf8');tag=f'source_service_{v}_b015_guarded_try08';subprocess.run([sys.executable,str(R/'scripts/compile_batchHI_v25.py'),'--plan',str(dest),'--variant',v,'--tag',tag],check=True)
 meta=R/f'scripts/{tag}_compiled.json';m=json.loads(meta.read_text());cfg=dict(old,tag=tag,scratchReadonlyInput=str(scratch),scratchSHA256=sha(scratch),compiledMetadata=str(meta),compiledMetadataSHA256=sha(meta),plan=str(dest),planSHA256=sha(dest),script=m['script'],scriptSHA256=sha(Path(m['script'])),log=m['log']);(work/'guard_configuration.json').write_text(json.dumps(cfg,indent=2),encoding='utf8')
s=(R/'scripts/launch_source_guardedHI_v7.py').read_text(encoding='utf-8-sig').replace("['', '_try02', '_try03', '_try04', '_try05', '_try06', '_try07']","['', '_try02', '_try03', '_try04', '_try05', '_try06', '_try07', '_try08']");(R/'scripts/launch_source_guardedHI_v8.py').write_text(s,encoding='utf8')
