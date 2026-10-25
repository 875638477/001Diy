"""Explicit per-net path candidates inside engineering policies; no Cadence writes."""
import pathlib,sys,argparse,json,math,heapq,time
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[2]/'scripts'))
from routing_geometry import CopperScene,load,LAYERS,ROOT,Point,np,shapely
P=argparse.ArgumentParser();P.add_argument('--independent',action='store_true');P.add_argument('--snapshot',required=True);P.add_argument('--networks',required=True);P.add_argument('--rules',required=True);P.add_argument('--policy',required=True);P.add_argument('--out',required=True);P.add_argument('--nets',required=True);P.add_argument('--step',type=float,default=.05);P.add_argument('--max-expanded',type=int,default=350000);args=P.parse_args()
snapshot=load(args.snapshot);networks=load(args.networks);policy=load(args.policy)
for op in policy.get('pendingDeleteSegments',[]):
 matches=[r for r in snapshot['routes'] if r['net']==op['net'] and r['layer']=='ETCH/'+op['layer'] and abs(r['width']-op['width'])<1e-6 and (r['startEnd']==op['points'] or r['startEnd']==list(reversed(op['points']))) ]
 assert len(matches)==1,('Future engineered ripup must uniquely match source copper',op)
 snapshot['routes'].remove(matches[0])
import inspect
method=inspect.getsource(CopperScene.forbidden).replace(' def forbidden','def forbidden',1).replace('radius=.3 if via else width/2','radius=.26 if via else width/2')
# The original method body has one extra indentation level.
method='\n'.join(line[1:] if line.startswith(' ') else line for line in method.splitlines()) if method.startswith(' ') else method
ns={};exec(method,vars(sys.modules[CopperScene.__module__]),ns);CopperScene.forbidden=ns['forbidden']
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
 if net not in MASK_CACHE:MASK_CACHE[net]=exact_masks(net,width,step)
 starts,viaMasks=MASK_CACHE[net]
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
  dx=abs(tx-x);dy=abs(ty-y);return 1.5*(max(dx,dy)+(math.sqrt(2)-1)*min(dx,dy))
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
   n=node(xx,yy,l);ng=g+distance*((bottomFactor if l else 1.)+SOFTCOST[l][yy,xx])+(bend if oldDir is not None and oldDir!=(dx,dy) else 0.)
   if ng+1e-9<costs.get(n,1e30):costs[n]=ng;parent[n]=current;heapq.heappush(heap,(ng+heuristic(xx,yy),ng,n))
  ll=1-l
  if not starts[ll][y,x] and ((x,y) in through or (not viaMasks[0][y,x] and not viaMasks[1][y,x])):
   n=node(x,y,ll);ng=g+(.01 if (x,y) in through else viaCost)*(1.+float(SOFTVIA[0][y,x]+SOFTVIA[1][y,x]))
   if ng+1e-9<costs.get(n,1e30):costs[n]=ng;parent[n]=current;heapq.heappush(heap,(ng+heuristic(x,y),ng,n))
 if best is None:
  cells=[decode(z) for z in costs];summary=[]
  for ll in range(2):
   cc=[(x*step,y*step) for x,y,l in cells if l==ll]
   if cc:summary.append(dict(layer=LAYERS[ll],count=len(cc),bbox=[min(x for x,y in cc),min(y for x,y in cc),max(x for x,y in cc),max(y for x,y in cc)],nearestTargetMM=min(math.dist((x,y),tp) for x,y in cc)))
  raise ValueError(f'No geometric candidate after {expanded} expanded cells; reached={summary}')
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


from shapely.geometry import LineString,Polygon
from shapely.ops import unary_union
MASK_CACHE={};ROUTES={};HISTORY=[np.zeros((ny,nx),dtype=np.float32) for _ in range(2)]
X=np.arange(nx)*step;Y=np.arange(ny)*step

def mark(g,out,weight=1.):
 if g.is_empty:return
 x0,y0,x1,y1=g.bounds;ix0=max(0,math.floor(x0/step));ix1=min(nx,math.ceil(x1/step)+1);iy0=max(0,math.floor(y0/step));iy1=min(ny,math.ceil(y1/step)+1)
 if ix0>=ix1 or iy0>=iy1:return
 xx,yy=np.meshgrid(X[ix0:ix1],Y[iy0:iy1]);out[iy0:iy1,ix0:ix1]+=(weight*shapely.contains_xy(g,xx,yy)).astype(out.dtype)

def copper(ops):
 d={l:[] for l in LAYERS}
 for o in ops:
  if o['type']=='route':d[o['layer']].append(LineString(o['points']).buffer(o['width']/2,quad_segs=8))
  elif o['type']=='via':
   for l in LAYERS:d[l].append(Point(o['xy']).buffer(o.get('padDiameterMM',.52)/2,quad_segs=12))
 return {l:unary_union(gs) for l,gs in d.items()}

