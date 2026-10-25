import sys
sys.dont_write_bytecode=True
import pathlib,json,copy,math,hashlib
R=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
sys.path.insert(0,str(R/'scripts'))
from routing_geometry import CopperScene,load,Point,LineString,box,unary_union
OUT=R/'review/b020_engineering'
def near(a,b):return math.dist(a,b)<1e-6
def apply(s,ops):
 s=copy.deepcopy(s); evidence=[]
 for o in ops:
  if o['type']=='deleteSegment':
   ids=[i for i,a in enumerate(s['routes']) if not a.get('generatedThermal') and a['net']==o['net'] and a['layer'].removeprefix('ETCH/')==o['layer'] and abs(a['width']-o['width'])<1e-6 and (all(near(x,y) for x,y in zip(a['startEnd'],o['points'])) or all(near(x,y) for x,y in zip(a['startEnd'][::-1],o['points'])))]
   assert len(ids)==1,(o,ids);evidence.append({'id':o['id'],'matched':ids,'before':s['routes'][ids[0]]});s['routes'].pop(ids[0])
  elif o['type']=='deleteVia':
   ids=[i for i,a in enumerate(s['vias']) if a['net']==o['net'] and near(a['xy'],o['xy'])];assert len(ids)==1,(o,ids);evidence.append({'id':o['id'],'matched':ids,'before':s['vias'][ids[0]]});s['vias'].pop(ids[0])
  elif o['type']=='route':
   for a,b in zip(o['points'],o['points'][1:]):s['routes'].append({'net':o['net'],'layer':'ETCH/'+o['layer'],'startEnd':[a,b],'width':o['width'],'generatedThermal':False,'candidateId':o['id']})
  elif o['type']=='via':
   rad=o['padDiameterMM']/2;s['vias'].append({'net':o['net'],'xy':o['xy'],'padstack':o['padstack'],'drill':o['drillDiameterMM'],'candidateId':o['id'],'pads':[{'layer':l,'figure':'CIRCLE','bbox':[[-rad,-rad],[rad,rad]]} for l in s['actualEtchLayers']]})
 return s,evidence

