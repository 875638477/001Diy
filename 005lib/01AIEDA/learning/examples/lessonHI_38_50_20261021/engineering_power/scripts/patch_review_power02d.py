from pathlib import Path
import shutil
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_power')
p=R/'scripts/review_power02d.py'
shutil.copyfile(R/'readouts/review_power02d.json',R/'readouts/review_power02d_failed_parser_v1.json')
s=p.read_text()
s=s.replace("sum(len(c['pins']) for c in a['placements'])==272","sum(sum(bool(p['number']) and not p['mechanical'] for p in c['pins']) for c in a['placements'])==272")
s=s.replace("for p in vv[0]['pads']}","for p in vv[0]['pads'] if p['figure'] and p['figure']!='NULL'}")
s=s.replace("row['allowEtch']==(row['layer'] in g['allowed_layers'])","bool(row['allowEtch'])==(row['layer'] in g['allowed_layers'])")
start=s.index("  p=ps[0];outer=")
end=s.index("  corridor=",start)
s=s[:start]+"""  p=ps[0]
  def cadpoly(vs):
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
    steps=max(1,math.ceil(abs(delta)/math.radians(.5)))
    out.extend([[cx+r*math.cos(a0+delta*j/steps),cy+r*math.sin(a0+delta*j/steps)] for j in range(1,steps+1)])
   q=Polygon(out);assert q.is_valid
   return q
  outer=cadpoly(p['vertices']);holes=[cadpoly(h) for h in p['holes']]
  plane=outer.difference(unary_union(holes))
  check(variant+'.sampledArcAreaMatchesNative',abs(plane.area-p['area'])<.01,dict(sampled=plane.area,native=p['area'],bound=.01,arcStep_deg=.5))
  free=outer.buffer(-.0001).difference(unary_union(holes).buffer(.0001))
""" + s[end:]
s=s.replace("Plane outerpolygon minus conservatively enlarged holeAABBs, no field/current simulation.","OfficialaxlPolyFromDB radius applies previous->current vertex, positivearc leftofYaxis/negative right, quadrantlimited. Sample.5deg, nativearea agreement<.01mm2, outwardvoidbuffer.0001mm conservative. No field/current simulation.")
s=s.replace("# Conservative inner/bottom plane hole bounds: extra2*radius per hole contains any arc, can overreject but cannot invent copper.","# Official radius convention used; old full-holeAABB overestimated L-shapedsensevoid and false-rejected localcopper.")
p.write_text(s)
shutil.copyfile(Path(r'C:\Program0\Cadence\SPB172\share\pcb\examples\skill\DOC\FUNCS\axlPolyFromDB.txt'),R/'source/axlPolyFromDB.txt')
print('patchedparser')
