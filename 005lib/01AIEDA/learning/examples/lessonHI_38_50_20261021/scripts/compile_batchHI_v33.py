from pathlib import Path
import json,hashlib,argparse,shutil
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
P=argparse.ArgumentParser();P.add_argument('--plan',required=True);P.add_argument('--variant',choices=['4L','2L'],required=True);P.add_argument('--tag',required=True)
a=P.parse_args();planpath=Path(a.plan);data=json.loads(planpath.read_text(encoding='utf8'));tag=a.tag
assert planpath.resolve().is_relative_to(R.resolve())
def q(s):return json.dumps(s,ensure_ascii=True)
def num(x):return repr(float(x))
def pt(p):assert len(p)==2;return 'list('+num(p[0])+' '+num(p[1])+')'
def points(pp):return 'list('+' '.join(pt(x) for x in pp)+')'
def quotedValue(v):
 if isinstance(v,list):return 'list('+' '.join(quotedValue(x) for x in v)+')'
 if isinstance(v,bool):return 't' if v else 'nil'
 if isinstance(v,(int,float)):return num(v)
 return q(v)
def terminal(x):
 if isinstance(x,dict):return x['ref']+'.'+str(x['pin'])
 return x
out=R/f'logs/{tag}';board=R/f'native/HI_{a.variant}_{tag}.brd';il=R/f'scripts/{tag}.il'
if data.get('outputBoard'):
 board=Path(data['outputBoard']).resolve()
 assert board.is_relative_to((R/'native_candidates').resolve()) and not board.exists(), 'Guarded SaveAs must target a brand new task candidate'
known={op['id']:op for op in data.get('operations',[])}
known_pads={p.stem.upper() for p in (R/'library').rglob('*.pad')}
for op in data.get('operations',[]):
 if op['type']=='via':
  assert op['padstack'].upper() in known_pads, 'Via padstack must be concrete and present in isolated library: '+op['padstack']
node_defs={}
for op in data.get('operations',[]):
 if op['type']=='via':node_defs[op['id']]=(op['net'],'TOP',op['xy'],'via')
 if op['type']=='route':node_defs[op['id']]=(op['net'],op['layer'],op['points'][0],'point')
for alias in data.get('aliases',[]):node_defs[alias['id']]=(alias['net'],alias.get('layer','TOP'),alias['xy'],alias.get('type','point'))
for op in data.get('operations',[]):
 if op['type']!='route':continue
 for field,xy in [('from',op['points'][0]),('to',op['points'][-1])]:
  name=terminal(op.get(field))
  if not name or '.' in name or name in node_defs or name in known:continue
  if name.startswith('NODE_'):kind='point'
  elif name.startswith('G31_') or name.startswith('V_'):kind='via'
  else:raise ValueError('Unknown named endpoint needs explicit alias: '+name)
  node_defs[name]=(op['net'],op['layer'],xy,kind)
defs='list('+' '.join('list('+q(n)+' '+q(v[0])+' '+q(v[1])+' '+pt(v[2])+' '+q(v[3])+')' for n,v in node_defs.items())+')'
statements=['hiDeferredReferences=nil','hiReferenceParamsBefore=nil','hiRegistry=nil','hiNodeDefinitions='+defs,'hiDiagnosticOutput='+q(out.as_posix()),'hiDiagnosticLibrary='+q((R/'library').as_posix())]
statements.append('axlSetVariable("padpath" list('+q((R/'library').as_posix())+'))')
statements.append('axlSetVariable("psmpath" list('+q((R/'library').as_posix())+'))')
for pad in sorted({o['padstack'] for o in data.get('operations',[]) if o['type']=='via'}):
 statements.append('unless(axlLoadPadstack('+q(pad)+') error("Cannot load isolated concrete via padstack\\n"))')
placement_statements=[]
placement_mode=data.get('placementSequence','BEFORE_OPERATIONS')
assert placement_mode in ['BEFORE_OPERATIONS','AFTER_INITIAL_DELETIONS','AFTER_SECOND_DELETIONS']
for p in data.get('placementChanges',[]):
 assert p.get('side','TOP')=='TOP'
 placement_statements.append(f'hiMove(f {q(p["ref"])} {pt(p["xy"])} {num(p["rotation"])})')