def build(v):
 d=R/'inventory/checkpoints'/f'padentry_{v}_b019_DRC_PENDING';original=load(d/'normalized.json');ops=load(R/'engineering_mcu/plans'/f'GPIO_PB1_inward_{v}_80_delta.json')
 # Minimal PB1 L shift approved as read-only joint engineering candidate by MCU owner.
 for o in ops:
  if o['type']=='route' and o['net']=='GPIO_PB1' and o.get('layer')=='BOTTOM':o['points']=[[41.9,26.79],[40.8,25.69],[40.8,23.55],[36.7,23.55],[36.7,21.8],[36.25,21.35]]
  if o['type']=='via' and o['net']=='GND' and near(o['xy'],[36.92,27.8]):o['xy']=[37.85,27.82];o['id']='PB10_RELOCATED_ORDINARY_RETURN_2L'
 s,ev=apply(original,ops);n=load(d/'networks.json');rules=load(d/'base_net_rules.json');pol=load(R/'engineering_mcu/plans'/f'GPIO_PB1_inward_{v}_80_policy.json')
 scene=CopperScene(s,n,rules,pol)
 # Replace polygon approximations of via circles by near-exact circles and annotate original provenance.
 vi=iter(s['vias']);idx=0
 for a in scene.obstacles:
  if a['kind']=='via':
   z=s['vias'][idx//2];idx+=1;rad=max(abs(q) for p in z['pads'] if p['layer'].removeprefix('ETCH/')==a['layer'] for xy in p['bbox'] for q in xy);a['geometry']=Point(z['xy']).buffer(rad,quad_segs=128);a['source']=z.get('candidateId','native_via')+':'+str(z['xy']);a['xy']=z['xy']
 return original,s,scene,ops,ev

def audit(sc,net,layer,geom,via=False,limit=10):
 rows=[]
 for a in sc.obstacles:
  if a['layer']!=layer or a['net']==net:continue
  actual=geom.distance(a['geometry']);required=sc.space(net,a['net'],layer,a['kind'],via)
  # report base-field screening; local-region checks are separately evaluated using scene.path_clear for traces.
  rows.append({'net':a['net'],'kind':a['kind'],'source':a['source'],'bbox':list(a['geometry'].bounds),'gapMM':round(actual,9),'requiredBaseMM':required,'marginMM':round(actual-required,9),'overlapAreaMM2':round(geom.intersection(a['geometry']).area,9)})
 rows.sort(key=lambda a:a['marginMM'])
 return {'baseFieldIssues':[a for a in rows if a['marginMM']<-.00001], 'nearest':rows[:limit],'pairComparisons':len(rows)}

def main():
 summary={}
 for v in ('2L','4L'):
  original,s,sc,ops,ev=build(v)
  objects=[{'type':'route','id':'PB10_NW_BOTTOM_01','net':'GPIO_PB10','layer':'BOTTOM','points':[[38,26.3],[31.3,33]],'width':.2},{'type':'via','id':'PB10_NW_PORT_VIA_01','net':'GPIO_PB10','xy':[31.3,33],'padstack':'L28_VIA030_C060','padDiameterMM':.6,'drillDiameterMM':.3},{'type':'route','id':'PB10_NW_TOP_01','net':'GPIO_PB10','layer':'TOP','points':[[31.3,33],[30.5,33.8],[29.5,33.8]],'width':.2},{'type':'via','id':'PB10_NW_RETURN_01','net':'GND','xy':[30.2,32.9],'padstack':'L28_VIA030_C060','padDiameterMM':.6,'drillDiameterMM':.3}]
  results=[]
  for o in objects:
   if o['type']=='route':
    geom=LineString(o['points']).buffer(o['width']/2,quad_segs=128);r=audit(sc,o['net'],o['layer'],geom);r['pathClearIncludingFiniteRegions']=sc.path_clear(o['net'],o['layer'],o['points'],o['width']);results.append(dict(operation=o,audit=r))
   else:
    for layer0 in s['actualEtchLayers']:
     layer=layer0.removeprefix('ETCH/')
     if layer not in ('TOP','BOTTOM'):continue
     results.append(dict(operation=o,layer=layer,audit=audit(sc,o['net'],layer,Point(o['xy']).buffer(.3,quad_segs=128),True)))
  # Scan source-retaining NW segment end, no top escape assumed. Every candidate checked against all actual fixed copper.
  candidates=[]
  for i in range(121):
   x=38-i*.05;y=64.3-x
   if sc.path_clear('GPIO_PB10','BOTTOM',[[38,26.3],[x,y]],.2):
    gaps=[]
    for layer in ('TOP','BOTTOM'):
     a=audit(sc,'GPIO_PB10',layer,Point(x,y).buffer(.3,quad_segs=128),True,1);gaps.extend(a['baseFieldIssues'])
    if not gaps:candidates.append([round(x,4),round(y,4)])
  summary[v]={'scope':'READ_ONLY_LOCAL_CANDIDATE_NO_NATIVE','actualSourceDirectory':str(R/'inventory/checkpoints'/f'padentry_{v}_b019_DRC_PENDING'),'inputHashes':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest().upper() for p in [R/'inventory/checkpoints'/f'padentry_{v}_b019_DRC_PENDING'/'normalized.json',R/'engineering_mcu/plans'/f'GPIO_PB1_inward_{v}_80_delta.json']},'jointPB1Candidate':ops,'uniqueDeleteEvidence':ev,'initialCandidateResults':results,'clearStockViaCentersOnNWLine':candidates}
  print(v,'initial',[(o['operation']['id'],o.get('layer',o['operation'].get('layer')),len(o['audit']['baseFieldIssues']),o['audit']['nearest'][:2]) for o in results]);print('via candidates',candidates)
 (OUT/'PB10_NW_initial_audit_01.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8')
if __name__=='__main__':main()

