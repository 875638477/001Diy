"""Explicit per-net path candidates inside engineering policies; no Cadence writes."""
import pathlib,sys,argparse,json,math,heapq,time
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[2]/'scripts'))
from routing_geometry import CopperScene,load,LAYERS,ROOT,Point,np,shapely
P=argparse.ArgumentParser();P.add_argument('--snapshot',required=True);P.add_argument('--networks',required=True);P.add_argument('--rules',required=True);P.add_argument('--policy',required=True);P.add_argument('--out',required=True);P.add_argument('--nets',required=True);P.add_argument('--step',type=float,default=.05);P.add_argument('--max-expanded',type=int,default=350000);args=P.parse_args()
snapshot=load(args.snapshot);networks=load(args.networks);policy=load(args.policy)
for op in policy.get('pendingDeleteSegments',[]):
 matches=[r for r in snapshot['routes'] if r['net']==op['net'] and r['layer']=='ETCH/'+op['layer'] and abs(r['width']-op['width'])<1e-6 and (r['startEnd']==op['points'] or r['startEnd']==list(reversed(op['points']))) ]
 assert len(matches)==1,('Future engineered ripup must uniquely match source copper',op)
 snapshot['routes'].remove(matches[0])
scene=CopperScene(snapshot,networks,load(args.rules),policy)
# Native pads remain original. Only explicitly derived future via copper uses its declared diameter.
for o in scene.obstacles:
 if o['kind']=='via' and o['source']=='native_via':
  cc=o['geometry'].centroid
  vv=next((v for v in snapshot['vias'] if math.dist(v['xy'],[cc.x,cc.y])<1e-5),None)
  if vv and vv.get('padDiameterMM'):o['geometry']=Point(vv['xy']).buffer(vv['padDiameterMM']/2,quad_segs=16)
assert snapshot['readbackDirectory']==networks.get('nativeLog',networks.get('readback')),'Do not combine different native checkpoints'
for pending in policy.get('pendingOperations',[]):scene.add_operation(pending)
step=args.step;nx=round(80/step)+1;ny=round(60/step)+1
selected=args.nets.split(',');operations=[];proofs=[];reviews=[];failures=[]
DIRECTIONS=((1,0,1.),(-1,0,1.),(0,1,1.),(0,-1,1.),(1,1,math.sqrt(2)),(-1,1,math.sqrt(2)),(1,-1,math.sqrt(2)),(-1,-1,math.sqrt(2)))
def node(ix,iy,l):return (l*ny+iy)*nx+ix
def decode(n):q,ix=divmod(n,nx);l,iy=divmod(q,ny);return ix,iy,l
def qxy(xy):return round(xy[0]/step),round(xy[1]/step)
def unq(xy):return [round(xy[0]*step,6),round(xy[1]*step,6)]
def simplify(points):
 out=[]
 for p in points:
  p=[round(float(v),6) for v in p]
  if out and math.dist(p,out[-1])<1e-8:continue
  while len(out)>1:
   a,b=out[-2:];dx1,dy1=b[0]-a[0],b[1]-a[1];dx2,dy2=p[0]-b[0],p[1]-b[1]
   if abs(dx1*dy2-dy1*dx2)<1e-9 and dx1*dx2+dy1*dy2>=0:out.pop()
   else:break
  out.append(p)
 return out

