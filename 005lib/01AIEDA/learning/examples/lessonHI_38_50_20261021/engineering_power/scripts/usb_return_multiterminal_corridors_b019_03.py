from pathlib import Path
import sys,json,math,heapq,copy
H=Path(r'D:/001DIY/005lib/01AIEDA/learning/examples/lessonHI_38_50_20261021');O=H/'engineering_power';sys.path[:0]=[str(H/'scripts'),str(O/'scripts'),str(H/'tooling/packages')]
from routing_geometry import *
import shapely,numpy as np
cp=H/'inventory/checkpoints/padentry_2L_b019_DRC_PENDING';base=load(cp/'normalized.json');w=load(cp/'networks.json');r=load(cp/'base_net_rules.json');policy=load(O/'N49_2L_policy.json');policy['pendingOperations']=[]
plans=[load(O/'USB_COMMON_RETURN_STITCH_2L_03.json'),load(O/'USB_COMMON_RETURN_LOCAL_VSS_STITCH_2L_02.json')]
step=.05;bounds=(34,12,49,31.5);xs=np.arange(bounds[0],bounds[2]+step/2,step);ys=np.arange(bounds[1],bounds[3]+step/2,step);X,Y=np.meshgrid(xs,ys);height,width=X.shape
pinGoals={f"U1.{p['number']}":p['xy']for c in base['placements']if c['ref']=='U1'for p in c['pins']if p['number']in['23','35','47']};assert len(pinGoals)==3
starts=[dict(id='BulkBelowR5_6',layer='BOTTOM',xy=[40.25,17.7]),dict(id='SourceReferenceNorthOfSlots',layer='BOTTOM',xy=[40.6,22.1]),dict(id='ESD_U4_2_GroundLand',layer='TOP',xy=[40.25,12.7])]
def build(stage):
 n=copy.deepcopy(base)
 if stage=='DERIVED_STITCH03_LOCAL02':
  for plan in plans:
   for op in plan['operations']:
    if op['type']=='via':
     tmp=copy.deepcopy(next(a for a in base['vias']if a['padstack']==op['padstack']));tmp['net']='GND';tmp['xy']=op['xy'];n['vias'].append(tmp)
    elif op['type']=='route':
     for a,b in zip(op['points'],op['points'][1:]):n['routes'].append(dict(net='GND',layer='ETCH/TOP',startEnd=[a,b],width=op['width'],kind='line',generatedThermal=False,fixedManualCline=True))
 s=CopperScene(n,w,r,policy);gnd={l:[]for l in ['TOP','BOTTOM']}
 for a in n['planes']:
  if a['net']=='GND'and a.get('generated'):gnd[a['layer'].removeprefix('ETCH/')].append(plane_from_native(dict(a,holes=a.get('holes')or[])))
 for a in n['routes']:
  if a['net']=='GND'and not a.get('generatedThermal'):gnd[a['layer'].removeprefix('ETCH/')].append(LineString(a['startEnd']).buffer(a['width']/2,quad_segs=24))
 for a in s.obstacles:
  if a['net']=='GND'and a['kind']in ['via','smdpin','thrupin']:gnd[a['layer']].append(a['geometry'])
 return n,{l:unary_union(z)for l,z in gnd.items()}
