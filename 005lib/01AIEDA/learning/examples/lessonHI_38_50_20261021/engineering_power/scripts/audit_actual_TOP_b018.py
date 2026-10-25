from pathlib import Path
import sys,json,math,csv,re,hashlib,argparse
H=Path(r'D:/001DIY/005lib/01AIEDA/learning/examples/lessonHI_38_50_20261021')
O=H/'engineering_power'
sys.path[:0]=[str(H/'scripts'),str(O/'scripts'),str(H/'tooling/packages')]
from routing_geometry import *
from shapely.ops import nearest_points
from shapely.geometry import Point,LineString,box,Polygon
from reference_projection_screen_b016 import run as projection_run
import cadence_poly
USB={'USB_DP','USB_DM','PA11_SHARED','PA12_SHARED'}
NORTH={'GPIO_PC13','GPIO_PC14','GPIO_PC15','GPIO_PA1','GPIO_PA2','GPIO_PA3'}
def parts(g):
 if g.is_empty:return []
 if g.geom_type=='Polygon':return [g]
 return [p for a in getattr(g,'geoms',[]) for p in parts(a)]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def values(g):return [g] if not hasattr(g,'geoms')else list(g.geoms)
def rays(pt,dx,dy,ground):
 ln=math.hypot(dx,dy);out=[]
 for k in [-1,1]:
  q=LineString([[pt.x,pt.y],[pt.x-k*dy/ln*2,pt.y+k*dx/ln*2]])
  a=q.intersection(ground)
  out.append(None if a.is_empty else pt.distance(a))
 return out

