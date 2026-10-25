import pathlib,json,math,sys
H=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021");R=H/"engineering_mcu"
sys.path.insert(0,str(H/"tooling/packages"))
from shapely.geometry import Polygon
def flatten(vs,err=.00002):
 out=[];records=[]
 for i,z in enumerate(vs):
  p0=vs[(i-1)%len(vs)][0];p1=z[0];rad=float(z[1])
  if abs(rad)<1e-10:out.append(p1);continue
  r=abs(rad);dx=p1[0]-p0[0];dy=p1[1]-p0[1];d=math.hypot(dx,dy)
  if d>2*r+1e-4:raise ValueError((p0,p1,rad,d))
  mid=[(p0[k]+p1[k])/2 for k in range(2)];h=math.sqrt(max(0,r*r-d*d/4))
  cs=[[mid[0]+s*(-dy/d)*h,mid[1]+s*(dx/d)*h] for s in(-1,1)]
  choices=[]
  for c in cs:
   a=math.atan2(p0[1]-c[1],p0[0]-c[0]);b=math.atan2(p1[1]-c[1],p1[0]-c[0]);delta=(b-a+math.pi)%(2*math.pi)-math.pi
   xside=math.cos(a+delta/2)
   # Cadence official polygon radius sign: positive arc left of vertical axis through center; negative right.
   valid=xside*rad<=1e-9
   choices.append((valid,c,a,delta,xside))
  good=[x for x in choices if x[0]]
  if len(good)!=1:
   sagitta=r-math.sqrt(max(0,r*r-d*d/4))
   if sagitta<=err:
    out.append(p1);records.append({"start":p0,"end":p1,"radius":rad,"linearizedSubToleranceAmbiguity":sagitta});continue
   raise ValueError(("ambiguous",p0,p1,rad,choices))
  _,c,a,delta,_=good[0];steps=max(2,math.ceil(abs(delta)/(2*math.acos(max(-1,min(1,1-err/r))))))
  for k in range(1,steps+1):t=a+delta*k/steps;out.append([c[0]+r*math.cos(t),c[1]+r*math.sin(t)])
  records.append({"start":p0,"end":p1,"radius":rad,"center":c,"angle":delta})
 return out,records
def poly_from_native(p):
 outer,arcs=flatten(p["vertices"]);holes=[];ha=[]
 for hole in p.get("holes") or[]:
  # holes is vertices list in normalized, not polygon object.
  if isinstance(hole,dict):vs=hole["vertices"]
  else:vs=hole
  h,a=flatten(vs);holes.append(h);ha+=a
 return Polygon(outer,holes),arcs+ha
if __name__=="__main__":
 result={}
 for v in("4L","2L"):
  nf=H/f"inventory/checkpoints/mcu_{v}_b006/normalized.json";n=json.loads(nf.read_text(encoding="utf-8"));rows=[]
  for p in n["planes"]:
   sh,arcs=poly_from_native(p);rows.append({"layer":p["layer"],"nativeArea":p["area"],"flattenedArea":sh.area,"absoluteAreaDifference":abs(sh.area-p["area"]),"valid":sh.is_valid,"nativeHoleCount":len(p.get("holes") or[]),"arcCount":len(arcs)})
  result[v]=rows
 (R/"review/mcu6_native_polygon_flattening_check.json").write_text(json.dumps(result,indent=2),encoding="utf-8");print(json.dumps(result))
