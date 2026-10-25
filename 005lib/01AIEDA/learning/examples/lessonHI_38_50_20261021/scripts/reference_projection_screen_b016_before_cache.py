"""Read-only geometry screen. Copper projection is not a return-current proof."""
from pathlib import Path
import json,sys,hashlib,math
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'tooling/packages'))
sys.path.insert(0,str(R/'engineering_power/scripts'))
from shapely.geometry import LineString
from shapely.ops import unary_union
from cadence_poly import plane_from_native
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def linear_parts(g):
 if g.is_empty:return []
 if g.geom_type=='LineString':return [g]
 if hasattr(g,'geoms'):return [p for c in g.geoms for p in linear_parts(c)]
 return []
def run(c):
 s=json.loads((c/'normalized.json').read_text(encoding='utf8'))
 n=json.loads((c/'networks.json').read_text(encoding='utf8'))
 v=s['variant'];refs={'TOP':'BOTTOM','BOTTOM':'TOP'} if v=='2L' else {'TOP':'L2','BOTTOM':'L3'}
 copper={};areas=[]
 for idx,p in enumerate(s['planes']):
  if p['net']!='GND' or not p['filled']:continue
  poly=plane_from_native(dict(p,holes=p.get('holes') or []))
  assert poly.is_valid
  error=poly.area-p['area']
  assert abs(error)<.02,(v,idx,error)
  is_quiet=not p.get('generated') and abs(p['area']-62.895)<.01
  layer=p['layer'].removeprefix('ETCH/')
  areas.append({'index':idx,'layer':layer,'nativeAreaMm2':p['area'],'parsedAreaMm2':poly.area,'errorMm2':error,'excludedQuietIsland':is_quiet,'nativeCommonConnectivityVerifiedInThisScript':False})
  if not is_quiet:copper.setdefault(layer,[]).append(poly)
 copper={k:unary_union(x) for k,x in copper.items()}
 out={};details=[]
 for r in s['routes']:
  if not r.get('fixedManualCline') or r.get('generatedThermal') or r['net']=='GND':continue
  pts=r['startEnd']
  if len(pts)<2:continue
  assert r['kind']=='line',r['kind']
  line=LineString(pts)
  if line.length<1e-8:continue
  layer=r['layer'].removeprefix('ETCH/')
  ref=refs.get(layer)
  assert ref is not None,('Unexpected signal on plane',v,r)
  key=(r['net'],layer)
  q=out.setdefault(key,{'net':r['net'],'signalLayer':layer,'candidateReferenceLayer':ref,'segments':0,'traceLengthMm':0,'projectedCenterlineOutsidePlaneMm':0,'traceFootprintAreaMm2':0,'footprintOutsidePlaneAreaMm2':0})
  plane=copper.get(ref)
  footprint=line.buffer(r['width']/2,cap_style=2,join_style=2)
  if plane is None:missing=line;uncovered_area=footprint.area
  else:missing=line.difference(plane.buffer(.0001));uncovered_area=footprint.difference(plane.buffer(.0001)).area
  q['segments']+=1;q['traceLengthMm']+=line.length;q['projectedCenterlineOutsidePlaneMm']+=missing.length;q['traceFootprintAreaMm2']+=footprint.area;q['footprintOutsidePlaneAreaMm2']+=uncovered_area
  for m in linear_parts(missing):
   if m.length<.01:continue
   details.append({'net':r['net'],'signalLayer':layer,'candidateReferenceLayer':ref,'lengthMm':m.length,'points':[[round(x,5),round(y,5)] for x,y in m.coords],'sourceWidthMm':r['width']})
 rows=sorted(out.values(),key=lambda q:q['projectedCenterlineOutsidePlaneMm'],reverse=True)
 for q in rows:
  q['centerlineOutsideFraction']=q['projectedCenterlineOutsidePlaneMm']/q['traceLengthMm'] if q['traceLengthMm'] else 0
  q['signalViaCountWholeNet']=sum(x['net']==q['net'] for x in s['vias'])
 nets={x['net']:x for x in n['nets']}
 return {'variant':v,'checkpoint':str(c),'snapshotSha256':sha(c/'normalized.json'),'nativeBoardSha256':n['sha256'],'status':'READ_ONLY_PLANE_PROJECTION_SCREEN_NOT_RETURN_PATH_OR_SI_ACCEPTANCE','remainingNativeJoins':n['summary']['nativeRemainingConnections'],'scope':{'geometry':'native filled GND planes with all holes and official arcs, quiet island excluded; +0.0001 mm boundary tolerance','coplanarGroundTracesPadsAndViasIncluded':False,'planeCommonMembershipProvenByThisScript':False,'referenceCorridorOrFieldCalculation':False,'traceFootprintArea':'sum per segment, overlapping ends can count twice; used only as a local screen','interpretation':'An opening can be intentional pad/via antipad or require return detour review. Coverage alone does not establish common ground, return inductance, impedance, compliance or pass/fail.'},'planes':areas,'netLayerMetrics':rows,'outsideCenterlinePieces':details,'pendingNetworks':[{'net':k,'joins':a['minTerminalJoins']} for k,a in nets.items() if a['minTerminalJoins']>0]}
if __name__=='__main__':
 all_results={}
 for v in ['2L','4L']:
  c=R/'inventory/checkpoints'/('clearance_'+v+'_b016_DRC_PENDING')
  all_results[v]=run(c)
 p=R/'review/reference_projection_screen_b016.json'
 p.write_text(json.dumps(all_results,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 print(json.dumps({'output':str(p),'status':'SCREEN_ONLY_NOT_FINAL_ACCEPTANCE','top5':{v:[{k:q[k] for k in ['net','signalLayer','traceLengthMm','projectedCenterlineOutsidePlaneMm']} for q in a['netLayerMetrics'][:5]] for v,a in all_results.items()}}))
