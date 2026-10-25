"""Explicit per-net path candidates inside engineering policies; no Cadence writes."""
import pathlib,sys,argparse,json,math,heapq,time
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
sys.path.insert(0,r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\scripts')
from routing_geometry import CopperScene,load,LAYERS,ROOT,Point
P=argparse.ArgumentParser();P.add_argument('--snapshot',required=True);P.add_argument('--networks',required=True);P.add_argument('--rules',required=True);P.add_argument('--policy',required=True);P.add_argument('--out',required=True);P.add_argument('--nets',required=True);P.add_argument('--step',type=float,default=.05);P.add_argument('--max-expanded',type=int,default=350000);args=P.parse_args()
snapshot=load(args.snapshot);networks=load(args.networks);policy=load(args.policy)
# Candidate edits are declared future copper only; source SHA/readback is retained.
for edit in policy.get('pendingDeleteVias',[]):
 matches=[v for v in snapshot.get('vias',[]) if v['net']==edit['net'] and math.dist(v['xy'],edit['xy'])<1e-6 and (not edit.get('padstack') or v['padstack']==edit['padstack'])]
 assert len(matches)==1,('Future via ripup must be unique',edit,len(matches));snapshot['vias'].remove(matches[0])
for change in policy.get('pendingPlacementChanges',[]):
 comp=next(p for p in snapshot['placements'] if p['ref']==change['ref']);old=comp['xy'];new=change['xy'];rad=math.radians(change['rotation']-comp['rotation']);ca,sa=math.cos(rad),math.sin(rad)
 def transform(v):return [new[0]+(v[0]-old[0])*ca-(v[1]-old[1])*sa,new[1]+(v[0]-old[0])*sa+(v[1]-old[1])*ca]
 for pin in comp['pins']:
  pin['xy']=transform(pin['xy']);bb=pin['padBBox'];corners=[transform([x,y]) for x in (bb[0][0],bb[1][0]) for y in (bb[0][1],bb[1][1])];pin['padBBox']=[[min(v[0] for v in corners),min(v[1] for v in corners)],[max(v[0] for v in corners),max(v[1] for v in corners)]]
  for net in networks['nets']:
   for part in net['components']:
    for terminal in part['terminals']:
     if terminal['key']==comp['ref']+'.'+str(pin['number']):terminal['xy']=pin['xy']
 comp['xy']=new;comp['rotation']=change['rotation']

for op in policy.get('pendingDeleteSegments',[]):
 matches=[r for r in snapshot['routes'] if r['net']==op['net'] and r['layer']=='ETCH/'+op['layer'] and abs(r['width']-op['width'])<1e-6 and (r['startEnd']==op['points'] or r['startEnd']==list(reversed(op['points']))) ]
 assert len(matches)==1,('Future engineered ripup must uniquely match source copper',op)
 snapshot['routes'].remove(matches[0])
scene=CopperScene(snapshot,networks,load(args.rules),policy)
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
 starts,viaMasks=scene.masks(net,width,step)
 for i,layer in enumerate(LAYERS):
  if 'allowEtch' in scene.rule(net,layer) and not scene.rule(net,layer)['allowEtch']:starts[i][:]=True
 sp,sourceLeg=scene.endpoint_port(source,width);tp,targetLeg=scene.endpoint_port(target,width)
 sx,sy=qxy(sp);tx,ty=qxy(tp);sourceLeg=simplify(sourceLeg+[unq((sx,sy))]);targetLeg=simplify(targetLeg+[unq((tx,ty))])
 sourceLayers=tuple(LAYERS.index(l) for l in scene.pins[source].get('layers',LAYERS if scene.pins[source]['through'] else ('TOP',)));targetLayers=tuple(LAYERS.index(l) for l in scene.pins[target].get('layers',LAYERS if scene.pins[target]['through'] else ('TOP',)))
 sourceLayers=tuple(l for l in sourceLayers if len(sourceLeg)<2 or scene.path_clear(net,LAYERS[l],sourceLeg,width));targetLayers=tuple(l for l in targetLayers if len(targetLeg)<2 or scene.path_clear(net,LAYERS[l],targetLeg,width))
 if not sourceLayers or not targetLayers:raise ValueError('Exact pad-to-grid fanout is obstructed on all permitted access layers')
 # Prevent the grid from retracing a forced MCU fanout through its own source pad.
 # Prefix geometry is already clear; the search must continue outside that pad.
 for endpoint in (source,target):
  p=scene.pins[endpoint]
  if p['ref']!='U1':continue
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

start=time.time();proofs=[];operations=[];reviews=[];failures=[]
pairs={'SWCLK':[('ANCHOR_SWCLK','J9.4')],'SWO':[('ANCHOR_SWO','J9.6')],'GPIO_PA15':[('ANCHOR_GPIO_PA15','J13.4')],'GPIO_PB4':[('ANCHOR_GPIO_PB4','J13.5')],'GPIO_PB5':[('ANCHOR_GPIO_PB5','J13.6')],'GPIO_PB8':[('ANCHOR_GPIO_PB8','J13.7')],'GPIO_PB9':[('ANCHOR_GPIO_PB9','J13.8')],'I2C_SCL':[('ANCHOR_I2C_SCL','R19.2')],'I2C_SDA':[('ANCHOR_I2C_SDA','R20.2')],'BOOT0':[('ANCHOR_BOOT0','R28.1'),('R28.1','J8.2')]}
for net in selected:
 for join,(source,target) in enumerate(pairs[net]):
  try:segments,vias,expanded=astar(net,source,target,.2)
  except ValueError as e:failures.append(dict(net=net,source=source,target=target,reason=str(e)));print(json.dumps(failures[-1]),flush=True);continue
  for j,xy in enumerate(vias):
   o=dict(type='via',id='RIGHT_LONG_'+net+'_'+str(join)+'_V'+str(j),net=net,xy=xy,padstack='L28_VIA030_C060',purpose='Candidate transition; final return GND and reference proof mandatory');operations.append(o);scene.add_operation(o)
  for j,(layer,pts) in enumerate(segments):
   if len(pts)<2:continue
   o=dict(type='route',id='RIGHT_LONG_'+net+'_'+str(join)+'_R'+str(j),net=net,layer=layer,points=pts,width=.2,purpose='Explicit endpoint/corridor long route after engineered source; actual native/reference review pending');operations.append(o);scene.add_operation(o)
  proofs.append(dict(net=net,source=scene.pins[source].get('connectedTo',source),target=scene.pins[target].get('connectedTo',target)))
  reviews.append(dict(net=net,source=source,target=target,viaCount=len(vias),length_mm=sum(sum(math.dist(a,b) for a,b in zip(pts,pts[1:])) for _,pts in segments),expanded=expanded));print(json.dumps(reviews[-1]),flush=True)
out=pathlib.Path(args.out);out.write_text(json.dumps(dict(status='LONG_PATH_GEOMETRY_CANDIDATE_NEEDS_ENGINEERING_REVIEW',variant=snapshot['variant'],sourceExpectedSHA256=networks.get('sourceSHA256',networks.get('sha256')),operations=operations,proofs=proofs,reviews=reviews,failures=failures,scope='Specified right10 long endpoints only; sourcejoint and all declared future plans are obstacles. I2C remote R19/R20 toJ5 from rootv7 retained as separate knowncandidate, no duplicate automaticstar. Signal transitions need final ground. No Cadence invoked.'),indent=2),encoding='utf-8')
