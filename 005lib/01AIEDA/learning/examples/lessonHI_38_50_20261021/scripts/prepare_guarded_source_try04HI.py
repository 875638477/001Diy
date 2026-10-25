from pathlib import Path
import json,hashlib,stat,subprocess,sys
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
s=(R/'scripts/compile_batchHI_v22.py').read_text();s=s.replace("R/'scripts/batchHI_exact_ripup_v2.il',il]","R/'scripts/batchHI_exact_ripup_v2.il',R/'scripts/batchHI_route_probe_v1.il',il]");(R/'scripts/compile_batchHI_v23.py').write_text(s,encoding='utf8')
for v in ['2L','4L']:
 old=json.loads((R/f'native_work/source_b015_{v}_try03/guard_configuration.json').read_text());work=R/f'native_work/source_b015_{v}_try04';work.mkdir(exist_ok=False);scratch=work/'input.brd'
 with scratch.open('xb') as f:f.write(Path(old['scratchReadonlyInput']).read_bytes())
 scratch.chmod(stat.S_IREAD);plan=json.loads(Path(old['plan']).read_text());plan['executionGuard']['scratchReadonlyInput']=str(scratch);plan['executionGuard']['inputSHA256']=sha(scratch);plan['nativeConstructionDiagnostic']='BOOT0 long path built in reverse from physicalR28.1 at identical geometric union to distinguish first-touch and pad reentry; no engineering coordinates or rules altered. Every created path native net logged.'
 dest=R/f'batches/source_service_{v}_b015_guarded_try04.json';dest.write_text(json.dumps(plan,indent=2),encoding='utf8');tag=f'source_service_{v}_b015_guarded_try04';subprocess.run([sys.executable,str(R/'scripts/compile_batchHI_v23.py'),'--plan',str(dest),'--variant',v,'--tag',tag],check=True)
 meta=R/f'scripts/{tag}_compiled.json';m=json.loads(meta.read_text());cfg=dict(old,tag=tag,scratchReadonlyInput=str(scratch),scratchSHA256=sha(scratch),compiledMetadata=str(meta),compiledMetadataSHA256=sha(meta),plan=str(dest),planSHA256=sha(dest),script=m['script'],scriptSHA256=sha(Path(m['script'])),log=m['log']);(work/'guard_configuration.json').write_text(json.dumps(cfg,indent=2),encoding='utf8')
s=(R/'scripts/launch_source_guardedHI_v3.py').read_text(encoding='utf-8-sig').replace("['_none_']","['_none_']").replace("['', '_try02', '_try03']","['', '_try02', '_try03', '_try04']");(R/'scripts/launch_source_guardedHI_v4.py').write_text(s,encoding='utf8')
