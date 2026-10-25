from pathlib import Path
import json,hashlib,stat,subprocess,sys
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
p=R/'scripts/batchHI_exact_ripup_v2.il';s=p.read_text();s=s.replace('drain(f) drain(f) drain(f) drain(f)','drain(f)').replace('drain(f) drain(f)','drain(f)');s=s.replace('object=%L parent=%L\\n" id type net selected selected->objType','object=%L originalDescriptor=%L\\n" id type net selected spec');s=s.replace('fprintf(f "HI_EXACT_NATIVE_LIST_DELETE_RETURNED\\n") drain(f)\n    fprintf(f "HI_EXACT_NATIVE_LIST_DELETE_RETURNED\\n") drain(f)','fprintf(f "HI_EXACT_NATIVE_LIST_DELETE_RETURNED\\n") drain(f)');p.write_text(s,encoding='ascii')
for v in ['2L','4L']:
 old=json.loads((R/f'native_work/source_b015_{v}_try02/guard_configuration.json').read_text())
 work=R/f'native_work/source_b015_{v}_try03';work.mkdir(exist_ok=False);scratch=work/'input.brd'
 with scratch.open('xb') as f:f.write(Path(old['scratchReadonlyInput']).read_bytes())
 scratch.chmod(stat.S_IREAD)
 plan=json.loads(Path(old['plan']).read_text());plan['executionGuard']['scratchReadonlyInput']=str(scratch);plan['executionGuard']['inputSHA256']=sha(scratch)
 dest=R/f'batches/source_service_{v}_b015_guarded_try03.json';dest.write_text(json.dumps(plan,indent=2),encoding='utf8');tag=f'source_service_{v}_b015_guarded_try03'
 subprocess.run([sys.executable,str(R/'scripts/compile_batchHI_v22.py'),'--plan',str(dest),'--variant',v,'--tag',tag],check=True)
 meta=R/f'scripts/{tag}_compiled.json';m=json.loads(meta.read_text());cfg=dict(old,tag=tag,scratchReadonlyInput=str(scratch),scratchSHA256=sha(scratch),compiledMetadata=str(meta),compiledMetadataSHA256=sha(meta),plan=str(dest),planSHA256=sha(dest),script=m['script'],scriptSHA256=sha(Path(m['script'])),log=m['log']);(work/'guard_configuration.json').write_text(json.dumps(cfg,indent=2),encoding='utf8')
s=(R/'scripts/launch_source_guardedHI_v2.py').read_text(encoding='utf-8-sig');s=s.replace("['', '_try02']","['', '_try02', '_try03']");(R/'scripts/launch_source_guardedHI_v3.py').write_text(s,encoding='utf8')
