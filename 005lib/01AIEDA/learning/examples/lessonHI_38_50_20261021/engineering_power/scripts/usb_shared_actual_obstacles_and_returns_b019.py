from pathlib import Path
import sys,json,math,heapq,collections,hashlib
H=Path(r'D:/001DIY/005lib/01AIEDA/learning/examples/lessonHI_38_50_20261021');O=H/'engineering_power'
sys.path[:0]=[str(H/'scripts'),str(O/'scripts'),str(H/'tooling/packages')]
from routing_geometry import *
import numpy as np
import shapely
cp=H/'inventory/checkpoints/padentry_2L_b019_DRC_PENDING';n=load(cp/'normalized.json');w=load(cp/'networks.json');r=load(cp/'base_net_rules.json');p=load(O/'N49_2L_policy.json');p['pendingOperations']=[];s=CopperScene(n,w,r,p);a=load(O/'readouts/TOP_b018_2L_actual_reference_audit.json')
# b019 normalization Cuunion is independently verified unchanged from b018.
records=[]
for part in a['outsideReferencePieces']:
 if part['net']not in ['PA11_SHARED','PA12_SHARED']:continue
 line=LineString(part['points']);foot=line.buffer(part['sourceWidthMm']/2,cap_style=2);obs=[]
 for q in s.obstacles:
  if q['layer']!='BOTTOM' or q['net']=='GND' or q['kind']not in ['line','via','smdpin','thrupin']:continue
  expanded=q['geometry'].buffer(.3002);hit=line.intersection(expanded);footHit=foot.intersection(expanded)
  if hit.length<.001 and footHit.area<.001:continue
  item=dict(net=q['net'],kind=q['kind'],source=q['source'],bbox=q['geometry'].bounds,missingCenterlineWithinAssumed03ClearanceMM=hit.length,missingFootprintWithinAssumed03ClearanceMM2=footHit.area,directProjectionOverActualForeignCopperMM=line.intersection(q['geometry']).length)
  if q['kind']=='line':
   topconf=[]
   for other in s.obstacles:
    if other['layer']!='TOP' or other['net']==q['net']or other['kind']in['keepout','hole']:continue
    gap=q['geometry'].distance(other['geometry'])
    if gap<.16-.0001:topconf.append(dict(net=other['net'],source=other['source'],kind=other['kind'],gapMM=gap,overlapAreaMM2=q['geometry'].intersection(other['geometry']).area))
   item['sameXYChangeToTOPConflictsUnderEven016']=topconf[:12];item['shortTOPBridgeAtCurrentXY']=False if topconf else 'NOT_PROVEN_CLEAR_FULLRULEANDVIAAPPROACH_PENDING'
  else:item['shortTOPBridgeAtCurrentXY']='ViarequiresXYrelocationbothouterandinnerCu; cannotremoveantipadbychangingoneadjacenttrace'
  obs.append(item)
 obs.sort(key=lambda q:(-q['directProjectionOverActualForeignCopperMM'],-q['missingCenterlineWithinAssumed03ClearanceMM']))
 records.append(dict(net=part['net'],points=part['points'],lengthMM=part['lengthMm'],sourceWidthMM=part['sourceWidthMm'],nativeMissingPlaneIsObserved=True,obstacleCorrelations=obs,interpretation='ActualforeignCu projection is direct geometric obstruction; .3002 shell attribution is a local clearance correlation, not an exactCadence causegetter. Morethanoneobstaclecanoverlap; lengthsnotadditive.',sameLayerCommonSamples=part['coplanarSamples']))
# Actual common GND union: all GND pins/vias/generated shapes passed nativehealth;
# quietstatic is excluded even though uniqueanchor makes its netcommon.
ground={l:[]for l in ['TOP','BOTTOM']}
for z in n['planes']:
 if z['net']=='GND'and z.get('generated'):ground[z['layer'].removeprefix('ETCH/')].append(plane_from_native(dict(z,holes=z.get('holes')or[])))
for z in n['routes']:
 if z['net']=='GND'and not z.get('generatedThermal'):ground[z['layer'].removeprefix('ETCH/')].append(LineString(z['startEnd']).buffer(z['width']/2,quad_segs=24))
for z in s.obstacles:
 if z['net']=='GND'and z['kind']in ['smdpin','thrupin','via']:ground[z['layer']].append(z['geometry'])
ground={l:unary_union(g)for l,g in ground.items()}
bounds=(36.5,15.5,45.5,24.3);step=.05;xs=np.arange(bounds[0],bounds[2]+step/2,step);ys=np.arange(bounds[1],bounds[3]+step/2,step);X,Y=np.meshgrid(xs,ys);height,width=X.shape;count=height*width

def simplify(points):
 out=[]
 for q in points:
  if len(out)>1 and q[0]==out[-1][0]==out[-2][0]:out[-1]=q;continue
  if len(out)>1 and q[1]==out[-1][1] and out[-1][0]==out[-2][0]:out[-1]=q;continue
  if len(out)>1 and q[1]==out[-1][1]==out[-2][1]and abs((q[2]-out[-1][2])*(out[-1][3]-out[-2][3])-(q[3]-out[-1][3])*(out[-1][2]-out[-2][2]))<1e-7:out[-1]=q;continue
  out.append(q)
 return out

