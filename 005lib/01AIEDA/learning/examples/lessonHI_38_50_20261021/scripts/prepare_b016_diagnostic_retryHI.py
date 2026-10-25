from pathlib import Path
import json,hashlib,subprocess,sys
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
s=(R/'scripts/batchHI_exact_ripup_v2.il').read_text().replace('    unless(equal(expected after) error(','''    foreach(sig car(expected) unless(member(sig car(after)) fprintf(f "HI_NON_TARGET_LINE_SIGNATURE_BEFORE_ONLY=%s\\n" sig)))
    foreach(sig car(after) unless(member(sig car(expected)) fprintf(f "HI_NON_TARGET_LINE_SIGNATURE_AFTER_ONLY=%s\\n" sig)))
    foreach(sig cadr(expected) unless(member(sig cadr(after)) fprintf(f "HI_NON_TARGET_VIA_SIGNATURE_BEFORE_ONLY=%s\\n" sig)))
    foreach(sig cadr(after) unless(member(sig cadr(expected)) fprintf(f "HI_NON_TARGET_VIA_SIGNATURE_AFTER_ONLY=%s\\n" sig)))
    drain(f)
    unless(equal(expected after) error(''');(R/'scripts/batchHI_exact_ripup_v3_diagnostic.il').write_text(s,encoding='ascii')
s=(R/'scripts/compile_batchHI_v29.py').read_text().replace('batchHI_exact_ripup_v2.il','batchHI_exact_ripup_v3_diagnostic.il');(R/'scripts/compile_batchHI_v30.py').write_text(s,encoding='utf8')
# A reusable retry preparation tool never replaces any work input, log, candidate, or snapshot.
s='''from pathlib import Path
import argparse,json,hashlib,subprocess,sys
R=Path(r'D:\\001DIY\\005lib\\01AIEDA\\learning\\examples\\lessonHI_38_50_20261021');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper();P=argparse.ArgumentParser();P.add_argument('--variant',required=True);P.add_argument('--try-number',required=True);P.add_argument('--compiler',required=True);a=P.parse_args();v=a.variant;t=a.try_number;assert v in ['2L','4L'] and t.isdigit();old=json.loads((R/f'native_work/b016_{v}_try01/guard_configuration.json').read_text());work=R/f'native_work/b016_{v}_try{t}';work.mkdir(exist_ok=False);scratch=work/'input.brd'
with scratch.open('xb') as f:f.write(Path(old['scratchWritableWorkingCopy']).read_bytes())
plan=json.loads(Path(old['plan']).read_text());plan['executionGuard']['scratchWritableWorkingCopy']=str(scratch);plan['executionGuard']['inputSHA256']=sha(scratch);tag=f'clearance_remaining_{v}_b016_DRC_PENDING_try{t}';dest=R/f'batches/{tag}.json';dest.write_text(json.dumps(plan,indent=2),encoding='utf8');subprocess.run([sys.executable,str(R/f'scripts/compile_batchHI_v{a.compiler}.py'),'--plan',str(dest),'--variant',v,'--tag',tag],check=True);meta=R/f'scripts/{tag}_compiled.json';m=json.loads(meta.read_text());cfg=dict(old,tag=tag,scratchWritableWorkingCopy=str(scratch),scratchSHA256=sha(scratch),compiledMetadata=str(meta),compiledMetadataSHA256=sha(meta),plan=str(dest),planSHA256=sha(dest),script=m['script'],scriptSHA256=sha(Path(m['script'])),log=m['log']);(work/'guard_configuration.json').write_text(json.dumps(cfg,indent=2),encoding='utf8')
''';(R/'scripts/prepare_b016_retryHI.py').write_text(s,encoding='utf8')
s=(R/'scripts/launch_b016_guardedHI_v1.py').read_text().replace("assert a.try_suffix in ['_try01']","assert a.try_suffix.startswith('_try') and a.try_suffix[4:].isdigit()");(R/'scripts/launch_b016_guardedHI_v2.py').write_text(s,encoding='utf8')
subprocess.run([sys.executable,str(R/'scripts/prepare_b016_retryHI.py'),'--variant','2L','--try-number','02','--compiler','30'],check=True)