def astar(net,source,target,width):
 # A fine nominal mask is followed by exact continuous path_clear on every segment.
 oldMasks=scene.masks
 def exact_masks(net,width,step):
  xs=np.arange(0,80+step/2,step);ys=np.arange(0,60+step/2,step);xx,yy=np.meshgrid(xs,ys);mm=[];vv=[]
  for lay in LAYERS:
   bad,inside=scene.forbidden(net,lay,width,False,.001);mm.append(shapely.contains_xy(bad,xx,yy)|~shapely.contains_xy(inside,xx,yy))
   bad,inside=scene.forbidden(net,lay,width,True,.001);vv.append(shapely.contains_xy(bad,xx,yy)|~shapely.contains_xy(inside,xx,yy))
  return mm,vv
 starts,viaMasks=exact_masks(net,width,step)
 for i,layer in enumerate(LAYERS):
  if 'allowEtch' in scene.rule(net,layer) and not scene.rule(net,layer)['allowEtch']:starts[i][:]=True
 
 def access(endpoint):
  pin=scene.pins[endpoint]
  if pin['ref']=='U1' and pin['net'] in policy.get('allowInwardPinAccess',[]):return list(pin['xy']),[list(pin['xy'])]
  return scene.endpoint_port(endpoint,width)
 sp,sourceLeg=access(source);tp,targetLeg=access(target)
 sx,sy=qxy(sp);tx,ty=qxy(tp);sourceLeg=simplify(sourceLeg+[unq((sx,sy))]);targetLeg=simplify(targetLeg+[unq((tx,ty))])
 sourceLayers=tuple(LAYERS.index(l) for l in scene.pins[source].get('layers',LAYERS if scene.pins[source]['through'] else ('TOP',)));targetLayers=tuple(LAYERS.index(l) for l in scene.pins[target].get('layers',LAYERS if scene.pins[target]['through'] else ('TOP',)))
 sourceLayers=tuple(l for l in sourceLayers if len(sourceLeg)<2 or scene.path_clear(net,LAYERS[l],sourceLeg,width));targetLayers=tuple(l for l in targetLayers if len(targetLeg)<2 or scene.path_clear(net,LAYERS[l],targetLeg,width))
 if not sourceLayers or not targetLayers:raise ValueError('Exact pad-to-grid fanout is obstructed on all permitted access layers')
 # Prevent the grid from retracing a forced MCU fanout through its own source pad.
 # Prefix geometry is already clear; the search must continue outside that pad.
 for endpoint in (source,target):
  p=scene.pins[endpoint]
  if p['ref']!='U1' or p['net'] in policy.get('allowInwardPinAccess',[]):continue
  g=p['geom'].buffer(width/2+.002);x0,y0,x1,y1=g.bounds
  for iy in range(max(0,math.floor(y0/step)),min(ny,math.ceil(y1/step)+1)):
   for ix in range(max(0,math.floor(x0/step)),min(nx,math.ceil(x1/step)+1)):
    if g.covers(Point(ix*step,iy*step)):starts[0][iy,ix]=True
 through=set()
 for p in scene.pins.values():
  if p['net']==net and p['through']:through.add(qxy(p['xy']))
 for o in scene.obstacles:
  if o['net']==net and o['kind']=='via':through.add(qxy([o['geometry'].centroid.x,o['geometry'].centroid.y]))
 goals={node(tx,ty,l) for l in targetLayers if not starts[l][ty,tx]}
 if not goals:raise ValueError('No legal target grid cell under the supplied rule/policy')
 def heuristic(x,y):
  dx=abs(tx-x);dy=abs(ty-y);return max(dx,dy)+(math.sqrt(2)-1)*min(dx,dy)
 heap=[];costs={};parent={};best=None;expanded=0
 for l in sourceLayers:
  if not starts[l][sy,sx]:n=node(sx,sy,l);costs[n]=0.;heapq.heappush(heap,(heuristic(sx,sy),0.,n))
 if not heap:raise ValueError('No legal source grid cell under supplied rule/policy')
 bottomFactor=policy.get('bottomCost',2. if snapshot['variant']=='2L' else 1.15);viaCost=policy.get('viaCostMM',12. if snapshot['variant']=='2L' else 5.)/step;bend=.15/step
 while heap:
  f,g,current=heapq.heappop(heap)
  if g!=costs.get(current):continue
  expanded+=1
  if current in goals:best=current;break
  if expanded>args.max_expanded:break
  x,y,l=decode(current);prior=parent.get(current);oldDir=None
  if prior is not None:
   px,py,pl=decode(prior)
   if pl==l:oldDir=(x-px,y-py)
  for dx,dy,distance in DIRECTIONS:
   xx,yy=x+dx,y+dy
   if not(0<=xx<nx and 0<=yy<ny) or starts[l][yy,xx]:continue
   if dx and dy and (starts[l][y,xx] or starts[l][yy,x]):continue
   n=node(xx,yy,l);ng=g+distance*(bottomFactor if l else 1.)+(bend if oldDir is not None and oldDir!=(dx,dy) else 0.)
   if ng+1e-9<costs.get(n,1e30):costs[n]=ng;parent[n]=current;heapq.heappush(heap,(ng+heuristic(xx,yy),ng,n))
  ll=1-l
  if not starts[ll][y,x] and ((x,y) in through or (not viaMasks[0][y,x] and not viaMasks[1][y,x])):
   n=node(x,y,ll);ng=g+(.01 if (x,y) in through else viaCost)
   if ng+1e-9<costs.get(n,1e30):costs[n]=ng;parent[n]=current;heapq.heappush(heap,(ng+heuristic(x,y),ng,n))
 if best is None:raise ValueError(f'No geometric candidate after {expanded} expanded cells')
 path=[]
 while True:
  path.append(decode(best))
  if best not in parent:break
  best=parent[best]
 path.reverse();segments=[];vias=[];currentLayer=path[0][2];points=list(sourceLeg)
 for i,(x,y,l) in enumerate(path):
  xy=unq((x,y))
  if l!=currentLayer:
   points=simplify(points+[xy]);segments.append((LAYERS[currentLayer],points));points=[xy]
   if (x,y) not in through:vias.append(xy)
   currentLayer=l
  elif not points or math.dist(points[-1],xy)>1e-8:points.append(xy)
 points=simplify(points+list(reversed(targetLeg)));segments.append((LAYERS[currentLayer],points))
 for layer,pts in segments:
  if len(pts)>1 and not scene.path_clear(net,layer,pts,width):raise ValueError('Continuous segment collision after grid simplification')
 return segments,vias,expanded