def route_return(label,layer,start,diameter):
 valid=[]
 for l in ['TOP','BOTTOM']:valid.append(shapely.intersects_xy(ground[l].buffer(-diameter/2+.0001),X,Y))
 valid=np.array(valid);goal=[42.3252,21.3248]
 def idx(l,q):return(l,int(round((q[1]-ys[0])/step)),int(round((q[0]-xs[0])/step)))
 def nearest(l,q):
  b=np.argwhere(valid[l]);dist=(b[:,1]*step+xs[0]-q[0])**2+(b[:,0]*step+ys[0]-q[1])**2;j=int(np.argmin(dist));return(l,int(b[j,0]),int(b[j,1])),float(math.sqrt(dist[j]))
 begin,shift=nearest(['TOP','BOTTOM'].index(layer),start);end,endshift=nearest(0,goal)
 edges={}
 for z in n['vias']:
  if z['net']!='GND' or not box(*bounds).covers(Point(z['xy'])):continue
  aa=idx(0,z['xy']);bb=idx(1,z['xy'])
  if valid[aa]and valid[bb]:edges[aa]=(bb,z['xy']);edges[bb]=(aa,z['xy'])
 heap=[(0,begin)];dist={begin:0};prev={};seen=set()
 while heap:
  cost,node=heapq.heappop(heap)
  if node in seen:continue
  seen.add(node)
  if node==end:break
  l,y,x=node;near=[]
  for dy,dx in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]:
   yy,xx=y+dy,x+dx
   if not(0<=yy<height and 0<=xx<width)or not valid[l,yy,xx]:continue
   if dx and dy and(not valid[l,y,xx]or not valid[l,yy,x]):continue
   near.append(((l,yy,xx),step*math.hypot(dx,dy)))
  if node in edges:near.append((edges[node][0],1.6))
  for b,inc in near:
   nd=cost+inc
   if nd<dist.get(b,1e99):dist[b]=nd;prev[b]=node;heapq.heappush(heap,(nd,b))
 if end not in seen:return dict(label=label,startLayer=layer,startRequested=start,corridorDiameterMM=diameter,status='NO_PATH_IN_LOCAL_GRID_NOT_GLOBALDISCONNECTION',startNudgeMM=shift,goalNudgeMM=endshift)
 path=[];q=end
 while True:
  path.append(q)
  if q==begin:break
  q=prev[q]
 path=path[::-1];switch=[];poly=[];planar=0
 for i,(l,y,x)in enumerate(path):
  poly.append([['TOP','BOTTOM'][l],round(float(xs[x]),4),round(float(ys[y]),4)])
  if i:
   if path[i-1][0]!=l:switch.append([round(float(xs[x]),4),round(float(ys[y]),4)])
   else:planar+=step*math.hypot(y-path[i-1][1],x-path[i-1][2])
 # Compress only collinear points on same actual layer, preserving switches.
 comp=[]
 for q in poly:
  if len(comp)>=2 and comp[-2][0]==comp[-1][0]==q[0]and abs((q[1]-comp[-1][1])*(comp[-1][2]-comp[-2][2])-(q[2]-comp[-1][2])*(comp[-1][1]-comp[-2][1]))<1e-7:comp[-1]=q
  else:comp.append(q)
 return dict(label=label,startLayer=layer,startRequested=start,goalLayer='TOP',goalNormalGroundBranchRequested=goal,startNudgeMM=shift,goalNudgeMM=endshift,corridorDiameterMM=diameter,status='GEOMETRIC_LOCAL_GROUND_CORRIDOR_IN_ACTUAL_NATIVE_COMMON_CU_NOT_HF_CURRENT_SOLUTION',planarLengthMM=planar,viaTransitions=switch,costWithNominal16LayerJumpMM=dist[end],polyline=comp,pendingActualVSS35NeckAdditionMM=1.39242640687119,limits='Gridsafe diagonals; generatedandmanualCu incl solid via pads approximated; realdrill/barrelinductance/skin/currentdensitynotmodeled. Goalnormalbranchthenknown.25VSS35neck. Not shortestEMreturnproof.')
returns=[]
for diameter in [.1,.2,.3]:
 for label,layer,start in [('BulkBelowR5_6','BOTTOM',[40.25,17.7]),('MCUNorthOfSlots','BOTTOM',[40.6,22.1]),('C14GroundViaTOP','TOP',[42.3252,19.35])]:returns.append(route_return(label,layer,start,diameter))
result=dict(status='READ_ONLY_FULL_SHARED_REFERENCE_OBSTACLE_AND_ACTUAL_GROUND_CORRIDOR_AUDIT_NO_SI_ACCEPTANCE',boardSHA=w['sha256'],checkpoint=str(cp),criticalNetsUntouched=['USB_DP','USB_DM','PA11_SHARED','PA12_SHARED'],gapPieces=records,localReturnCorridors=returns,corridorBounds=bounds,gridStepMM=step,classification=['Same-XYforeigntrace→TOP shortbridge is rejected wherever actualTOP_USB/otherCu conflict recorded','PA9/PA10 comparison03 is only a limited avoid-parallel candidate; forecaststill2.967/4.039mmsharedgaps, cannot callcomplete-reference repair','Actual C14.2→U1.35 directTOPGND branch is retained and spansBOTTOMsource slots; nativepositivecommon andlocalCu corridor are distinct evidence','ToremoveallTOP_USBunderlyingopeningsunderpresent2Lfanout wouldrequirejointordinarysourcefanout/layout/layercrossoverrework, not a singlelocalbridge; thisauditdoesnotproveimpossibleglobalrouting','Beforefinalacceptance: exactnativefreshgroundpin/via/shapecommon, alloldphysicaledges, HSEsingleanchornegative, all69appropriateDRCandactualcommon/widthreviewagainafterSouth'])
file=O/'readouts/USB_shared_b019_obstacles_and_actual_ground_corridors.json';file.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(output=str(file),pieces=len(records),returns=[{k:q.get(k)for k in['label','corridorDiameterMM','status','planarLengthMM','viaTransitions','startNudgeMM']}for q in returns])))
