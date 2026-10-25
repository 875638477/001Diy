from pathlib import Path
import json,argparse
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
P=argparse.ArgumentParser();P.add_argument('--tag',required=True);P.add_argument('--plan');P.add_argument('--compiled');a=P.parse_args()
helpers=['de_board_read.il','build29_v2.il','read29.il','extra_read29.il','specific_proof.il','more28.il','mechanical28.il','correction.il','inventoryG.il','placementG.il','local_copperG_v2.il']
loads=[R/'source'/x for x in helpers]+[R/'scripts/network_inventoryHI_v2.il',R/'scripts/batchHI.il',R/'scripts/batchHI_extended.il',R/'scripts/batchHI_shapes_v3.il',R/'scripts/extraReadHI.il']
h='set NOCONFIRM\n'+''.join('skill errset(load('+json.dumps(p.as_posix())+') t)\n' for p in loads)
out=(R/'logs'/a.tag).as_posix()
h+='skill errset(axlDRCUpdate(t) t)\n'
h+='skill errset(gSnapshot("'+out+'" "'+(R/'library').as_posix()+'") t)\n'
h+='skill errset(hiNetworkInventory("'+out+'") t)\n'
h+='skill errset(hiExtraRead("'+out+'") t)\n'
h+='skill errset(hiShapeBoundaryRead("'+out+'") t)\n'
h+='skill errset(hiRouteRoles("'+out+'") t)\n'
if a.plan:
 d=json.loads(Path(a.plan).read_text(encoding='utf8'))
 il='procedure(hiReadbackProofs()\n let((f)\n  f=outfile("'+out+'/hi_reopen_endpoint_proofs.txt")\n  hiRegistry=nil\n'
 if a.compiled:
  meta=json.loads(Path(a.compiled).read_text(encoding='utf8'))
  defs=meta['endpointDefinitions']
  def pt(x):return 'list('+' '.join(str(float(v)) for v in x)+')'
  il+='  hiNodeDefinitions=list('+' '.join('list('+json.dumps(k)+' '+json.dumps(v[0])+' '+json.dumps(v[1])+' '+pt(v[2])+' '+json.dumps(v[3])+')' for k,v in defs.items())+')\n'
 for op in d.get('operations',[]):
  if op['type']=='shape':
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
   il+='  hiHSEIsolationChallenge('+json.dumps(out)+' '+pt(p['anchorXY'])+' '+json.dumps(p['localLayer'])+' list('+' '.join(pt(x) for x in p['guardPoints'])+'))\n'
  else:raise ValueError(p['type'])
 il+='  fprintf(f "HI_REOPEN_ALL_ENDPOINTS_COMPLETE\\n") close(f) t))\n'
 (R/f'scripts/{a.tag}.il').write_text(il,encoding='ascii')
 h+='skill errset(load("'+(R/f'scripts/{a.tag}.il').as_posix()+'") t)\n'
 h+='skill errset(hiReadbackProofs() t)\n'
h+='quit\nfillin "yes"\n'
(R/f'scripts/{a.tag}.scr').write_text(h,encoding='ascii');print(R/f'scripts/{a.tag}.scr')
