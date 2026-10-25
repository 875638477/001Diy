from pathlib import Path
import json,hashlib,argparse
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
P=argparse.ArgumentParser();P.add_argument('--plan',required=True);P.add_argument('--variant',choices=['4L','2L'],required=True);P.add_argument('--tag',required=True)
a=P.parse_args();planpath=Path(a.plan);data=json.loads(planpath.read_text());tag=a.tag
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
statements=['hiRegistry=nil']
for p in data.get('placementChanges',[]):
 assert p.get('side','TOP')=='TOP'
 statements.append(f'hiMove(f {q(p["ref"])} {pt(p["xy"])} {num(p["rotation"])})')
for op in data.get('constraintOperations',[]):
 typ=op['type']
 if typ=='csetCopy':
  domain=op['domain'];assert domain in ['physical','spacing']
  vals='list('+' '.join('list(\''+k+' '+quotedValue(v)+')' for k,v in op['values'].items())+')'
  statements.append(f'hiCSet(f \'{domain} {q(op["name"])} {q(op["copyFrom"])} {vals})')
 elif typ=='region':
  assigns='list('+' '.join('list('+q(x['netClass'])+' \''+x['domain']+' '+q(x['cset'])+')' for x in op['assignments'])+')'
  statements.append(f'hiRegion(f {q(op["id"])} {q(op["layer"])} {points(op["polygon"])} {assigns})')
 else:raise ValueError(typ)
proofs=[]
for op in data.get('operations',[]):
 typ=op['type'];ident=op['id'];net=op['net']
 if typ=='via':statements.append(f'hiVia(f {q(ident)} {q(net)} {pt(op["xy"])} {q(op["padstack"])})')
 elif typ=='route':
  pp=op['points'];ww=op.get('widths',[op.get('width')]*(len(pp)-1))
  assert len(ww)==len(pp)-1 and all(w is not None and w>0 for w in ww)
  statements.append(f'hiRoute(f {q(ident)} {q(net)} {q(op["layer"])} {points(pp)} list('+' '.join(num(x) for x in ww)+'))')
  if op.get('from') and op.get('to'):proofs.append((terminal(op['from']),terminal(op['to']),True))
 else:raise ValueError(typ)
for p in data.get('proofs',[]):proofs.append((terminal(p['from']),terminal(p['to']),p.get('connected',True)))
proofstr='list('+' '.join('list('+q(a)+' '+q(b)+' '+('t' if c else 'nil')+')' for a,b,c in proofs)+')'
code='procedure(hiBatchProgram()\n let((f)\n  f=outfile('+q((out/'hi_batch_execution.txt').as_posix())+')\n  '+ '\n  '.join(statements)+'\n  hiFinalize(f '+q(out.as_posix())+' '+q(board.as_posix())+' '+q((R/'library').as_posix())+' '+proofstr+')\n  t))\n'
il.write_text(code,encoding='ascii')
helpers=['de_board_read.il','build29_v2.il','read29.il','extra_read29.il','specific_proof.il','more28.il','mechanical28.il','correction.il','inventoryG.il','placementG.il','local_copperG_v2.il']
loads=[R/'source'/x for x in helpers]+[R/'scripts/network_inventoryHI_v2.il',R/'scripts/batchHI.il',il]
h='set NOCONFIRM\n'+''.join('skill errset(load('+q(p.as_posix())+') t)\n' for p in loads)
script=R/f'scripts/{tag}.scr';script.write_text(h+'skill errset(hiBatchProgram() t)\nquit\nfillin "yes"\n',encoding='ascii')
record={'plan':str(planpath),'planSHA256':hashlib.sha256(planpath.read_bytes()).hexdigest().upper(),'variant':a.variant,'batch':tag,'output':str(board),'log':str(out),'script':str(script),'proofCount':len(proofs),'operations':len(data.get('operations',[]))}
(R/f'scripts/{tag}_compiled.json').write_text(json.dumps(record,indent=2),encoding='utf8');print(json.dumps(record,indent=2))
