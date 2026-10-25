import pathlib,json,sys,math,csv,re,heapq,hashlib,datetime,shutil
R=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu");H=R.parent
sys.path.insert(0,str(H/"tooling/packages"));sys.path.insert(0,str(R))
from shapely.geometry import LineString,Point,box
from shapely.ops import unary_union
from native_polygon_geometry import poly_from_native
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def key(layer,p):return(layer,round(float(p[0]),6),round(float(p[1]),6))
def pin(n,ref,pin):
 c=next(c for c in n["placements"] if c["ref"]==ref);return next(p for p in c["pins"] if p["number"]==pin)["xy"]
def geoms(s):
 if s.is_empty:return[]
 if s.geom_type=="LineString":return[s]
 return[x for g in getattr(s,"geoms",[]) for x in geoms(g)]
def copper_ground(n,logs,layer):
 pieces=[poly_from_native(p)[0] for p in n["planes"] if p["net"]=="GND" and p["layer"]=="ETCH/"+layer]
 pieces +=[LineString(z["startEnd"]).buffer(z["width"]/2,quad_segs=64) for z in n["routes"] if z["net"]=="GND" and z["layer"]=="ETCH/"+layer]
 prows=list(csv.DictReader((logs/"physical_pad_layers.tsv").open(encoding="utf-8"),delimiter="\t"))
 # Native physical layer records qualify the pad on the actual reference layer.
 for v in n["vias"]:
  if v["net"]!="GND":continue
  rows=[r for r in prows if r["kind"]=="VIA" and r["layer"]=="ETCH/"+layer and r["figure"]=="CIRCLE" and math.dist([float(x) for x in re.findall(r"[-+]?(?:\d*\.\d+|\d+)",r["xy"])],v["xy"])<1e-6]
  if rows:pieces.append(Point(v["xy"]).buffer(v["drill"]*0+ .3,quad_segs=128))
 # Include pin copper only when native map has that actual etch layer. Circle/rectangle/oblong exact for teaching pads.
 omitted=[]
 for c in n["placements"]:
  for p in c["pins"]:
   if p["net"]!="GND":continue
   rows=[r for r in prows if r["kind"]=="PIN" and r["layer"]=="ETCH/"+layer and r["figure"]!="NULL" and math.dist([float(x) for x in re.findall(r"[-+]?(?:\d*\.\d+|\d+)",r["xy"])],p["xy"])<1e-6]
   if not rows:continue
   bb=p["padBBox"];fig=rows[0]["figure"].upper();dx=bb[1][0]-bb[0][0];dy=bb[1][1]-bb[0][1];cx=(bb[0][0]+bb[1][0])/2;cy=(bb[0][1]+bb[1][1])/2
   if fig=="CIRCLE" and abs(dx-dy)<1e-5:pieces.append(Point(cx,cy).buffer(dx/2,quad_segs=128))
   elif fig in("RECTANGLE","SQUARE"):pieces.append(box(*bb[0],*bb[1]))
   elif fig=="OBLONG":
    radius=min(dx,dy)/2
    a=[cx-max(0,(dx-dy)/2),cy-max(0,(dy-dx)/2)];b=[cx+max(0,(dx-dy)/2),cy+max(0,(dy-dx)/2)]
    pieces.append(LineString([a,b]).buffer(radius,quad_segs=128))
   else:omitted.append({"pin":c["ref"]+"."+p["number"],"figure":fig})
 return unary_union(pieces),omitted
def graph_path(n,net,src,dst):
 routes=[z for z in n["routes"] if z["net"]==net and z["kind"]=="line"]
 adj={};edgeinfo={}
 def add(a,b,length,vertical,width=None):
  adj.setdefault(a,[]).append((b,length));adj.setdefault(b,[]).append((a,length))
  edgeinfo[frozenset((a,b))]={"from":[a[1],a[2]],"to":[b[1],b[2]],"layer":a[0] if not vertical else"THROUGH","planarLength":0 if vertical else length,"viaCount":1 if vertical else 0,"width":width}
 for layer in("TOP","BOTTOM"):
  rs=[z for z in routes if z["layer"]=="ETCH/"+layer]
  for line in geoms(unary_union([LineString(z["startEnd"]) for z in rs])):
   cs=list(line.coords)
   for a,b in zip(cs,cs[1:]):
    target=LineString([a,b]);matches=[z for z in rs if target.difference(LineString(z["startEnd"]).buffer(.000001)).length<.000001]
    width=max([z["width"] for z in matches],default=None);add(key(layer,a),key(layer,b),math.dist(a,b),False,width)
 for via in n["vias"]:
  if via["net"]==net:
   a=key("TOP",via["xy"]);b=key("BOTTOM",via["xy"])
   if a in adj and b in adj:add(a,b,0,True)
 resolve=lambda s: s if isinstance(s[0],(int,float)) else pin(n,*s)
 start=key("TOP",resolve(src));end=key("TOP",resolve(dst));dist={start:0};prev={};q=[(0,start)]
 while q:
  d,x=heapq.heappop(q)
  if d!=dist[x]:continue
  if x==end:break
  for y,w in adj.get(x,[]):
   nd=d+w
   if nd<dist.get(y,float("inf"))-1e-12:dist[y]=nd;prev[y]=x;heapq.heappush(q,(nd,y))
 if end not in dist:return{"reachable":False,"from":src,"to":dst}
 es=[];x=end
 while x!=start:y=prev[x];es.append(edgeinfo[frozenset((x,y))]);x=y
 es.reverse()
 return{"reachable":True,"from":src,"to":dst,"net":net,"planarLength":sum(e["planarLength"] for e in es),"throughViaCount":sum(e["viaCount"] for e in es),"planarByLayer":{l:sum(e["planarLength"] for e in es if e["layer"]==l) for l in("TOP","BOTTOM")},"edges":es}