def run(stage,diameter):
 n,gnd=build(stage);valid=np.array([shapely.intersects_xy(gnd[l].buffer(-diameter/2+.0001),X,Y)for l in ['TOP','BOTTOM']]);loc={}
 for l in [0,1]:loc[l]=np.argwhere(valid[l])
 def near(l,q):
  arr=loc[l];ds=(arr[:,1]*step+xs[0]-q[0])**2+(arr[:,0]*step+ys[0]-q[1])**2;idx=int(np.argmin(ds));return(l,int(arr[idx,0]),int(arr[idx,1])),float(math.sqrt(ds[idx]))
 def idx(l,q):return(l,int(round((q[1]-ys[0])/step)),int(round((q[0]-xs[0])/step)))
 edges={}
 for a in n['vias']:
  if a['net']!='GND'or not box(*bounds).covers(Point(a['xy'])):continue
  aa,bb=idx(0,a['xy']),idx(1,a['xy'])
  if valid[aa]and valid[bb]:edges[aa]=(bb,a['xy']);edges[bb]=(aa,a['xy'])
 heap=[];dist={};prev={};owner={};goals={}
 for label,q in pinGoals.items():
  a,shift=near(0,q);dist[a]=0;owner[a]=label;goals[label]=dict(node=a,nudgeMM=shift);heapq.heappush(heap,(0,a))
 targets={};targetmeta={}
 for a in starts:
  node,shift=near(['TOP','BOTTOM'].index(a['layer']),a['xy']);targets[node]=a['id'];targetmeta[a['id']]=dict(node=node,nudgeMM=shift)
 seen=set();remaining=set(targets)
 while heap and remaining:
  cost,node=heapq.heappop(heap)
  if node in seen:continue
  seen.add(node);remaining.discard(node);l,y,x=node;ns=[]
  for dy,dx in[(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]:
   yy,xx=y+dy,x+dx
   if not(0<=yy<height and 0<=xx<width)or not valid[l,yy,xx]:continue
   if dx and dy and(not valid[l,y,xx]or not valid[l,yy,x]):continue
   ns.append(((l,yy,xx),step*math.hypot(dx,dy)))
  if node in edges:ns.append((edges[node][0],1.6))
  for b,inc in ns:
   nd=cost+inc
   if nd<dist.get(b,1e99):dist[b]=nd;prev[b]=node;owner[b]=owner[node];heapq.heappush(heap,(nd,b))
 out=[]
 for a in starts:
  label=a['id'];node=targetmeta[label]['node']
  if node not in seen:out.append(dict(start=a,status='NO_LOCAL_GRID_CORRIDOR_NOT_GLOBALDISCONNECTION',nudgeMM=targetmeta[label]['nudgeMM']));continue
  path=[node]
  while node in prev:node=prev[node];path.append(node)
  poly=[];transitions=[];planar=0
  for i,(l,y,x)in enumerate(path):
   q=[['TOP','BOTTOM'][l],round(float(xs[x]),4),round(float(ys[y]),4)]
   if i:
    if path[i-1][0]!=l:transitions.append(q[1:])
    else:planar+=step*math.hypot(y-path[i-1][1],x-path[i-1][2])
   if len(poly)>1 and poly[-2][0]==poly[-1][0]==q[0]and abs((q[1]-poly[-1][1])*(poly[-1][2]-poly[-2][2])-(q[2]-poly[-1][2])*(poly[-1][1]-poly[-2][1]))<1e-7:poly[-1]=q
   else:poly.append(q)
  out.append(dict(start=a,status='GEOMETRIC_CORRIDOR_NOT_HF_CURRENT_SOLUTION',corridorDiameterMM=diameter,nearestPhysicalMCUGroundPin=owner[path[0]],startNudgeMM=targetmeta[label]['nudgeMM'],goalNudgeMM=goals[owner[path[0]]]['nudgeMM'],planarLengthMM=planar,barrelJumps=transitions,costInclNominal16mmBoardThickness=dist[path[0]],polyline=poly))
 print(stage,diameter,[(a['start']['id'],a.get('planarLengthMM'),a.get('nearestPhysicalMCUGroundPin'),a.get('barrelJumps'))for a in out]);return dict(stage=stage,testCorridorDiameterMM=diameter,paths=out)
results=[run(stage,d)for stage in ['ACTUAL_B019','DERIVED_STITCH03_LOCAL02']for d in [.1,.2]]
file=O/'readouts/USB_b019_return_multiterminal_actual_vs_derived_03.json';file.write_text(json.dumps(dict(status='ACTUAL_VS_DERIVED_GROUND_CORRIDOR_DIAGNOSTIC_NOT_NATIVE_FILL_OR_SI_ACCEPTANCE',boardSHA=w['sha256'],bounds=bounds,gridStepMM=step,physicalGroundPinGoals=pinGoals,candidatePlans=[str(O/'USB_COMMON_RETURN_STITCH_2L_03.json'),str(O/'USB_COMMON_RETURN_LOCAL_VSS_STITCH_2L_02.json')],results=results,limitations=['GeometrygridwithnativecommonCu; sourcepads bbox/viadisks treatedsolid; actualbarreldrill/3Dinductance/currentdensity/fieldnotmodeled','Multi-goalphysicalMCUGNDpins23/35/47 used; previouswide02fixedVSS35normal22/32mmfiguresarenotglobalminimumEMreturnlengths','Nominal1.6mmviajumpcostjustgeometricbookkeeping, notdelay/impedance','No-pathinsidefinitewindowisnotglobaldisconnection; gridcorridorproofisnotnativegraphorHFvalidation','Derived4opsNOTexecuted; newprivateviapointapproval/alloldedges/ground/HSE/scopedDRC/actualrefillstillrequired']),indent=2)+'\n');print('SAVED',file)
