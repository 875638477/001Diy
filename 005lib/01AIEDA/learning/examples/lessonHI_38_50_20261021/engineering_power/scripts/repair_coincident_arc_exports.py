from pathlib import Path
import json,math,sys,shutil,hashlib,importlib
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');P=R/'engineering_power';p=P/'scripts/cadence_poly.py';backup=P/'scripts/cadence_poly_v2_before_coincident_arc_20261022.py'
s=p.read_text(encoding='utf-8');assert 'COINCIDENT_ARC_ENDPOINTS'not in s
if not backup.exists():shutil.copyfile(p,backup)
s=s.replace('ROUNDED_ARC_FLATTENED = []','ROUNDED_ARC_FLATTENED = []\nCOINCIDENT_ARC_ENDPOINTS = []')
needle='  assert d<=2*r+.001,(d,r)\n  h=math.sqrt'
replacement='''  assert d<=2*r+.001,(d,r)
  if d<=1e-12:
   # Official axlPolyFromDB splits arcs at quadrant boundaries: one arc
   # cannot be a full circle. With exported mm4 endpoints, two distinct
   # tangent/quadrant endpoints can round to the same 0.0001mm point.
   # Preserve the vertex/hole and flatten only this zero exported chord.
   # Bound the unknown true chord by a rounding-cell diagonal and <=90deg.
   quantum_mm=.0001
   assert len(vs)>=4 and len({tuple(a[0])for a in vs})>=3, ('Degenerate arc polygon, cannot infer circle',vs)
   chord_bound=min(math.sqrt(2)*quantum_mm,math.sqrt(2)*r)
   sag_bound=r-math.sqrt(max(0,r*r-chord_bound*chord_bound/4))
   point_bound=quantum_mm/math.sqrt(2)+sag_bound
   assert sag_bound<=1e-5 and point_bound<.0001, ('Coincident arc exceeds conservative tolerance',r,sag_bound,point_bound)
   COINCIDENT_ARC_ENDPOINTS.append(dict(start=start,end=end,radius=rr,exportQuantumMM=quantum_mm,trueChordUpperMM=chord_bound,sagittaUpperMM=sag_bound,pointDeviationUpperMM=point_bound,vertexCount=len(vs),vertexIndex=i,action='Preserve repeated vertex; flatten only zero exported chord; whole hole retained',basis='Official axlPolyFromDB quadrant-limited arc contract + known mm4 export precision'))
   out.append(end);continue
  h=math.sqrt'''
assert needle in s;s=s.replace(needle,replacement)
p.write_text(s,encoding='utf-8')
sys.path.insert(0,str(R/'tooling/packages'));sys.path.insert(0,str(P/'scripts'));import cadence_poly as mod
records=[]
for v in ['2L','4L']:
 cp=R/f'inventory/checkpoints/source_{v}_b015_DRC_PENDING/normalized.json';snap=json.loads(cp.read_text());
 for idx,rec in enumerate(snap['planes']):
  if not rec.get('filled'):continue
  q=mod.plane_from_native(dict(rec,holes=rec.get('holes')or[]));native=rec['area'];err=abs(q.area-native);assert q.is_valid and err<.01,(v,idx,err)
  c=mod.conservative_plane(dict(rec,holes=rec.get('holes')or[]));assert c.difference(q).area<1e-8
  records.append(dict(variant=v,planeIndex=idx,layer=rec['layer'],nativeAreaMM2=native,convertedAreaMM2=q.area,absoluteAreaErrorMM2=err,nativeHoleCount=len(rec.get('holes')or[]),retainedHoleScope='Every complete nativehole converted; only onezero exported edge may repeat',conservativeAreaMM2=c.area,source=str(cp)))
coincident=mod.COINCIDENT_ARC_ENDPOINTS;assert coincident
out=dict(status='PASS_OFFICIAL_QUADRANT_CONTRACT_BOUNDED_DEGENERATE_EXPORT_AUDIT',officialAPI='source/axlPolyFromDB.txt',parserSHA256=hashlib.sha256(p.read_bytes()).hexdigest().upper(),backup=str(backup),records=records,maxAbsoluteAreaErrorMM2=max(x['absoluteAreaErrorMM2']for x in records),coincidentArcEvents=coincident,roundedArcFlattenEvents=mod.ROUNDED_ARC_FLATTENED,scope='Only knownmm4 roundedexport used; not silentlydiscarding fullholes or assumingfullcircle. Wholeboard rendering/actualreference auditmayproceed with0.0001mmerosion/holeexpansion. Nativearea printedprecision ispartofthecomparison. NoCadenceexecution.')
(P/'readouts/arc_source_b015_area_audit.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(status=out['status'],planes=len(records),maxAreaErrorMM2=out['maxAbsoluteAreaErrorMM2'],coincidentEvents=len(coincident),maxPointDeviationMM=max(x['pointDeviationUpperMM']for x in coincident),parserSHA256=out['parserSHA256'])))