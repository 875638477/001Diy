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

def polygon_from_vertices(vs, step_degrees=.5):
 out=[]
 for i,(end,rr) in enumerate(vs):
  start=vs[i-1][0]
  if not rr:
   out.append(end);continue
  r=abs(rr);dx=end[0]-start[0];dy=end[1]-start[1];d=math.hypot(dx,dy)
  assert d<=2*r+.001,(d,r)
  h=math.sqrt(max(0,r*r-d*d/4));mx=(start[0]+end[0])/2;my=(start[1]+end[1])/2
  options=[]
  for sign in [-1,1]:
   cx=mx+sign*(-dy/d)*h;cy=my+sign*(dx/d)*h
   a0=math.atan2(start[1]-cy,start[0]-cx);a1=math.atan2(end[1]-cy,end[0]-cx)
   delta=(a1-a0+math.pi)%(2*math.pi)-math.pi
   xx=math.cos(a0+delta/2)
   if (rr>0 and xx<0) or(rr<0 and xx>0):options.append((cx,cy,a0,delta))
  assert len(options)==1,(start,end,rr,options)
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
