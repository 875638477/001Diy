from pathlib import Path
import json,hashlib,stat,subprocess,sys
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
for v in ['2L','4L']:
 old=json.loads((R/f'native_work/source_b015_{v}_try06/guard_configuration.json').read_text());work=R/f'native_work/source_b015_{v}_try07';work.mkdir(exist_ok=False);scratch=work/'input.brd'
 with scratch.open('xb') as f:f.write(Path(old['scratchReadonlyInput']).read_bytes())
 scratch.chmod(stat.S_IREAD);plan=json.loads(Path(old['plan']).read_text());plan['executionGuard']['scratchReadonlyInput']=str(scratch);plan['executionGuard']['inputSHA256']=sha(scratch)
 op=next(o for o in plan['operations'] if o['id']=='RIGHT_BOOT_DIRECT_TOP');before=json.loads(json.dumps(op));op['points']=[[46.8,27.65],[47.27,27.18],[52.8984,27.18],[52.8984,28]];op['purpose']='f28 reviewed BOOT endpoint simplification: remove pad-internal foldback and satisfy unchanged GND .3 spacing, actual nearest .3135; native revalidation required.'
 evidence=R/'engineering_power/readouts/BOOT_endpoint_simplification_02.json';plan['bootOpAdapterCorrection']={'before':before,'after':op,'evidence':str(evidence),'evidenceSHA256':sha(evidence),'frozenEngineeringInputsUnchanged':True}
 dest=R/f'batches/source_service_{v}_b015_guarded_try07.json';dest.write_text(json.dumps(plan,indent=2),encoding='utf8');tag=f'source_service_{v}_b015_guarded_try07';subprocess.run([sys.executable,str(R/'scripts/compile_batchHI_v24.py'),'--plan',str(dest),'--variant',v,'--tag',tag],check=True)
 meta=R/f'scripts/{tag}_compiled.json';m=json.loads(meta.read_text());cfg=dict(old,tag=tag,scratchReadonlyInput=str(scratch),scratchSHA256=sha(scratch),compiledMetadata=str(meta),compiledMetadataSHA256=sha(meta),plan=str(dest),planSHA256=sha(dest),script=m['script'],scriptSHA256=sha(Path(m['script'])),log=m['log']);(work/'guard_configuration.json').write_text(json.dumps(cfg,indent=2),encoding='utf8')
s=(R/'scripts/launch_source_guardedHI_v6.py').read_text(encoding='utf-8-sig').replace("['', '_try02', '_try03', '_try04', '_try05', '_try06']","['', '_try02', '_try03', '_try04', '_try05', '_try06', '_try07']");(R/'scripts/launch_source_guardedHI_v7.py').write_text(s,encoding='utf8')