def run(variant,checkpoint,nf_override=None):
 cp=H/"inventory/checkpoints"/checkpoint;nf=pathlib.Path(nf_override) if nf_override else cp/"normalized.json";n=json.loads(nf.read_text(encoding="utf-8"));logs=pathlib.Path(n["readbackDirectory"])
 archive=R/"review/inputs"/checkpoint;archive.mkdir(parents=True,exist_ok=True);shutil.copy2(nf,archive/"normalized.json")
 requests={"A_DP_ENTRY":("USB_DP",("J2","A6"),("U4","6")),"A_DM_ENTRY":("USB_DM",("J2","A7"),("U4","4")),"B_DP_ENTRY":("USB_DP",("J2","B6"),("U4","6")),"B_DM_ENTRY":("USB_DM",("J2","B7"),("U4","4")),"DP_U4_FLOW":("USB_DP",("U4","6"),("U4","1")),"DM_U4_FLOW":("USB_DM",("U4","4"),("U4","3")),"DP_PROTECTED":("USB_DP",("U4","1"),("R5","2")),"DM_PROTECTED":("USB_DM",("U4","3"),("R6","2")),"DP_SHARED":("PA12_SHARED",("R5","1"),("U1","33")),"DM_SHARED":("PA11_SHARED",("R6","1"),("U1","32")),"DP_DNP_STUB":("PA12_SHARED",("R5","1"),("R12","1")),"DM_DNP_STUB":("PA11_SHARED",("R6","1"),("R13","1")),"DP_PULLUP_TEE_FROM_U4":("USB_DP",("U4","1"),("R11","2"))}
 requests.update({"DP_PULLUP_TEE":("USB_DP",(40.455 if variant=="4L" else 40.905,14.6),("R11","2")),"A_DP_TO_SERIES":("USB_DP",("J2","A6"),("R5","2")),"A_DM_TO_SERIES":("USB_DM",("J2","A7"),("R6","2")),"B_DP_TO_SERIES":("USB_DP",("J2","B6"),("R5","2")),"B_DM_TO_SERIES":("USB_DM",("J2","B7"),("R6","2"))})
 paths={name:graph_path(n,*args) for name,args in requests.items()}
 grounds={l:copper_ground(n,logs,l) for l in(("L2","L3") if variant=="4L" else("TOP","BOTTOM"))}
 for path in paths.values():
  coverage=[]
  for e in path.get("edges",[]):
   if e["layer"]=="THROUGH":continue
   ref=("L2" if e["layer"]=="TOP" else"L3") if variant=="4L" else("BOTTOM" if e["layer"]=="TOP" else"TOP")
   ground,omitted=grounds[ref];line=LineString([e["from"],e["to"]]);missing=line.difference(ground);gaps=geoms(missing)
   coverage.append({"signalLayer":e["layer"],"reference":ref,"from":e["from"],"to":e["to"],"width":e["width"],"length":line.length,"projectedCenterlineUncoveredLength":sum(g.length for g in gaps),"uncoveredPieces":[list(g.coords) for g in gaps],"stripAreaCoverageRatio":None if not e["width"] else line.buffer(e["width"]/2,quad_segs=64).intersection(ground).area/line.buffer(e["width"]/2,quad_segs=64).area})
  path["referenceCoverage"]=coverage;path["totalProjectedCenterlineUncoveredLength"]=sum(e["projectedCenterlineUncoveredLength"] for e in coverage)
 lengthSummary={k:{z:p.get(z) for z in("reachable","planarLength","throughViaCount","planarByLayer","totalProjectedCenterlineUncoveredLength")} for k,p in paths.items()}
 out={"status":"INDEPENDENT_NATIVE_USB_CENTERLINE_AND_REFERENCE_PROJECTION_REVIEW","variant":variant,"checkpoint":str(cp),"snapshotSHA256":sha(nf),"readback":str(logs),"sourceFiles":[{"path":str(p),"sha256":sha(p)} for p in[nf,logs/"physical_pad_layers.tsv",logs/"stackup_full.tsv"]],"method":"Noded actual centerline graph shortestterminalpath; no unused leafbacktracking; PTHsignalvia planargraph edgeweight0 while separate count recorded. ActualfilledGNDpolygon withnativearcs + same-layerGNDcline + qualifiednativepad copper. Projectioncoverage isgeometryonly; noEM/simulation orguarantee currentfollowsnearestpoint.","limitations":["Copperstackbarrelvia physical time added separately, not hidden innative planarphase","Zero projectedgap alone not full field/impedance orEMI validation","Omitted unsupported padfigures listed; references outside suchpads conservative; generatedcopper remainscurrent native requirement"],"unsupportedGNDPadFigures":{l:x[1] for l,x in grounds.items()},"lengthSummary":lengthSummary,"paths":paths}
 (R/f"review/usb_native_{checkpoint}.json").write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8");print(json.dumps({"checkpoint":checkpoint,"paths":lengthSummary},ensure_ascii=True))
if __name__=="__main__":run(sys.argv[1],sys.argv[2],sys.argv[3] if len(sys.argv)>3 else None)