def audit(v):
 cp=H/f'inventory/checkpoints/TOP_trial_{v}_b018_PRE_ALL69_DRC_PENDING'
 n=load(cp/'normalized.json');w=load(cp/'networks.json');r=load(cp/'base_net_rules.json')
 plan=load(O/f'GPIO_NORTH6_{v}_51.json')
 p=load(O/f'N49_{v}_policy.json');p['pendingOperations']=[]
 scene=CopperScene(n,w,r,p)
 log=Path(n['readbackDirectory'])
 rows=list(csv.DictReader((log/'hi_graph_objects.tsv').open(encoding='utf8'),delimiter='\t'))
 c1xy=scene.pins['C1.2']['xy'];root=[]
 for row in rows:
  if row['net'].strip('"')!='GND':continue
  xy=re.search(r'\bxy \(([-+\d.]+) ([-+\d.]+)\)',row['attributes'])
  if xy and math.dist(c1xy,[float(a)for a in xy.groups()])<.0001:root.append(row['component'])
 assert len(set(root))==1,root
 component=root[0];common=[a for a in rows if a['net'].strip('"')=='GND' and a['component']==component]
 ids={a['object']for a in common};commonXY=[];shapeBB={}
 for a in common:
  m=re.search(r'\bxy \(([-+\d.]+) ([-+\d.]+)\)',a['attributes'])
  if m:commonXY.append([float(z)for z in m.groups()])
  if a['type'].strip('"')=='shape':
   m=re.search(r'\bbBox \(\(([-+\d.]+) ([-+\d.]+)\) \(([-+\d.]+) ([-+\d.]+)\)\)',a['attributes'])
   if m:shapeBB.setdefault(a['layer'].strip('"'),[]).append([float(z)for z in m.groups()])
 ground={a:[]for a in ['TOP','BOTTOM','L2','L3']};plane={a:[]for a in ground};membership=[]
 for i,a in enumerate(n['planes']):
  if a['net']!='GND' or not a.get('filled'):continue
  g=plane_from_native(dict(a,holes=a.get('holes')or[]));layer=a['layer'].removeprefix('ETCH/')
  err=g.area-a['area'];assert abs(err)<.01,(i,err)
  match=any(max(abs(x-y)for x,y in zip(g.bounds,b))<.001 for b in shapeBB.get(a['layer'],[]))
  assert match,(i,a['layer'],g.bounds)
  quiet=not a.get('generated')
  membership.append(dict(index=i,layer=layer,nativeAreaMM2=a['area'],parsedAreaMM2=g.area,areaErrorMM2=err,nativeCommonComponent=component,excludedQuietStatic=quiet))
  if not quiet:ground[layer].append(g);plane[layer].append(g)
 for a in n['routes']:
  if a['net']!='GND' or a.get('generatedThermal'):continue
  m=re.search(r'\bparent (dbid:[^ )]+)',a.get('attributes',''))
  if m and m.group(1)in ids:ground[a['layer'].removeprefix('ETCH/')].append(LineString(a['startEnd']).buffer(a['width']/2,quad_segs=24))
 for a in scene.obstacles:
  if a['net']!='GND' or a['kind']not in ['via','smdpin','thrupin']:continue
  xy=([a['geometry'].centroid.x,a['geometry'].centroid.y]if a['kind']=='via'else scene.pins.get(a['source'],{}).get('xy',[999,999]))
  if any(math.dist(xy,b)<.001 for b in commonXY):ground[a['layer']].append(a['geometry'])
 ground={k:unary_union(a)for k,a in ground.items()};plane={k:unary_union(a)for k,a in plane.items()}
 projection=projection_run(cp)
 selected=USB|NORTH
 metrics=[a for a in projection['netLayerMetrics']if a['net']in selected]
 footprint_openings=[]
 refs={'TOP':'BOTTOM','BOTTOM':'TOP'}if v=='2L'else{'TOP':'L2','BOTTOM':'L3'}
 for a in n['routes']:
  if a['net']not in selected or not a.get('fixedManualCline')or a.get('generatedThermal'):continue
  layer=a['layer'].removeprefix('ETCH/');ref=refs[layer]
  g=LineString(a['startEnd']).buffer(a['width']/2,cap_style=2).difference(plane[ref].buffer(.0001))
  if g.area>.0001:footprint_openings.append(dict(net=a['net'],layer=layer,referenceLayer=ref,points=a['startEnd'],areaMM2=g.area,bbox=g.bounds,meaning='Signal-width footprint missing from generated reference; centerline may still be covered'))
 outside=[a for a in projection['outsideCenterlinePieces']if a['net']in selected]
 missing=[]
 for a in outside:
  line=LineString(a['points']);samples=[];dx=line.coords[-1][0]-line.coords[0][0];dy=line.coords[-1][1]-line.coords[0][1]
  for j in range(5):
   pt=line.interpolate(j/4,normalized=True);g=ground[a['signalLayer']]
   q=nearest_points(pt,g)[1]if not g.is_empty else None
   samples.append(dict(xy=[pt.x,pt.y],sameLayerCommonGroundCenterToEdgeMM=None if q is None else pt.distance(q),commonEdgeXY=None if q is None else[q.x,q.y],normalRayGroundDistancesMM=rays(pt,dx,dy,g)))
  missing.append(dict(**a,coplanarSamples=samples))
 gndvias=[a for a in n['vias']if a['net']=='GND'and any(math.dist(a['xy'],b)<.001 for b in commonXY)]
 vias=[]
 for a in n['vias']:
  if a['net']not in selected:continue
  pt=Point(a['xy']);nearest=sorted(gndvias,key=lambda b:math.dist(a['xy'],b['xy']))[:3]
  layers={}
  for l in ['TOP','BOTTOM']if v=='2L'else['L2','L3']:
   g=ground[l];annulus=pt.buffer(1.5).difference(pt.buffer(.65));layers[l]=dict(groundCoverageInR065to15Annulus=g.intersection(annulus).area/annulus.area,signalCenterToGroundMM=pt.distance(g))
  vias.append(dict(net=a['net'],xy=a['xy'],padstack=a['padstack'],nearestNativeCommonGroundVias=[dict(xy=b['xy'],distanceMM=math.dist(a['xy'],b['xy']),padstack=b['padstack'])for b in nearest],referenceLayers=layers))
 returns=[]
 for a in plan['returns']:
  pt=Point(a['returnXY']);assert any(math.dist(a['returnXY'],b['xy'])<.001 for b in gndvias),a
  ls={}
  for l in ['TOP','BOTTOM']if v=='2L'else['TOP','L2','L3']:
   g=ground[l];disk=pt.buffer(.3,quad_segs=64);d=dict(padDiskAreaMM2=disk.area,groundIntersectionMM2=disk.intersection(g).area,localR2GroundAreaMM2=g.intersection(pt.buffer(2)).area)
   # Geometric width-core screen only; no drilling or 3D current model.
   c=g.intersection(pt.buffer(2.5));widths=[]
   for width in [.05,.1,.2,.3,.4,.5,.6]:
    core=c.buffer(-width/2)
    ok=any(q.intersects(pt.buffer(.3))and not q.difference(pt.buffer(1.9)).is_empty for q in parts(core))
    widths.append(dict(testWidthMM=width,connectedErodedCoreFromPadNeighbourhoodToBeyondR19=ok))
   d['widthCoreDiagnostic']=widths;ls[l]=d
  returns.append(dict(signalXY=a['signalXY'],returnXY=a['returnXY'],distanceMM=math.dist(a['signalXY'],a['returnXY']),nativeCommon=True,layers=ls))
 result=dict(status='ACTUAL_NATIVE_COMMON_COPPER_ENGINEERING_SCREEN_NOT_SI_OR_FINAL_DRC_ACCEPTANCE',variant=v,checkpoint=str(cp),boardSHA256=w['sha256'],snapshotSHA256=sha(cp/'normalized.json'),graphSHA256=sha(log/'hi_graph_objects.tsv'),commonRoot=dict(pin='C1.2',xy=c1xy,component=component),nativeGroundShapeMembership=membership,netLayerMetrics=metrics,footprintOpenings=footprint_openings,outsideReferencePieces=missing,signalVias=vias,northNewReturnVias=returns,polygonParserDiagnostics=dict(parserSHA256=sha(O/'scripts/cadence_poly.py'),coincidentArcEndpoints=cadence_poly.COINCIDENT_ARC_ENDPOINTS,ambiguousShortArcFlattened=cadence_poly.ROUNDED_ARC_FLATTENED),remainingNativeJoins=w['summary']['nativeRemainingConnections'],wholeDRC=w['summary']['nativeDRC'],limits=['Only native C1.2-connected generated GND shapes/manualclines/pads/vias in coplanar union; static oscillator island deliberately excluded even though singleanchor gives common net.','Arc conversion mm4/signedquadrant contract, eachnativearea error<.01mm2; .0001mm boundary tolerance only in projection screen.','Coplanar pad bbox is conservative copper approximation; solid via disk used for geometric adjacency, ignores drill/barrel/3D inductance.','Width-core is 2D morphological local diagnostic: positive does not certify minimum manufacturedneck/HFreturn; negative needs topology review, cannot override nativegraph.','Distances are descriptive, no universal1.5mm pass criterion, no90ohm/USBcompliance/EMI/SIcertification.','15 actual-island arc-polygons were converted with axlDBCreateVoid on4L TOP (not GUI island_delete, no DYN_DELETED_ISLAND tag claimed); after furtherSouth routes check whether obsolete voids should be regenerated, while retainingquietgeometry.'])
 out=O/f'readouts/TOP_b018_{v}_actual_reference_audit.json';out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
 # Self-contained visual, real copper polygons with holes, not idealised fill.
 def svgpath(g,color,alpha=.55):
  paths=[]
  for q in parts(g):
   rings=[q.exterior]+list(q.interiors);d=' '.join('M '+' L '.join(f'{x:.5f},{y:.5f}'for x,y in ring.coords)+' Z'for ring in rings)
   paths.append(f'<path d="{d}" fill="{color}" fill-opacity="{alpha}" fill-rule="evenodd"/>')
  return ''.join(paths)
 def panel(title,region,refLayer,xx):
  x0,y0,x1,y1=region;scale=22;ww=(x1-x0)*scale;hh=(y1-y0)*scale
  st=f'<g transform="translate({xx},55)"><rect width="{ww}" height="{hh}" fill="#fff" stroke="#667"/><text x="0" y="-16" font-size="16">{title}</text><g transform="translate({-x0*scale},{y1*scale}) scale({scale},-{scale})">'
  st+=svgpath(ground[refLayer].intersection(box(*region)),'#51ad8f',.65)
  if refLayer!='TOP':st+=svgpath(ground['TOP'].intersection(box(*region)),'#7a8aad',.23)
  cols={'USB_DP':'#d33332','USB_DM':'#2456cf','PA11_SHARED':'#a435d0','PA12_SHARED':'#da8b10','GPIO_PC13':'#884400','GPIO_PC14':'#0022dd','GPIO_PC15':'#aa33aa','GPIO_PA1':'#f00000','GPIO_PA2':'#116622','GPIO_PA3':'#ee8800'}
  for a in n['routes']:
   if a['net']not in cols or a.get('generatedThermal'):continue
   g=LineString(a['startEnd']).buffer(a['width']/2,quad_segs=8).intersection(box(*region));st+=svgpath(g,cols[a['net']],1 if a['layer']=='ETCH/TOP'else .7)
  for a in n['vias']:
   if not box(*region).covers(Point(a['xy'])):continue
   if a['net']in cols or a['net']=='GND':
    x,y=a['xy'];co='#125f46'if a['net']=='GND'else cols[a['net']]
    st+=f'<circle cx="{x}" cy="{y}" r=".3" fill="{co}"/><circle cx="{x}" cy="{y}" r="{a["drill"]/2}" fill="white"/>'
  st+='</g></g>';return st,ww,hh
 svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1260" height="780" viewBox="0 0 1260 780"><rect width="1260" height="780" fill="#f8fafc"/><text x="20" y="25" font-family="Arial" font-size="17">Actual '+v+' b018 copper: geometric reference review; not SI certification</text>'];x=20
 for title,region,layer in [('USB / L2 reference'if v=='4L'else'USB / BOTTOM reference',(34,1,47,24),'L2'if v=='4L'else'BOTTOM'),('USB / actual TOP common GND',(34,1,47,24),'TOP'),('North source / '+('L3'if v=='4L'else'TOP')+' reference',(31.5,26.5,43.5,38.5),'L3'if v=='4L'else'TOP')]:
  st,ww,hh=panel(title,region,layer,x);svg.append(st);x+=ww+25
 svg.append('<text x="20" y="620" font-size="14">Green = native common GND; pale blue = TOP common copper overlay on reference view; red/blue/purple/orange = USB nets.</text><text x="20" y="645" font-size="14">All holes/voids retained; oscillator quiet island excluded. Signal paths shown across both outer layers, with BOTTOM translucent.</text><text x="20" y="670" font-size="14">South7 routing and whole-board DRC pending. Later copper edits require repeat fill/native common/HSE/reference checks.</text></svg>')
 svgpathout=O/f'readouts/TOP_b018_{v}_USB_NORTH_actual.svg';svgpathout.write_text(''.join(svg),encoding='utf8')
 print(json.dumps(dict(output=str(out),boardSHA=w['sha256'],topReferenceMetrics=[a for a in metrics if a['net']in USB],maxAreaError=max(abs(a['areaErrorMM2'])for a in membership),northReturns=[dict(xy=a['returnXY'],layers={k:[x['testWidthMM']for x in b['widthCoreDiagnostic']if x['connectedErodedCoreFromPadNeighbourhoodToBeyondR19']]for k,b in a['layers'].items()})for a in returns])))
 return result
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--variant',choices=['2L','4L'],required=True);args=a.parse_args();audit(args.variant)
