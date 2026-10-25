from pathlib import Path
import json,argparse,shutil,hashlib
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
P=argparse.ArgumentParser();P.add_argument('--tag',required=True);P.add_argument('--plan');P.add_argument('--compiled');a=P.parse_args()
helpers=['de_board_read.il','build29_v2.il','read29.il','extra_read29.il','specific_proof.il','more28.il','mechanical28.il','correction.il','inventoryG.il','placementG.il','local_copperG_v2.il']
loads=[R/'source'/x for x in helpers]+[R/'scripts/network_inventoryHI_v2.il',R/'scripts/batchHI.il',R/'scripts/batchHI_extended.il',R/'scripts/batchHI_shapes_v3.il',R/'scripts/extraReadHI.il']
h='set NOCONFIRM\n'+''.join('skill errset(load('+json.dumps(p.as_posix())+') t)\n' for p in loads)
out=(R/'logs'/a.tag).as_posix()
captures=''
captures+='skill errset(axlDRCUpdate(t) t)\n'
captures+='skill errset(gSnapshot("'+out+'" "'+(R/'library').as_posix()+'") t)\n'
captures+='skill errset(hiNetworkInventory("'+out+'") t)\n'
captures+='skill errset(hiExtraRead("'+out+'") t)\n'
captures+='skill errset(hiShapeBoundaryRead("'+out+'") t)\n'
captures+='skill errset(hiRouteRoles("'+out+'") t)\n'
captures+='skill errset(hiUSBMaskRead("'+out+'") t)\n'
captures+='skill errset(hiBranchAudit("'+out+'") t)\n'
captures+='skill errset(hiReferenceCoverageRead("'+out+'" 0.1) t)\n'
if a.plan:
 d=json.loads(Path(a.plan).read_text(encoding='utf8'))
 il='procedure(hiReadbackProofs()\n let((f)\n  f=outfile("'+out+'/hi_reopen_endpoint_proofs.txt")\n  hiRegistry=nil\n  unwindProtect(progn(\n   axlDBControl(\'drcEnable nil)\n'
 if a.compiled:
  meta=json.loads(Path(a.compiled).read_text(encoding='utf8'))
  defs=meta['endpointDefinitions']
  def pt(x):return 'list('+' '.join(str(float(v)) for v in x)+')'
  il+='  hiNodeDefinitions=list('+' '.join('list('+json.dumps(k)+' '+json.dumps(v[0])+' '+json.dumps(v[1])+' '+pt(v[2])+' '+json.dumps(v[3])+')' for k,v in defs.items())+')\n'
 for op in d.get('operations',[]):
  if op['type']=='shape':
   if op.get('dynamic') and isinstance(op.get('polygon'),list):
    poly=op['polygon'];bbox=[[min(p[i] for p in poly) for i in range(2)],[max(p[i] for p in poly) for i in range(2)]]
    il+='  hiBindExistingShapeByBBox(f '+json.dumps(op['id'])+' '+json.dumps(op['net'])+' '+json.dumps(op['layer'])+' list('+ ' '.join(pt(v) for v in bbox)+'))\n'
   else:
    fn='hiBindExistingShape' if op.get('dynamic') else 'hiBindExistingStaticShape'
    il+='  '+fn+'(f '+json.dumps(op['id'])+' '+json.dumps(op['net'])+' '+json.dumps(op['layer'])+')\n'
 for op in d.get('operations',[]):
  if op['type']=='via':
   il+='  hiBindExistingVia(f '+json.dumps(op['id'])+' '+json.dumps(op['net'])+' list('+' '.join(repr(float(x)) for x in op['xy'])+') '+json.dumps(op['padstack'])+')\n'
 for op in d.get('operations',[]):
  if op.get('from') and op.get('to'):il+='  hiProof(f '+json.dumps(op['from'])+' '+json.dumps(op['to'])+' t)\n'
 for p in d.get('proofs',[]):
  il+='  hiProof(f '+json.dumps(p['from'])+' '+json.dumps(p['to'])+' '+('t' if p.get('connected',True) else 'nil')+')\n'
 for p in d.get('postChecks',[]):
  if p['type']=='hseIsolation':
   il+='  hiHSEIsolationChallengeGraph('+json.dumps(out)+' '+pt(p['anchorXY'])+' '+json.dumps(p['localLayer'])+' list('+' '.join(pt(x) for x in p['guardPoints'])+'))\n'
  else:raise ValueError(p['type'])
 il+='  t) progn(axlDBControl(\'drcEnable t) fprintf(f "HI_READBACK_UNWIND_DRC_RESTORED=%L\\n" axlDBControl(\'drcEnable))))\n'
 il+='  fprintf(f "HI_REOPEN_ALL_ENDPOINTS_COMPLETE\\n") close(f) t))\n'
 (R/f'scripts/{a.tag}.il').write_text(il,encoding='ascii')
 h+='skill errset(load("'+(R/f'scripts/{a.tag}.il').as_posix()+'") t)\n'
 h+='skill errset(hiReadbackProofs() t)\n'
h+=captures
h+='quit\nfillin "yes"\n'
snap=R/'source/readback_snapshots'/a.tag;snap.mkdir(parents=True,exist_ok=False)
source_files=loads+([R/f'scripts/{a.tag}.il'] if a.plan else [])
manifest=[]
for i,src in enumerate(source_files):
 dest=snap/(str(i).zfill(2)+'_'+src.name);shutil.copyfile(src,dest)
 h=h.replace(src.as_posix(),dest.as_posix())
 manifest.append({'source':str(src),'immutableSnapshot':str(dest),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest().upper()})
(snap/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
(R/f'scripts/{a.tag}.scr').write_text(h,encoding='ascii');print(R/f'scripts/{a.tag}.scr')