def conflicts():
 bad=[];geoms={n:copper(os) for n,os in ROUTES.items()}
 for i,a in enumerate(ROUTES):
  for b in list(ROUTES)[:i]:
   for l in LAYERS:
    ga,gb=geoms[a][l],geoms[b][l]
    if ga.is_empty or gb.is_empty:continue
    dist=ga.distance(gb)
    if dist<.1999:
     bad.append(dict(a=a,b=b,layer=l,distance=dist))
     hot=ga.buffer(.2).intersection(gb.buffer(.2)).buffer(.3)
     mark(hot,HISTORY[LAYERS.index(l)],.8)
 return bad

def feature(ops):
 c=copper(ops);tr=[np.zeros((ny,nx),dtype=np.uint8) for _ in range(2)];vi=[np.zeros((ny,nx),dtype=np.uint8) for _ in range(2)]
 for li,l in enumerate(LAYERS):mark(c[l].buffer(.301,quad_segs=8),tr[li]);mark(c[l].buffer(.461,quad_segs=8),vi[li])
 return tr,vi
start=time.time();initial=load(pathlib.Path(args.out).with_name('GPIO7_'+snapshot['variant']+'_independent59.json'))
for net in selected:ROUTES[net]=[o for o in initial['operations'] if o['net']==net]
FEATURE={n:feature(os) for n,os in ROUTES.items()};TOTALTRACE=[sum(f[0][li].astype(np.float32) for f in FEATURE.values()) for li in range(2)];TOTALVIA=[sum(f[1][li].astype(np.float32) for f in FEATURE.values()) for li in range(2)]
allreviews=[];failed=[];bad=conflicts();print(json.dumps({'round':0,'conflicts':len(bad)}),flush=True)
for turn in range(1,21):
 if not bad and all(ROUTES[n] for n in selected):break
 involved={q['a'] for q in bad}|{q['b'] for q in bad}|{n for n in selected if not ROUTES[n]}
 order=[n for n in selected if n in involved]
 if turn%2==0:order.reverse()
 for net in order:
  present=2.+turn*.8
  SOFTCOST=[h+present*(TOTALTRACE[li]-FEATURE[net][0][li]) for li,h in enumerate(HISTORY)];SOFTVIA=[h+present*(TOTALVIA[li]-FEATURE[net][1][li]) for li,h in enumerate(HISTORY)]
  a=next(a for a in policy['componentAnchors'] if a['net']==net)
  nn=next(n for n in networks['nets'] if n['net']==net)
  t=next(t for c in nn['components'] for t in c['terminals'] if not t['key'].startswith('U1.'))
  try:segments,vias,expanded=astar(net,a['key'],t['key'],.2)
  except ValueError as e:failed.append(dict(round=turn,net=net,error=str(e)));continue
  tag=f'NEG_{snapshot["variant"]}_{net}'
  ops=[dict(type='via',id=tag+f'_V{i}',net=net,xy=xy,padstack='HI_VIA026_C052_TENT',padDiameterMM=.52,drillDiameterMM=.26,purpose='Explicit signal transition; actual nearby GND return required') for i,xy in enumerate(vias)]
  ops += [dict(type='route',id=tag+f'_R{i}',net=net,layer=l,points=pts,width=.2,purpose='Ordinary GPIO candidate; engineering and native verification pending') for i,(l,pts) in enumerate(segments) if len(pts)>1]
  length=sum(sum(math.dist(a,b) for a,b in zip(o['points'],o['points'][1:])) for o in ops if o['type']=='route')
  old=FEATURE[net];new=feature(ops)
  for li in range(2):TOTALTRACE[li]+=new[0][li].astype(np.float32)-old[0][li];TOTALVIA[li]+=new[1][li].astype(np.float32)-old[1][li]
  FEATURE[net]=new
  print(json.dumps(dict(round=turn,net=net,lengthMM=round(length,2),elapsed=round(time.time()-start,1))),flush=True)
  ROUTES[net]=ops;allreviews.append(dict(round=turn,net=net,lengthMM=length,signalVias=len(vias),expanded=expanded))
 bad=conflicts()
 out=pathlib.Path(args.out);data=dict(status='GEOMETRIC_GROUP_CANDIDATE_PENDING_NATIVE_RETURN' if not bad else 'NEGOTIATION_PARTIAL_NOT_FOR_EXECUTION',variant=snapshot['variant'],round=turn,operations=[o for ops in ROUTES.values() for o in ops],conflicts=bad,failures=failed,reviews=allreviews,sourceNativeLog=snapshot['readbackDirectory'],scope='Helper-assisted ordinary GPIO candidates; no change to critical routes, electrical rules, feed, placement or native board. Not a routing/return certification.')
 out.write_text(json.dumps(data,indent=2),encoding='utf8');print(json.dumps({'round':turn,'conflicts':len(bad),'elapsed':round(time.time()-start,1),'out':str(out)}),flush=True)