if placement_mode=='BEFORE_OPERATIONS':statements.extend(placement_statements)
for op in data.get('constraintOperations',[]):
 typ=op['type']
 if typ=='csetCopy':
  domain=op['domain'];assert domain in ['physical','spacing']
  vals='list('+' '.join('list(\''+k+' '+quotedValue(':'.join(v) if k=='vias' and isinstance(v,list) else v)+')' for k,v in op['values'].items())+')'
  statements.append(f'hiCSet(f \'{domain} {q(op["name"])} {q(op["copyFrom"])} {vals})')
  for layer,fields in op.get('layerValues',{}).items():
   for field,val in fields.items():statements.append(f'hiCSetLayerValue(f \'{domain} {q(op["name"])} {q(layer)} \'{field} {quotedValue(val)})')
 elif typ=='existingSpacingFields':
  vals='list('+' '.join('list(\''+k+' '+quotedValue(v)+')' for k,v in op['values'].items())+')'
  statements.append(f'hiSpacingFieldsUpdate(f {q(op["name"])} {vals})')
 elif typ=='existingSpacingLayerFields':
  vals='list('+' '.join('list('+q(layer)+' \''+k+' '+quotedValue(val)+')' for layer,fields in op['layerValues'].items() for k,val in fields.items())+')'
  statements.append(f'hiSpacingLayerFieldsUpdate(f {q(op["name"])} {vals})')
 elif typ=='ecsetCopy':
  vals='list('+' '.join('list(\''+k+' '+quotedValue(':'.join(v) if k=='vias' and isinstance(v,list) else v)+')' for k,v in op['values'].items())+')'
  statements.append(f'hiECSetCopy(f {q(op["name"])} {q(op["copyFrom"])} {vals} {q(op["pair"])})')
 elif typ=='netClass':
  statements.append(f'hiAssignNetClass(f {q(op["name"])} \'{op["domain"]} {q(op["cset"])} list('+ ' '.join(q(n) for n in op['nets'])+'))')
 elif typ=='region':
  assigns='list('+' '.join('list('+q(x['netClass'])+' \''+x['domain']+' '+q(x['cset'])+' '+(q(x['otherNetClass']) if x.get('otherNetClass') else 'nil')+')' for x in op['assignments'])+')'
  statements.append(f'hiRegion(f {q(op["id"])} {q(op["layer"])} {points(op["polygon"])} {assigns})')
 else:raise ValueError(typ)
proofs=[]
delete_prefix=[]
for op in data.get('operations',[]):
 if op['type'] not in ['deleteVia','deleteSegment']:break
 delete_prefix.append(op)
