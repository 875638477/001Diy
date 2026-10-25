"""Independent geometry checks against the original engineering drawing transcription.
No Cadence process launches. Input comes from fresh readonly native reopen.
"""
import pathlib,csv,json,math,re,hashlib,sys,html
B=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\examples\lesson10_connector_20261018")
spec=json.loads((B/"spec.json").read_text(encoding="utf-8"))
checks=[]
def ok(label,cond,detail=None):
 checks.append({"check":label,"pass":bool(cond),"detail":detail})
 if not cond:raise AssertionError(label+": "+str(detail))
def close(a,b,t=.00051):return abs(float(a)-float(b))<=t
def un(s):return s.strip().strip('"')
def rows(p):
 with p.open(encoding="utf-8") as f:return [{k:un(v) if v is not None else None for k,v in r.items()} for r in csv.DictReader(f,delimiter="\t")]
def sh(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
R=B/"logs/reopen_package";RB=B/"logs/reopen_board"
ok("source_pdf_sha",sh(B/"source/usb4105.pdf")==spec["source_sha256"])
for folder in [R,RB]:
 t=(folder/"summary.txt").read_text(encoding="utf-8")
 ok(folder.name+"_complete","L10_READ COMPLETE" in t,t)
 ok(folder.name+"_units",'("millimeters" 3)' in t)
 ok(folder.name+"_two_layer_order",re.findall(r'STACK "(TOP|BOTTOM|L\d+)" "CONDUCTOR"',t)==["TOP","BOTTOM"],t)
pp=rows(R/"pins.tsv");bp=rows(RB/"pins.tsv");pg=rows(R/"geometry.tsv");bg=rows(RB/"geometry.tsv");bs=rows(RB/"symbols.tsv")
ok("package_native_rows_18x6",len(pp)==108,len(pp))
ok("board_native_rows_54x6",len(bp)==324,len(bp))
expected=[]
for p in spec["lands"]:expected.append(dict(p,mechanical=False,kind="smd"))
for p in spec["shell"]:expected.append(dict(p,w=p["land"][0],h=p["land"][1],mechanical=False,kind="shell"))
for x,y in spec["npth"]:expected.append({"number":"","x":x,"y":y,"w":0,"h":0,"mechanical":True,"kind":"npth"})
def find(ps,e,x,y,layer):
 rs=[r for r in ps if r["number"]==e["number"] and close(r["x"],x) and close(r["y"],y) and r["layer"]==layer]
 ok("unique_pin_"+e["number"]+"_"+layer+"_"+str((x,y)),len(rs)==1)
 return rs[0]
def pincheck(ps,e,x,y,mirror,tag,angle=0):
 def size(w,h):return (h,w) if angle==90 else (w,h)
 for layer in ["ETCH/TOP","ETCH/BOTTOM"]:
  r=find(ps,e,x,y,layer)
  ok(tag+"_relative_xy_"+e["number"]+"_"+layer,close(r["relx"],e["x"]) and close(r["rely"],e["y"]))
  ok(tag+"_pin_rotation_"+e["number"]+"_"+layer,close(r["rotation"],angle) and (r["mirrored"]=="t")==mirror)
  ok(tag+"_mechanical_"+e["number"]+"_"+layer,(r["mechanical"]=="t")==e["mechanical"])
  active=e["kind"]=="shell" or (e["kind"]=="smd" and layer==("ETCH/BOTTOM" if mirror else "ETCH/TOP"))
  ew,eh=size(e["w"],e["h"]) if active else (0,0)
  ok(tag+"_copper_size_"+e["number"]+"_"+layer,close(r["w"],ew) and close(r["h"],eh),r)
  ok(tag+"_copper_polygon_presence_"+e["number"]+"_"+layer,(r["poly_bbox"]!="nil")==active)
  if active:
   nums=list(map(float,re.findall(r'-?\d+(?:\.\d+)?',r["poly_bbox"])))
   ok(tag+"_actual_polygon_bbox_"+e["number"]+"_"+layer,len(nums)==4 and all(close(a,b) for a,b in zip(nums,[x-ew/2,y-eh/2,x+ew/2,y+eh/2])),nums)
  if e["kind"]=="smd":
   ok(tag+"_copper_side_"+e["number"]+"_"+layer,(r["figure"]=="RECTANGLE")==active)
  elif e["kind"]=="shell":
   ok(tag+"_shell_figure_"+e["number"]+"_"+layer,r["figure"] in ["OBLONG","OBLONG_X"])
   ok(tag+"_shell_slot_"+e["number"]+"_"+layer,r["hole_type"] in ["OVAL_SLOT","oval slot"] and close(r["drill_x"],e["hole"][0]) and close(r["drill_y"],e["hole"][1]) and r["plating"]=="PLATED")
  else:
   ok(tag+"_npth_no_copper_"+layer+str(x),r["figure"]=="NULL")
   ok(tag+"_npth_drill_"+layer+str(x),close(r["drill_diameter"],.65) and r["plating"]=="NON_PLATED")
 for side in ["TOP","BOTTOM"]:
  for kind in ["SOLDERMASK","PASTEMASK"]:
   r=find(ps,e,x,y,f"PIN/{kind}_{side}")
   if e["kind"]=="smd":
    active=side==("BOTTOM" if mirror else "TOP")
    delta=.1 if kind=="SOLDERMASK" else 0
    ew,eh=size(e["w"]+delta,e["h"]+delta) if active else (0,0)
    ok(tag+"_"+kind+"_"+e["number"]+"_"+side,(r["figure"]=="RECTANGLE")==active and close(r["w"],ew) and close(r["h"],eh))
   elif e["kind"]=="shell":
    ew,eh=size(e["w"]+.1,e["h"]+.1)
    ok(tag+"_"+kind+"_"+e["number"]+"_"+side,(r["figure"] in ["OBLONG","OBLONG_X"] and close(r["w"],ew) and close(r["h"],eh)) if kind=="SOLDERMASK" else (r["figure"]=="NULL" and close(r["w"],0) and close(r["h"],0)))
   else:
    ok(tag+"_"+kind+"_npth_"+side+str(x),(r["figure"]=="CIRCLE" and close(r["w"],.75) and close(r["h"],.75)) if kind=="SOLDERMASK" else (r["figure"]=="NULL" and close(r["w"],0) and close(r["h"],0)))

for e in expected:pincheck(pp,e,e["x"],e["y"],False,"package")
for layer in ["REF DES/SILKSCREEN_TOP","REF DES/ASSEMBLY_TOP","COMPONENT VALUE/ASSEMBLY_TOP"]:
 rs=[r for r in pg if r["type"]=="text" and r["layer"]==layer]
 ok("origin_text_"+layer,len(rs)==1 and close(rs[0]["x"],0) and close(rs[0]["y"],0) and close(rs[0]["rotation"],0))
bounds=[r for r in pg if r["layer"]=="PACKAGE GEOMETRY/PLACE_BOUND_TOP"]
ok("one_placebound",len(bounds)==1)
bound=bounds[0]
ok("true_height_max_3p46","PACKAGE_HEIGHT_MAX" in bound["props"] and "3.46 MM" in bound["props"],bound)
ok("filled_placebound",bound["filled"]=="t")
ko=[r for r in pg if r["layer"]=="ROUTE KEEPOUT/ALL" and r["type"]=="shape"]
ok("two_independent_npth_route_keepouts",len(ko)==2 and all(r["filled"]=="t" for r in ko))
for x,y in spec["npth"]:
 ok("npth_keepout_bounds_"+str(x),any(close(r["x1"],x-.425) and close(r["x2"],x+.425) and close(r["y1"],y-.425) and close(r["y2"],y+.425) for r in ko))
edges=[r for r in pg if r["layer"]=="PACKAGE GEOMETRY/USER_BOARD_EDGE"]
ok("package_boardedge",len(edges)==1 and close((float(edges[0]["y1"])+float(edges[0]["y2"]))/2,spec["board_edge_y"]))
ok("three_pcb_instances",len(bs)==3,bs)
transforms=[(-15,0,0,False),(26.325,12,90,False),(15,0,0,True)]
for sx,sy,a,m in transforms:
 ss=[r for r in bs if close(r["x"],sx) and close(r["y"],sy) and close(r["rotation"],a) and (r["mirrored"]=="t")==m]
 ok("instance_"+str((sx,sy,a,m)),len(ss)==1 and int(ss[0]["pins"])==18)
 def tr(x,y):
  if m:x=-x
  if a==90:x,y=-y,x
  return x+sx,y+sy
 for e in expected:
  x,y=tr(e["x"],e["y"]);pincheck(bp,e,x,y,m,str((sx,sy,a,m)),a)
 # Native helper line must align to real board edge at bottom y=-3.675 or right x=30.
 ee=[r for r in bg if r["layer"]=="PACKAGE GEOMETRY/USER_BOARD_EDGE" and close((float(r["x1"])+float(r["x2"]))/2,tr(0,-3.675)[0]) and close((float(r["y1"])+float(r["y2"]))/2,tr(0,-3.675)[1])]
 ok("instance_edge_alignment_"+str(sx),len(ee)==1,ee)
 hb=[r for r in bg if r["type"]=="shape" and r["layer"]==("PACKAGE GEOMETRY/PLACE_BOUND_BOTTOM" if m else "PACKAGE GEOMETRY/PLACE_BOUND_TOP") and "3.46 MM" in r["props"]]
 ok("instance_height_present_"+str(sx),len(hb)>=1)
 for suffix in ["REF DES/SILKSCREEN_","REF DES/ASSEMBLY_","COMPONENT VALUE/ASSEMBLY_"]:
  text=[r for r in bg if r["type"]=="text" and r["layer"]==suffix+("BOTTOM" if m else "TOP") and close(r["x"],sx) and close(r["y"],sy)]
  ok("instance_text_anchor_"+str(sx)+suffix,len(text)==1)
ok("exact_16_contact_coverage",sorted(c for l in spec["lands"] for c in l["contacts"])==sorted(["A1","A4","A5","A6","A7","A8","A9","A12","B12","B9","B8","B7","B6","B5","B4","B1"]))
# Individual mask windows use +0.05 per edge; nearest neighbours leave 0.10mm mask web.
sp=sorted(spec["lands"],key=lambda p:p["x"])
webs=[b["x"]-a["x"]-(a["w"]+b["w"])/2-.1 for a,b in zip(sp,sp[1:])]
ok("smd_min_mask_web",close(min(webs),.1),webs)

# Check package helper bounds and every placed body height/keepout, not merely global existence.
def bbox_matches(r,v):
 return all(close(r[k],x) for k,x in zip(["x1","y1","x2","y2"],v))
def bounds_after_transform(box,sx,sy,a,m):
 pts=[]
 for x in [box[0][0],box[1][0]]:
  for y in [box[0][1],box[1][1]]:
   if m:x0=-x
   else:x0=x
   y0=y
   if a==90:x0,y0=-y0,x0
   pts.append((x0+sx,y0+sy))
 return [min(x for x,y in pts),min(y for x,y in pts),max(x for x,y in pts),max(y for x,y in pts)]
for sx,sy,a,m in transforms:
 hbox=bounds_after_transform(spec["place_bound"],sx,sy,a,m)
 hs=[r for r in bg if r["type"]=="shape" and r["layer"]==("PACKAGE GEOMETRY/PLACE_BOUND_BOTTOM" if m else "PACKAGE GEOMETRY/PLACE_BOUND_TOP") and bbox_matches(r,hbox)]
 ok("exact_instance_height_shape_"+str(sx),len(hs)==1 and hs[0]["filled"]=="t" and "3.46 MM" in hs[0]["props"],hbox)
 mlayer="PACKAGE GEOMETRY/USER_MATING_"+("BOTTOM" if m else "TOP")
 mb=[r for r in bg if r["layer"]==mlayer and (r["x1"] is not None)]
 target=bounds_after_transform(spec["mating_reference"],sx,sy,a,m)
 # Line bounds include 0.025mm stroke. Four lines unique to this separated instance.
 candidate=[r for r in mb if float(r["x1"])>=target[0]-.026 and float(r["x2"])<=target[2]+.026 and float(r["y1"])>=target[1]-.026 and float(r["y2"])<=target[3]+.026]
 ok("mating_helper_transform_"+str(sx),len(candidate)==4,target)
 for nx,ny in spec["npth"]:
  kb=bounds_after_transform([[nx-.425,ny-.425],[nx+.425,ny+.425]],sx,sy,a,m)
  kr=[r for r in bg if r["layer"]=="ROUTE KEEPOUT/ALL" and r["type"]=="shape" and bbox_matches(r,kb)]
  ok("placed_npth_keepout_"+str((sx,nx)),len(kr)==1 and kr[0]["filled"]=="t",kb)
stacktext=(RB/"summary.txt").read_text(encoding="utf-8")
th=[float(r) for r in re.findall(r'STACK (?:nil|"[^"]+") "(?:CONDUCTOR|DIELECTRIC)" ([0-9.]+)',stacktext)]
ok("teaching_board_total_thickness_0p8",len(th)==3 and close(sum(th),.8),th)

result={"status":"PASS","checks_count":len(checks),"checks":checks,"smd_min_mask_web":min(webs),"native_artifacts":[{"path":str(p),"sha256":sh(p),"bytes":p.stat().st_size} for p in [*sorted((B/"library").glob("*.pad")),B/"library/l10_gct_usb4105_gf_a_12land.dra",B/"library/l10_gct_usb4105_gf_a_12land.psm",B/"lesson10_connector.brd"]],"scope":"software geometry, save/compile/reopen/placement. Not fabrication signoff, full SI/PI/EMI certification, or 3D verification."}
(B/"verification/validation.json").write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
# SVG and PNG from actual reopened native pad rectangles and holes. Not a Cadence screenshot.
sys.path.insert(0,r"D:\001DIY\005lib\01AIEDA\learning\tools\pymupdf_1_28_2");import pymupdf
W=1300;H=1550;scale=55;cx=650;cy=450
def XY(x,y):return cx+scale*x,cy-scale*y
parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">','<rect width="100%" height="100%" fill="#111827"/>']
def rect(x1,y1,x2,y2,fill,stroke="#fff",rx=0,opacity=1):
 x,y=XY(x1,y2);parts.append(f'<rect x="{x}" y="{y}" width="{scale*(x2-x1)}" height="{scale*(y2-y1)}" fill="{fill}" stroke="{stroke}" stroke-width="2" rx="{rx*scale}" opacity="{opacity}"/>')
def text(x,y,t,col="#f1f5f9",sz=19):
 px,py=XY(x,y);parts.append(f'<text x="{px}" y="{py}" font-size="{sz}" fill="{col}" text-anchor="middle" font-family="Arial">{html.escape(t)}</text>')
text(0,7,"Lesson 10 | GCT USB4105-GF-A",sz=32)
text(0,6.4,"Top / component side | native reopened geometry",sz=22)
rect(-6,-15.675,6,-3.675,"#28364b","#64748b",opacity=.5)
rect(-4.47,-3.675,4.47,3.675,"none","#38bdf8")
rect(-5.12,-4,5.12,4.555,"none","#a78bfa")
for e in expected:
 r=next(r for r in pp if r["number"]==e["number"] and close(r["x"],e["x"]) and close(r["y"],e["y"]) and r["layer"]=="ETCH/TOP")
 x,y=float(r["x"]),float(r["y"])
 if e["kind"]!="npth":
  w,h=float(r["w"]),float(r["h"]);rect(x-w/2,y-h/2,x+w/2,y+h/2,"#eab308","#fef08a",.5 if e["kind"]=="shell" else 0)
  if e["kind"]=="shell":
   a,b=e["hole"];rect(x-a/2,y-b/2,x+a/2,y+b/2,"#111827","#fff",.3);text(x,y-1.4,e["number"],sz=17)
 else:
  px,py=XY(x,y);parts.append(f'<circle cx="{px}" cy="{py}" r="{scale*.325}" fill="#111827" stroke="#f8fafc" stroke-width="3"/>')
  text(x,y-.65,"NPTH 0.65",sz=16)
for i,p in enumerate(spec["lands"]):
 text(p["x"],4.9+(i%2)*.35,p["number"],"#fef08a",13)
px,py=XY(-7,-3.675);qx,qy=XY(7,-3.675);parts.append(f'<line x1="{px}" y1="{py}" x2="{qx}" y2="{qy}" stroke="#fb7185" stroke-width="4"/>')
text(0,-4.35,"PCB EDGE y=-3.675 | opening -Y / plug insertion +Y","#fb7185",20)
text(0,-8.0,"12 x 12 mm project mating reserve","#94a3b8",20)
text(0,-8.6,"Reference helper, not full plug / cable 3D clearance","#94a3b8",19)
text(0,0,"J* / VALUE @ origin",sz=22)
text(0,-1,"Body 8.94 x 7.35 mm | height max 3.46 mm",sz=20)
text(0,-17,"12 copper lands / 16 contacts + 4 shell stakes + 2 NPTH",sz=23)
text(0,-17.7,"Source: GCT USB4105 Rev B4 sheet 1 | all dimensions mm",sz=19)
parts.append("</svg>")
svg="\n".join(parts)
(B/"preview.svg").write_text(svg,encoding="utf-8")
d=pymupdf.open(stream=svg.encode(),filetype="svg")
d[0].get_pixmap(matrix=pymupdf.Matrix(1.3,1.3)).save(B/"preview.png")
print(json.dumps({"status":"PASS","checks":len(checks),"preview":str(B/"preview.png")},indent=2))
