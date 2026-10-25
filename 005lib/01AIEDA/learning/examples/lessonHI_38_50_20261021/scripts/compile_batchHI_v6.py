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
 if isinstance(v,bool):return 't' if v else 'nil'
 if isinstance(v,(int,float)):return num(v)
 return q(v)
def terminal(x):
 if isinstance(x,dict):return x['ref']+'.'+str(x['pin'])
 return x
out=R/f'logs/{tag}';board=R/f'native/HI_{a.variant}_{tag}.brd';il=R/f'scripts/{tag}.il'
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
statements=['hiRegistry=nil','hiNodeDefinitions='+defs]
for p in data.get('placementChanges',[]):
 assert p.get('side','TOP')=='TOP'
 statements.append(f'hiMove(f {q(p["ref"])} {pt(p["xy"])} {num(p["rotation"])})')
for op in data.get('constraintOperations',[]):
 typ=op['type']
 if typ=='csetCopy':
  domain=op['domain'];assert domain in ['physical','spacing']
  vals='list('+' '.join('list(\''+k+' '+quotedValue(v)+')' for k,v in op['values'].items())+')'
  statements.append(f'hiCSet(f \'{domain} {q(op["name"])} {q(op["copyFrom"])} {vals})')
  for layer,fields in op.get('layerValues',{}).items():
   for field,val in fields.items():statements.append(f'hiCSetLayerValue(f \'{domain} {q(op["name"])} {q(layer)} \'{field} {quotedValue(val)})')
 elif typ=='netClass':
  statements.append(f'hiAssignNetClass(f {q(op["name"])} \'{op["domain"]} {q(op["cset"])} list('+ ' '.join(q(n) for n in op['nets'])+'))')
 elif typ=='region':
  assigns='list('+' '.join('list('+q(x['netClass'])+' \''+x['domain']+' '+q(x['cset'])+' '+(q(x['otherNetClass']) if x.get('otherNetClass') else 'nil')+')' for x in op['assignments'])+')'
  statements.append(f'hiRegion(f {q(op["id"])} {q(op["layer"])} {points(op["polygon"])} {assigns})')
 else:raise ValueError(typ)
proofs=[]
for op in data.get('operations',[]):
 typ=op['type'];ident=op['id'];net=op['net']
 if typ=='bindShape':statements.append(f'hiBindExistingShape(f {q(ident)} {q(net)} {q(op["layer"])})')
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
for check in data.get('postChecks',[]):
 if check['type']=='hseIsolation':statements.append(f'hiHSEIsolationChallenge({q(out.as_posix())} {pt(check["anchorXY"])} {q(check["localLayer"])} {points(check["guardPoints"])})')
 else:raise ValueError(check['type'])
for p in data.get('proofs',[]):proofs.append((terminal(p['from']),terminal(p['to']),p.get('connected',True)))
proofstr='list('+' '.join('list('+q(a)+' '+q(b)+' '+('t' if c else 'nil')+')' for a,b,c in proofs)+')'
code='procedure(hiBatchProgram()\n let((f)\n  f=outfile('+q((out/'hi_batch_execution.txt').as_posix())+')\n  '+ '\n  '.join(statements)+'\n  hiFinalize(f '+q(out.as_posix())+' '+q(board.as_posix())+' '+q((R/'library').as_posix())+' '+proofstr+')\n  t))\n'
il.write_text(code,encoding='ascii')
helpers=['de_board_read.il','build29_v2.il','read29.il','extra_read29.il','specific_proof.il','more28.il','mechanical28.il','correction.il','inventoryG.il','placementG.il','local_copperG_v2.il']
loads=[R/'source'/x for x in helpers]+[R/'scripts/network_inventoryHI_v2.il',R/'scripts/batchHI.il',R/'scripts/batchHI_extended.il',R/'scripts/batchHI_shapes_v3.il',il]
snapshot=R/'source/batch_snapshots'/tag
snapshot.mkdir(parents=True,exist_ok=False)
input_records=[]
snaploads=[]
for i,orig in enumerate(loads):
 dest=snapshot/(f'{i:02d}_'+orig.name);shutil.copyfile(orig,dest);snaploads.append(dest)
 input_records.append({'source':str(orig),'snapshot':str(dest),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest().upper()})
(snapshot/'inputs_manifest.json').write_text(json.dumps(input_records,indent=2),encoding='utf8')
h='set NOCONFIRM\n'+''.join('skill errset(load('+q(p.as_posix())+') t)\n' for p in snaploads)
script=R/f'scripts/{tag}.scr';script.write_text(h+'skill errset(hiBatchProgram() t)\nquit\nfillin "yes"\n',encoding='ascii')
record={'plan':str(planpath),'planSHA256':hashlib.sha256(planpath.read_bytes()).hexdigest().upper(),'variant':a.variant,'batch':tag,'output':str(board),'log':str(out),'script':str(script),'proofCount':len(proofs),'operations':len(data.get('operations',[])),'endpointDefinitions':node_defs,'helperSnapshots':input_records}
(R/f'scripts/{tag}_compiled.json').write_text(json.dumps(record,indent=2),encoding='utf8');print(json.dumps({k:v for k,v in record.items() if k not in ['helperSnapshots','endpointDefinitions']},indent=2))
