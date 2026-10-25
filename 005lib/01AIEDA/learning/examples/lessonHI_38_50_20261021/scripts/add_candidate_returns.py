"""Screen nearby APP-GND stitches for explicit signal transitions, not reference certification."""
import sys,pathlib,argparse,json,math
sys.path.insert(0,str(pathlib.Path(__file__).parent))
from routing_geometry import CopperScene,Point,Polygon,load,LAYERS
p=argparse.ArgumentParser();p.add_argument('--checkpoint',required=True);p.add_argument('--policy',required=True);p.add_argument('--plans',nargs='+',required=True);p.add_argument('--out',required=True);a=p.parse_args()
c=pathlib.Path(a.checkpoint);s=load(c/'normalized.json');n=load(c/'networks.json');policy=load(a.policy)
scene=CopperScene(s,n,load(c/'base_net_rules.json'),policy)
for op in policy.get('pendingOperations',[]):scene.add_operation(op)
ops=[]
for path in a.plans:
 data=load(path);ops+=data.get('operations',[])+data.get('commonOperations',[])+data.get('variantOperations',{}).get(s['variant'],[])
for op in ops:scene.add_operation(op)
quiet=[Polygon(poly).buffer(.301) for poly in policy.get('noGlobalGroundViaAreas',[])]
def is_app(xy):return not any(q.intersects(Point(xy)) for q in quiet)
common=[]
for v in s.get('vias',[]):
 if v['net']=='GND' and is_app(v['xy']):common.append({'xy':v['xy'],'source':'native_GND_via'})
for v in scene.pins.values():
 if v['net']=='GND' and v['through'] and is_app(v['xy']):common.append({'xy':v['xy'],'source':v['key']})
for op in policy.get('pendingOperations',[])+ops:
 if op['type']=='via' and op['net']=='GND' and is_app(op['xy']):common.append({'xy':op['xy'],'source':op['id']})
allvias=[v['xy'] for v in s.get('vias',[])]+[o['xy'] for o in policy.get('pendingOperations',[])+ops if o['type']=='via']
returns=[];reviews=[];failures=[]
for op in ops:
 if op['type']!='via' or op['net']=='GND':continue
 xy=op['xy'];nearest=min(common,key=lambda x:math.dist(xy,x['xy']))
 if math.dist(xy,nearest['xy'])<=1.5+1e-6:
  reviews.append({'signalVia':op['id'],'net':op['net'],'xy':xy,'return':nearest,'distanceMM':math.dist(xy,nearest['xy']),'newStitch':False});continue
 masks=[scene.forbidden('GND',l,.6,via=True,gridMargin=.002) for l in LAYERS]
 candidates=[]
 for radius in (.95,1.05,1.2,1.35,1.45):
  for angle in range(0,360,10):
   t=math.radians(angle);pt=[round(xy[0]+radius*math.cos(t),3),round(xy[1]+radius*math.sin(t),3)];g=Point(pt)
   if not is_app(pt) or any(g.distance(Point(v))<.602 for v in allvias):continue
   if any(bad.intersects(g) or not allowed.covers(g) for bad,allowed in masks):continue
   # Local stitch near a presently common GND via/through terminal is preferable,
   # but generated copper must be updated and graph-verified natively after insertion.
   existing=min(math.dist(pt,v['xy']) for v in common)
   candidates.append((radius+min(existing,10)*.04,pt))
 if not candidates:failures.append({'signalVia':op['id'],'net':op['net'],'xy':xy,'reason':'No fully screened APP-GND stitch <=1.5mm; explicit topology review required'});continue
 score,pt=min(candidates);r={'type':'via','id':'APP_RETURN_'+op['id'],'net':'GND','xy':pt,'padstack':'L28_VIA030_C060','purpose':'Nearby signal transition APP-GND stitch, both external copper layers screened. Native updated-copper common-GND connectivity and reference continuity still required.'}
 returns.append(r);scene.add_operation(r);allvias.append(pt);common.append({'xy':pt,'source':r['id']})
 reviews.append({'signalVia':op['id'],'net':op['net'],'xy':xy,'return':common[-1],'distanceMM':math.dist(xy,pt),'newStitch':True})
data={'status':'RETURN_STITCH_CANDIDATE_NATIVE_AND_ACTUAL_REFERENCE_PENDING' if not failures else 'PARTIAL_RETURN_REQUIRES_ENGINEERING','variant':s['variant'],'sourceExpectedSHA256':n.get('sha256',n.get('sourceSHA256')),'sourcePlans':a.plans,'operations':returns,'proofs':[],'reviews':reviews,'failures':failures,'scope':'Distance is a geometry screen only: not proof of reference continuity, return-current distribution, impedance or EMI. Excludes HSE quiet island and guard region. Drill/solder-mask/body/assembly assumptions remain.'}
pathlib.Path(a.out).write_text(json.dumps(data,indent=2),encoding='utf8');print(json.dumps({'newGND':len(returns),'signalVias':len(reviews),'failures':failures}))