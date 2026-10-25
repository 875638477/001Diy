from pathlib import Path
import shutil
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
p=R/'scripts/compile_batchHI.py'
shutil.copyfile(p,R/'source/compile_batchHI_v1.py')
s=p.read_text()
s=s.replace("statements=['hiRegistry=nil']","""known={op['id']:op for op in data.get('operations',[])}
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
statements=['hiRegistry=nil','hiNodeDefinitions='+defs]""")
s=s.replace(" elif typ=='route':\n  pp=op['points'];"," elif typ=='shape':\n  poly=q(op['polygon']) if isinstance(op['polygon'],str) else points(op['polygon'])\n  vv='list('+' '.join(points(v) for v in op.get('voids',[]))+')'\n  statements.append(f'hiShape(f {q(ident)} {q(net)} {q(op[\"layer\"])} {poly} '+('t' if op.get('dynamic',False) else 'nil')+' '+vv+')')\n elif typ=='route':\n  pp=op['points'];")
s=s.replace("R/'scripts/batchHI.il',il]","R/'scripts/batchHI.il',R/'scripts/batchHI_extended.il',il]")
s=s.replace("'operations':len(data.get('operations',[]))","'operations':len(data.get('operations',[])),'endpointDefinitions':node_defs")
(R/'scripts/compile_batchHI_v2.py').write_text(s,encoding='ascii')
print('COMPILER_V2_PREPARED')