start=time.time();nets={n['net']:n for n in networks['nets']}
for net in selected:
 assert net not in policy.get('manualOnlyNets',[]),f'{net} requires explicit critical engineering path'
 n=nets[net];comps=[list(c['terminals']) for c in n['components']]
 for anchor in policy.get('componentAnchors',[]):
  if anchor['net']!=net:continue
  owners=[c for c in comps if any(t['key']==anchor['connectedTo'] for t in c)]
  assert len(owners)==1,'Explicit anchor must name one native terminal component'
  c=owners[0]
  if anchor.get('replacePinAccess'):c[:]=[t for t in c if t['key']!=anchor['connectedTo']]
  c.append({'key':anchor['key'],'xy':anchor['xy']})
 comps.sort(key=lambda c:-len(c))
 if len(comps)<2:reviews.append({'net':net,'joins':0,'note':'Already one native terminal component'});continue
 connected=comps.pop(0);joins=0;width=float(scene.rule(net,'TOP')['widthMinMM']);netStart=time.time()
 while comps:
  choices=sorted((math.dist(a['xy'],b['xy']),i,a['key'],b['key']) for i,c in enumerate(comps) for a in c for b in connected)
  joined=False;errors=[]
  for distance,i,source,target in choices[:8]:
   try:segments,vias,expanded=astar(net,source,target,width)
   except ValueError as error:errors.append({'from':source,'to':target,'reason':str(error)});continue
   tag=f'HI_{snapshot["variant"]}_{net}_{joins+1}'
   for j,xy in enumerate(vias):
    o={'type':'via','id':tag+f'_V{j+1}','net':net,'xy':xy,'padstack':'L28_VIA030_C060','purpose':'Geometric candidate signal transition; local reference and GND return-via review required'};operations.append(o);scene.add_operation(o)
   for j,(layer,pts) in enumerate(segments):
    if len(pts)<2:continue
    o={'type':'route','id':tag+f'_R{j+1}','net':net,'layer':layer,'points':pts,'width':width,'purpose':'Explicit candidate under native base rules and engineering reservations; native DRC/graph and actual return/reference review pending'};operations.append(o);scene.add_operation(o)
   proofs.append({'from':scene.pins[source].get('connectedTo',source),'to':scene.pins[target].get('connectedTo',target),'connected':True});connected.extend(comps.pop(i));joins+=1;joined=True
   print(json.dumps({'net':net,'join':joins,'from':source,'to':target,'expanded':expanded,'signalVias':len(vias),'elapsed':round(time.time()-start,1)}),flush=True);break
  if not joined:failures.append({'net':net,'remainingComponents':len(comps)+1,'attempts':errors});break
 reviews.append({'net':net,'joins':joins,'nativeInitialMinimumJoins':n['minTerminalJoins'],'remainingCandidateComponents':len(comps)+1,'seconds':round(time.time()-netStart,2)})
out=pathlib.Path(args.out).resolve();assert out.is_relative_to(ROOT.resolve())
data={'status':'GEOMETRIC_CANDIDATE_WITH_PENDING_NATIVE_AND_RETURN_REVIEW' if not failures else 'PARTIAL_CANDIDATE_REQUIRES_ENGINEERING_CORRECTION','batchId':out.stem,'variant':snapshot['variant'],'sourceExpectedSHA256':networks.get('sourceSHA256',networks.get('sha256')),'sourceNativeLog':networks.get('nativeLog',networks.get('readback')),'operations':operations,'proofs':proofs,'candidateReviews':reviews,'failures':failures,'scope':'Only specified ordinary nets; explicit critical routes excluded. Paths obey supplied geometry/clearance/keepout policies but this is not native DRC approval, automatic product routing, reference certification or manufacturing release.','pending':['Native batch create/update/DRC/fresh reopen','Actual reference continuity along both layers','Signal transition nearby GND return connections','Whole-board plane island/neck review','Physical/electrical class exceptions at actual positions'],'seconds':round(time.time()-start,2)}
out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(data,indent=2),encoding='utf8')
print(json.dumps({'output':str(out),'status':data['status'],'operations':len(operations),'joins':len(proofs),'failedNets':len(failures),'seconds':data['seconds']}))