assert len(delete_prefix)==sum(o['type'] in ['deleteVia','deleteSegment'] for o in data.get('operations',[])), 'All exact deletes must be initial prefix'
delete_done=False
placed_moves=placement_mode=='BEFORE_OPERATIONS'
for op in data.get('operations',[]):
 typ=op['type'];ident=op['id'];net=op['net']
 if placement_mode=='AFTER_INITIAL_DELETIONS':
  if not placed_moves and typ not in ['deleteVia','deleteSegment']:
   if typ=='secondExactBatch':statements.extend(placement_statements);placed_moves=True
  elif placed_moves and typ in ['deleteVia','deleteSegment']:raise ValueError('All controlled deletions must be in initial prefix before placement changes')
 if typ in ['deleteVia','deleteSegment'] and delete_prefix:
  if not delete_done:
   rows=[]
   for d in delete_prefix:
    if d['type']=='deleteVia':rows.append('list('+q(d['type'])+' '+q(d['id'])+' '+q(d['net'])+' "" '+pt(d['xy'])+' '+q(d['padstack'])+')')
    else:rows.append('list('+q(d['type'])+' '+q(d['id'])+' '+q(d['net'])+' '+q(d['layer'])+' '+points(d['points'])+' '+num(d['width'])+')')
   statements.append('hiDeleteExactBatch(f list('+' '.join(rows)+'))');delete_done=True
  continue
 if typ=='deleteVia':statements.append(f'hiDeleteVia(f {q(ident)} {q(net)} {pt(op["xy"])} {q(op["padstack"])})')
 elif typ in ['secondExactBatch','exactBatch']:
  rows=[]
  for d in op['targets']:
   assert d['type']=='deleteSegment'
   rows.append('list('+q(d['type'])+' '+q(d['id'])+' '+q(d['net'])+' '+q(d['layer'])+' '+points(d['points'])+' '+num(d['width'])+')')
  statements.append('hiDeleteExactBatch(f list('+' '.join(rows)+'))')
  if typ=='secondExactBatch':statements.extend(placement_statements);placed_moves=True
 elif typ=='deferReference':statements.append(f'hiDeferReference(f {q(ident)} {q(op["layer"])} {points(op["polygon"])})')
 elif typ=='restoreReference':statements.append(f'hiRestoreReference(f {q(ident)})')
 elif typ=='verifyReferences':statements.append('hiVerifyReferences(f)')
 elif typ=='removeConstructionShape':statements.append(f'hiRemoveExactConstructionShape(f {q(ident)} {q(net)} {q(op["layer"])} {points(op["polygon"])} '+('t' if op.get('dynamic',False) else 'nil')+')')
 elif typ=='replaceShape':
  assert not op.get('oldHasArcs',False), 'Exact polygon replacement currently rejects arcs'
  vv='list('+' '.join(points(v) for v in op.get('voids',[]))+')'
  statements.append(f'hiReplaceExactShape(f {q(ident)} {q(net)} {q(op["layer"])} {points(op["oldPolygon"])} {points(op["newPolygon"])} '+('t' if op.get('dynamic',False) else 'nil')+' '+vv+')')
 elif typ=='replaceVoid':
  statements.append(f'hiReplaceExactVoid(f {q(ident)} {q(net)} {q(op["layer"])} {points(op["boundaryBBox"])} {points(op["oldPolygon"])} {points(op["newPolygon"])})')
 elif typ=='groundPointCheck':statements.append(f'hiGroundPointCheck(f {q(ident)} {pt(op["xy"])} '+('t' if op['topConnected'] else 'nil')+' '+('t' if op['bottomConnected'] else 'nil')+')')
 elif typ=='deleteSegment':statements.append(f'hiDeleteSegment(f {q(ident)} {q(net)} {q(op["layer"])} {points(op["points"])} {num(op["width"])})')
 elif typ=='bindShape':statements.append(f'hiBindExistingShape(f {q(ident)} {q(net)} {q(op["layer"])})')
 elif typ=='void':statements.append(f'hiVoid(f {q(op["shapeId"])} {points(op["polygon"])})')
 elif typ=='via':statements.append(f'hiVia(f {q(ident)} {q(net)} {pt(op["xy"])} {q(op["padstack"])})')
 elif typ=='shape':
  poly=q(op['polygon']) if isinstance(op['polygon'],str) else points(op['polygon'])
  vv='list('+' '.join(points(v) for v in op.get('voids',[]))+')'
  statements.append(f'hiShape(f {q(ident)} {q(net)} {q(op["layer"])} {poly} '+('t' if op.get('dynamic',False) else 'nil')+' '+vv+')')
 elif typ=='route':
  pp=op['points'];ww=op.get('widths',[op.get('width')]*(len(pp)-1))
  assert len(ww)==len(pp)-1 and all(w is not None and w>0 for w in ww)
  statements.append(f'hiRoute(f {q(ident)} {q(net)} {q(op["layer"])} {points(pp)} list('+' '.join(num(x) for x in ww)+'))')
  if op.get('from') and op.get('to'):proofs.append((terminal(op['from']),terminal(op['to']),True))
 else:raise ValueError(typ)
if not placed_moves:statements.extend(placement_statements)
if data.get('terminalContract'):
 contract='list('+' '.join('list('+q(x['ref'])+' '+q(x['pin'])+' '+(q(x['net']) if x['net'] else 'nil')+' '+q(x['padstack'])+')' for x in data['terminalContract'])+')'
 statements.append('hiPhysicalTerminalContract(f '+contract+')')
