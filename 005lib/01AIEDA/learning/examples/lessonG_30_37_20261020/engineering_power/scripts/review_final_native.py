from pathlib import Path
import csv,json,re,math,hashlib
B=Path(r'D:\001DIY\005lib\01AIEDA');G=B/'learning/examples/lessonG_30_37_20261020';R=G/'engineering_power'
source=json.loads((B/'learning/examples/de_15_26_20261019/integrated_circuit.json').read_text(encoding='utf-8'))
inventory=json.loads((G/'inventory/inventory_4L.json').read_text(encoding='utf-8'))
src={x['ref']:x for x in source['components']};inv={x['ref']:x for x in inventory['components']}
plan=json.loads((R/'readouts/layout_checkpoint_plan.json').read_text(encoding='utf-8'));pl={x['ref']:x for x in plan['placements']}
token=re.compile(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+')
def sexpr(t):
 ts=token.findall(t);i=0
 def parse():
  nonlocal i
  q=ts[i];i+=1
  if q=='(':
   a=[]
   while ts[i]!=')':a.append(parse())
   i+=1;return a
  if q.startswith('"'):return json.loads(q)
  if q=='nil':return None
  if q=='t':return True
  try:return float(q) if any(c in q for c in '.eE') else int(q)
  except ValueError:return q
 out=parse()
 if i!=len(ts):raise ValueError('Extra SKILL tokens: '+t)
 return out
def tsv(path):
 with path.open(encoding='utf-8-sig') as f:return list(csv.DictReader(f,delimiter='\t',quoting=csv.QUOTE_NONE))
def near(a,b):return len(a)==len(b) and all(abs(x-y)<=0.00011 for x,y in zip(a,b))
def transform(xy,at,rot):
 a=math.radians(rot);x,y=xy
 return [at[0]+x*math.cos(a)-y*math.sin(a),at[1]+x*math.sin(a)+y*math.cos(a)]
checks=[]
def ck(id,ok,details=None):checks.append(dict(id=id,passed=bool(ok),details=details))
allvariants={}
for variant in ['2L','4L']:
 snapPath=R/f'readouts/layout_checkpoint_actual_{variant}.json';d=json.loads(snapPath.read_text(encoding='utf-8'));logs=Path(d['readbackDirectory']);prefix=variant+':'
 summary=(logs/'native_summary.txt').read_text(encoding='utf-8')
 ck(prefix+'native_DRC0',re.search(r'(?m)^drcs=0$',summary)!=None,summary)
 symbols=[{k:sexpr(v) for k,v in x.items()} for x in tsv(logs/'g_actual_symbols.tsv')]
 actual={x['refdes']:x for x in symbols if x['refdes'] is not None}
 ck(prefix+'80_placed_unique_refs',set(actual)==set(src))
 rawpins=[{k:sexpr(v) for k,v in x.items()} for x in tsv(logs/'g_actual_pins.tsv')]
 logical=[p for p in rawpins if p['refdes'] is not None and p['pin'] and p['layer']=='ETCH/TOP' and not p['mechanical']]
 bypin={(p['refdes'],p['pin']):p for p in logical}
 ck(prefix+'272_logical_TOP_pins',len(logical)==len(bypin)==272)
 normalized={x['ref']:x for x in d['placements']}
 for ref,c in src.items():
  a=actual[ref];expected=pl[ref];origin=[expected['x'],expected['y']]
  ck(prefix+ref+':location',near(a['xy'],origin) and abs(a['rotation']-expected['rotation'])<0.00011)
  ck(prefix+ref+':package',a['package']==inv[ref]['package'])
  ck(prefix+ref+':bodyBBox',all(near(x,y) for x,y in zip(a['bodyExtent'],expected['extent'])))
  ck(prefix+ref+':normalizationOrigin',near(normalized[ref]['xy'],a['xy']) and abs(normalized[ref]['rotation']-a['rotation'])<0.00011)
  for n,net in c['pins'].items():
   p=bypin[(ref,n)];lp=next(x for x in inv[ref]['logicalPins'] if x['number']==n)
   world=transform(lp['localXY'],origin,expected['rotation'])
   ck(prefix+ref+'.'+n+':net',(p['net'] or None)==net)
   ck(prefix+ref+'.'+n+':worldXY',near(p['xy'],world))
   ck(prefix+ref+'.'+n+':padstack',p['padstack']==lp['padstack'])
   ib=lp['regularPadBBox'];pts=[transform([x,y],[0,0],expected['rotation']) for x in (ib[0][0],ib[1][0]) for y in (ib[0][1],ib[1][1])]
   expectedPadBBox=[[min(z[i] for z in pts) for i in (0,1)],[max(z[i] for z in pts) for i in (0,1)]]
   ck(prefix+ref+'.'+n+':rotatedPadBBox',all(near(x,y) for x,y in zip(p['padbbox'],expectedPadBBox)))

   np=next(x for x in normalized[ref]['pins'] if x['number']==n)
   ck(prefix+ref+'.'+n+':normalizedPin',(np['net'] or None)==net and near(np['xy'],p['xy']))
   normalizedBBox=[[p['xy'][i]+p['padbbox'][j][i] for i in (0,1)] for j in (0,1)]
   ck(prefix+ref+'.'+n+':normalizedPadBBox',all(near(x,y) for x,y in zip(np['padBBox'],normalizedBBox)))

 nets={x['net'] for x in tsv(logs/'nets.tsv')};expectednets={n for c in src.values() for n in c['pins'].values() if n}
 ck(prefix+'69_nets_unchanged',nets==expectednets and len(nets)==69)
 mech=[x for x in symbols if x['refdes'] is None]
 ck(prefix+'4_mechanical_NPTH_origins',sorted(x['xy'] for x in mech)==[[5,5],[5,55],[75,5],[75,55]])
 geometry=[{k:sexpr(v) for k,v in x.items()} for x in tsv(logs/'mechanical_direct.tsv')]
 outline=next(x for x in geometry if x['layer']=='BOARD GEOMETRY/DESIGN_OUTLINE')
 expectedvertices=[[2,0],[78,0],[80,2],[80,58],[78,60],[2,60],[0,58],[0,2]]
 ck(prefix+'C2_80x60_outline',outline['bbox']==[[0,0],[80,60]] and [x[0] for x in outline['vertices']]==expectedvertices)
 allroutes=[{k:sexpr(v) for k,v in x.items()} for x in tsv(logs/'route_geometry.tsv')]
 routes=[x for x in allroutes if x['layer'] and x['layer'].startswith('ETCH/')]
 vias=[{k:sexpr(v) for k,v in x.items()} for x in tsv(logs/'vias.tsv')]
 uniquevias={(x['x'],x['y'],x['net'],x['name']) for x in vias};groundvias=[(x[0],x[1]) for x in uniquevias if x[2]=='GND']
 planes=[{k:sexpr(v) for k,v in x.items()} for x in tsv(logs/'g_copper_shapes.tsv')]
 hold={}
 for ref,n in [('C3','2'),('U2','1'),('C8','2'),('C9','2'),('U4','2'),('C11','2')]:
  p=bypin[(ref,n)];hold[ref+'.'+n]={'xy':p['xy'],'nearestExistingGNDViaCenter_mm':round(min(math.dist(p['xy'],v) for v in groundvias),4) if groundvias else None,'status':'ROUTING_REQUIRED_NO_CLAIM_CURRENT_LOOP_COMPLETE'}
 allvariants[variant]={'snapshot':str(snapPath),'readback':str(logs),'netRouteCounts':{n:sum(x['net']==n for x in routes) for n in sorted({x['net'] for x in routes if x['net']})},'BUCK_notRouted':not any(x['net'] in ['BUCK_SW','BUCK_BOOT','BUCK_FB','VIN_PROT','V5'] for x in routes),'uniqueViaCount':len(uniquevias),'uniqueGNDViaCount':len(groundvias),'groundViaDistances':hold,'planes':planes}
failed=[x for x in checks if not x['passed']]
report={'status':'PASS_INDEPENDENT_POWER_INTERFACE_LAYOUT_REVIEW' if not failed else 'FAIL','checks':len(checks),'failed':failed,'detail':checks,'variants':allvariants,'scope':'Independent read-only raw native TSV vs original source, inventory and final plan. Placement QA and defined routing holds only, not production, EMC, PI/SI or impedance approval.','finalPlanSHA256':hashlib.sha256((R/'readouts/layout_checkpoint_plan.json').read_bytes()).hexdigest().upper()}
(R/'readouts/final_native_power_review.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps({'status':report['status'],'checks':len(checks),'failed':failed[:8],'routes':{v:d['netRouteCounts'] for v,d in allvariants.items()},'planes':{v:len(d['planes']) for v,d in allvariants.items()}},ensure_ascii=True))
