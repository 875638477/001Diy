"""Read-only Cadence polygon conversion.
Source: installation official axlPolyFromDB.txt, copied to ../source.
Radius belongs to previous->current point. Positive arc is left of local Y-axis;
negative is right. Cadence splits arcs at quadrant boundaries.
No Cadence process/API calls. Requires caller to make Shapely available.
Half-degree chords are an approximation: use conservative_plane(.0001) for
clearance and compare area against exported native area. Not a field solver.
"""
import math
from shapely.geometry import Polygon
from shapely.ops import unary_union

ROUNDED_ARC_FLATTENED = []
COINCIDENT_ARC_ENDPOINTS = []

def polygon_from_vertices(vs, step_degrees=.5):
 out=[]
 for i,(end,rr) in enumerate(vs):
  start=vs[i-1][0]
  if not rr:
   out.append(end);continue
  r=abs(rr);dx=end[0]-start[0];dy=end[1]-start[1];d=math.hypot(dx,dy)
  assert d<=2*r+.001,(d,r)
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
  h=math.sqrt(max(0,r*r-d*d/4));mx=(start[0]+end[0])/2;my=(start[1]+end[1])/2
  options=[]
  for sign in [-1,1]:
   cx=mx+sign*(-dy/d)*h;cy=my+sign*(dx/d)*h
   a0=math.atan2(start[1]-cy,start[0]-cx);a1=math.atan2(end[1]-cy,end[0]-cx)
   delta=(a1-a0+math.pi)%(2*math.pi)-math.pi
   xx=math.cos(a0+delta/2)
   if (rr>0 and xx<0) or(rr<0 and xx>0):options.append((cx,cy,a0,delta))
  if len(options)!=1:
   # Near a quadrant tangent the rounded endpoints can make left/right ambiguous.
   # Flatten only if endpoint-rounding plus full minor-arc sagitta is <=0.0001mm, bounded
   # than conservative_plane's 0.0001mm erosion/expansion. Preserve audit.
   sag=r-math.sqrt(max(0,r*r-d*d/4))
   point_bound=.0001/math.sqrt(2)+sag
   if point_bound<=.0001:
    ROUNDED_ARC_FLATTENED.append(dict(start=start,end=end,radius=rr,sagitta_mm=sag,exportQuantumMM=.0001,pointDeviationUpperMM=point_bound,action='Flatten only ambiguous short tangent arc under combined endpoint-rounding+sagitta<=0.0001mm bound; retain entire polygon/hole'))
    out.append(end);continue
   raise AssertionError((start,end,rr,options,sag))
  cx,cy,a0,delta=options[0]
  assert abs(delta)<=math.pi/2+.003,delta
  steps=max(1,math.ceil(abs(delta)/math.radians(step_degrees)))
  out.extend([[cx+r*math.cos(a0+delta*j/steps),cy+r*math.sin(a0+delta*j/steps)] for j in range(1,steps+1)])
 q=Polygon(out);assert q.is_valid
 return q

def plane_from_native(record, step_degrees=.5):
 outer=polygon_from_vertices(record['vertices'],step_degrees)
 holes=[polygon_from_vertices(h,step_degrees) for h in record['holes']]
 return outer.difference(unary_union(holes))

def conservative_plane(record,tolerance_mm=.0001,step_degrees=.5):
 outer=polygon_from_vertices(record['vertices'],step_degrees)
 holes=[polygon_from_vertices(h,step_degrees) for h in record['holes']]
 return outer.buffer(-tolerance_mm).difference(unary_union(holes).buffer(tolerance_mm))