statements.append('hiVerifyExplicitPA10Restored(f)')
statements.append("axlDBControl('drcEnable t)")
statements.append('fprintf(f "HI_SCOPED_CHECK_MASTER_DRC_ENABLED=%L\\n" axlDBControl(\'drcEnable))')
for check in data.get('postChecks',[]):
 if check['type']=='hseIsolation':statements.append(f'hiHSEIsolationChallengeGraph({q(out.as_posix())} {pt(check["anchorXY"])} {q(check["localLayer"])} {points(check["guardPoints"])})')
 elif check['type']=='spacingFieldChallenge':statements.append(f'hiScopedSpacingFieldChallenge({q(out.as_posix())} {q(check["cset"])} {q(check["layer"])} \'{check["field"]} {q(check["net"])} {num(check["normal"])} {num(check["strict"])})')
 elif check['type']=='changedNetworks':statements.append('hiScopedChangedNetworks('+q(out.as_posix())+' list('+' '.join(q(n) for n in check['nets'])+'))')
 elif check['type']=='finiteViaLineChallenge':statements.append(f'hiFiniteViaLineChallenge({q(out.as_posix())} {q(check["cset"])} {q(check["layer"])} {q(check["net"])} {num(check["normal"])} {num(check["strict"])})')
 elif check['type']=='ccSpacingChallenge':statements.append(f'hiCCSpacingChallenge({q(out.as_posix())})')
 else:raise ValueError(check['type'])
for p in data.get('proofs',[]):proofs.append((terminal(p['from']),terminal(p['to']),p.get('connected',True)))
proofstr='list('+' '.join('list('+q(a)+' '+q(b)+' '+('t' if c else 'nil')+')' for a,b,c in proofs)+')'
code='procedure(hiBatchProgram()\n let((f)\n  f=outfile('+q((out/'hi_batch_execution.txt').as_posix())+')\n  fprintf(f "HI_BATCH_DRC_BEFORE=%L\\n" axlDBControl(\'drcEnable))\n  unwindProtect(\n   progn(\n    axlDBControl(\'drcEnable nil)\n    fprintf(f "HI_ASSEMBLY_ONLINE_DRC_TEMPORARILY_DISABLED=%L\\n" axlDBControl(\'drcEnable))\n    '+ '\n    '.join(statements)+'\n    t)\n   progn(\n    axlDBControl(\'drcEnable t)\n    fprintf(f "HI_UNWIND_DRC_RESTORED=%L\\n" axlDBControl(\'drcEnable))))\n  unless(axlDBControl(\'drcEnable) error("Final DRC must be enabled\\n"))\n  hiFinalize(f '+q(out.as_posix())+' '+q(board.as_posix())+' '+q((R/'library').as_posix())+' '+proofstr+')\n  t))\n'

il.write_text(code,encoding='ascii')
helpers=['de_board_read.il','build29_v2.il','read29.il','extra_read29.il','specific_proof.il','more28.il','mechanical28.il','correction.il','inventoryG.il','placementG.il','local_copperG_v2.il']
loads=[R/'source'/x for x in helpers]+[R/'scripts/network_inventoryHI_v2.il',R/'scripts/batchHI.il',R/'scripts/batchHI_extended.il',R/'scripts/batchHI_shapes_v3.il',R/'scripts/batchHI_exact_ripup_v4_explicit_PA10.il',R/'scripts/batchHI_route_probe_v1.il',R/'scripts/extraReadHI.il',R/'scripts/batchHI_b016_scoped_reference.il',R/'scripts/batchHI_intermediate_drc_pending.il',il]
snapshot=R/'source/batch_snapshots'/tag
snapshot.mkdir(parents=True,exist_ok=False)
input_records=[]
snaploads=[]
for i,orig in enumerate(loads):
 dest=snapshot/(f'{i:02d}_'+orig.name);shutil.copyfile(orig,dest);snaploads.append(dest)
 input_records.append({'source':str(orig),'snapshot':str(dest),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest().upper()})
(snapshot/'inputs_manifest.json').write_text(json.dumps(input_records,indent=2),encoding='utf8')
h='set NOCONFIRM\n'+''.join('skill errset(load('+q(p.as_posix())+') t)\n' for p in snaploads)
script=R/f'scripts/{tag}.scr';script.write_text(h+'skill errset(hiBatchProgram() t)\nskill errset(axlKillDesign() t)\nquit\n',encoding='ascii')
record={'plan':str(planpath),'planSHA256':hashlib.sha256(planpath.read_bytes()).hexdigest().upper(),'variant':a.variant,'batch':tag,'output':str(board),'log':str(out),'script':str(script),'proofCount':len(proofs),'operations':len(data.get('operations',[])),'endpointDefinitions':node_defs,'helperSnapshots':input_records}
(R/f'scripts/{tag}_compiled.json').write_text(json.dumps(record,indent=2),encoding='utf8');print(json.dumps({k:v for k,v in record.items() if k not in ['helperSnapshots','endpointDefinitions']},indent=2))
