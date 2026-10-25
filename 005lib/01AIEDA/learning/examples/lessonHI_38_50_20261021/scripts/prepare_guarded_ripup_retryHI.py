from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
s=(R/'scripts/compile_batchHI_v21.py').read_text()
s=s.replace('proofs=[]\nplaced_moves=', '''proofs=[]
delete_prefix=[]
for op in data.get('operations',[]):
 if op['type'] not in ['deleteVia','deleteSegment']:break
 delete_prefix.append(op)
assert len(delete_prefix)==sum(o['type'] in ['deleteVia','deleteSegment'] for o in data.get('operations',[])), 'All exact deletes must be initial prefix'
delete_done=False
placed_moves=''')
s=s.replace(" if typ=='deleteVia':statements.append", """ if typ in ['deleteVia','deleteSegment'] and delete_prefix:
  if not delete_done:
   rows=[]
   for d in delete_prefix:
    if d['type']=='deleteVia':rows.append('list('+q(d['type'])+' '+q(d['id'])+' '+q(d['net'])+' "" '+pt(d['xy'])+' '+q(d['padstack'])+')')
    else:rows.append('list('+q(d['type'])+' '+q(d['id'])+' '+q(d['net'])+' '+q(d['layer'])+' '+points(d['points'])+' '+num(d['width'])+')')
   statements.append('hiDeleteExactBatch(f list('+' '.join(rows)+'))');delete_done=True
  continue
 if typ=='deleteVia':statements.append""")
s=s.replace("R/'scripts/batchHI_shapes_v3.il',il]", "R/'scripts/batchHI_shapes_v3.il',R/'scripts/batchHI_exact_ripup_v2.il',il]")
(R/'scripts/compile_batchHI_v22.py').write_text(s,encoding='utf8')
# New immutable retry work inputs/compilation; previous failed attempt stays intact.
import json,hashlib,stat,subprocess,sys
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
for v in ['2L','4L']:
 old=json.loads((R/f'native_work/source_b015_{v}/guard_configuration.json').read_text())
 work=R/f'native_work/source_b015_{v}_try02';work.mkdir(exist_ok=False)
 scratch=work/'input.brd'
 with scratch.open('xb') as f:f.write(Path(old['scratchReadonlyInput']).read_bytes())
 scratch.chmod(stat.S_IREAD)
 plan=json.loads(Path(old['plan']).read_text());plan['executionGuard']['scratchReadonlyInput']=str(scratch);plan['executionGuard']['inputSHA256']=sha(scratch)
 plan['exactRipupStrategy']='Official axlDeleteObject(list prebound unique original-net line/via dbids) atomically, transaction rollback on any changed non-target manual line(net/layer/points/width) or via(net/xy/pad) signature. Avoid native intermediate disconnected segment relabeling demonstrated in failed attempt.'
 dest=R/f'batches/source_service_{v}_b015_guarded_try02.json';dest.write_text(json.dumps(plan,indent=2),encoding='utf8')
 tag=f'source_service_{v}_b015_guarded_try02'
 subprocess.run([sys.executable,str(R/'scripts/compile_batchHI_v22.py'),'--plan',str(dest),'--variant',v,'--tag',tag],check=True)
 meta=R/f'scripts/{tag}_compiled.json';m=json.loads(meta.read_text())
 cfg=dict(old,tag=tag,scratchReadonlyInput=str(scratch),scratchSHA256=sha(scratch),compiledMetadata=str(meta),compiledMetadataSHA256=sha(meta),plan=str(dest),planSHA256=sha(dest),script=m['script'],scriptSHA256=sha(Path(m['script'])),log=m['log'])
 (work/'guard_configuration.json').write_text(json.dumps(cfg,indent=2),encoding='utf8')
s=(R/'scripts/launch_source_guardedHI.py').read_text().replace("a=A.parse_args();work=R/f'native_work/source_b015_{a.variant}'", "A.add_argument('--try-suffix',default='');a=A.parse_args();assert a.try_suffix in ['', '_try02'];work=R/f'native_work/source_b015_{a.variant}{a.try_suffix}'")
(R/'scripts/launch_source_guardedHI_v2.py').write_text(s,encoding='utf8')
