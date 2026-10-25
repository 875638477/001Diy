"""Capture XML cache-origin rebase. Never runs CAD.
Only changes coordinate representation for zero rotation/mirror inputs.
Nonzero poses are explicitly rejected: the legacy pure-O+RM model omits native bbox offsets."""
from pathlib import Path
import argparse,collections,copy,csv,hashlib,json,xml.etree.ElementTree as E
def D(e):return e.find("Defn").attrib if e is not None and e.find("Defn") is not None else {}
def j(v):return json.dumps(v,ensure_ascii=True,separators=(",",":"))
def c(e):return [e.tag,sorted(e.attrib.items()),e.text if e.text and e.text.strip() else "",[c(x) for x in e],e.tail if e.tail and e.tail.strip() else ""]
def h(e):return hashlib.sha256(j(c(e)).encode()).hexdigest().upper()
def fs(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def L(s):return s.replace("/","\\").upper()
def rm(x,y,a):
 if int(a.get("mirror","0")):x=-x
 r=int(a.get("rotation","0"))%4
 if r==1:x,y=y,-x
 elif r==2:x,y=-x,-y
 elif r==3:x,y=-y,x
 return x,y
def absolute(x,y,a):
 x,y=rm(x,y,a);return x+int(a["locX"]),y+int(a["locY"])
# Ordered point pairs for the exact primitive vocabulary currently supported.
# Font metrics, 3D model strings and electrical properties are never coordinates.
PAIRS={
 "SymbolBBox":[("x1","y1"),("x2","y2")],
 "SymbolPinScalar":[("startX","startY"),("hotptX","hotptY")],
 "SymbolPinBus":[("startX","startY"),("hotptX","hotptY")],
 "SymbolDisplayProp":[("locX","locY")],
 "Line":[("x1","y1"),("x2","y2")],
 "Rect":[("x1","y1"),("x2","y2")],
 "Ellipse":[("x1","y1"),("x2","y2")],
 "Arc":[("x1","y1"),("x2","y2"),("startX","startY"),("endX","endY")],
 "PolygonPoint":[("x","y")],"PolylinePoint":[("x","y")],"BezierPoint":[("x","y")],
 "CommentText":[("locX","locY"),("x1","y1"),("x2","y2")]
}
COORDNAMES={v for pairs in PAIRS.values() for pair in pairs for v in pair}|{"hotX","hotY","left","top","right","bottom"}
def coordinates(view):
 # Return actual mutable attribute dictionaries and ordered known pairs.
 result=[]
 def walk(e,path):
  dd=e.find("Defn")
  if dd is not None:
   present=set(dd.attrib)&COORDNAMES
   if present:
    assert e.tag in PAIRS,("Unknown coordinate-bearing tag; review required",path,e.tag,dd.attrib)
    used=set()
    for x,y in PAIRS[e.tag]:
     if x in dd.attrib or y in dd.attrib:
      assert x in dd.attrib and y in dd.attrib,("Partial coordinate pair",path,x,y)
      int(dd.get(x));int(dd.get(y));result.append((dd,x,y,path));used|={x,y}
    assert present<=used,("Unclassified coordinate",path,present-used)
  # A nested SymbolVector has a second local frame and is deliberately unsupported.
  assert e.tag not in {"SymbolVector","Bitmap","PinDisplayProp"},("Unvalidated nested frame/display semantics",path,e.tag)
  for i,z in enumerate(e):
   if z.tag!="Defn":walk(z,path+"/"+z.tag+"["+str(i)+"]")
 walk(view,view.tag);return result
def shift_view(view,rx,ry):
 for dd,x,y,path in coordinates(view):
  dd.set(x,str(int(dd.get(x))-rx));dd.set(y,str(int(dd.get(y))-ry))
def view_index(r):
 out={}
 for pkg in r.findall("./Cache/Package"):
  pd=D(pkg)
  for ci,lp in enumerate(pkg.findall("LibPart")):
   for view in lp:
    if view.tag not in {"NormalView","ConvertView"}:continue
    key=(L(pd.get("sourceLibName","")),pd["name"],D(lp).get("CellName","")+D(view).get("suffix",""))
    assert key not in out,("Duplicate graphic identity",key)
    out[key]={"view":view,"pkg":pkg,"cell_index":ci,"view_tag":view.tag,"cell_name":D(lp).get("CellName",""),"libpart":lp}
 return out
def instance_key(inst):
 return (L(D(inst).get("libName","")),D(inst).get("pkgName",""),inst.find("GraphicName/Defn").get("name"))
def projection(view,inst):
 # Independent forward absolute projection of every supported local point;
 # full ordered non-coordinate view data remain in the clone.
 q=copy.deepcopy(view);ia=D(inst)
 for dd,x,y,path in coordinates(q):
  xx,yy=absolute(int(dd.get(x)),int(dd.get(y)),ia);dd.set(x,str(xx));dd.set(y,str(yy))
 return h(q)
def override_projection(inst):
 out=[]
 for pi,pin in enumerate(inst):
  if pin.tag not in {"PortInstScalar","PortInstBus"}:continue
  pd=D(pin);r={"tag":pin.tag,"position":pd.get("position",""),"name":pd.get("name","")}
  q=copy.deepcopy(pin);qd=q.find("Defn")
  for x,y in [("startX","startY"),("hotptX","hotptY")]:
   if x in qd.attrib or y in qd.attrib:
    assert x in qd.attrib and y in qd.attrib
    xx,yy=absolute(int(qd.get(x)),int(qd.get(y)),D(inst));qd.set(x,str(xx));qd.set(y,str(yy))
  r["absolute_complete_pin_sha256"]=h(q);out.append(r)
 return out
def dp_projection(inst):
 out=[];o=D(inst)
 for index,dp in enumerate(inst.findall("PartInstDisplayProp")):
  q=copy.deepcopy(dp);dd=q.find("Defn")
  # Native confirmed: PartInst DisplayProp absolute anchor is O+local,
  # without applying instance rotation/mirror.
  dd.set("locX",str(int(o["locX"])+int(dd.get("locX","0"))));dd.set("locY",str(int(o["locY"])+int(dd.get("locY","0"))))
  out.append({"index":index,"name":D(dp).get("name",""),"absolute_complete_dp_sha256":h(q)})
 return out
P=argparse.ArgumentParser();P.add_argument("--input",type=Path,required=True);P.add_argument("--output",type=Path,required=True);P.add_argument("--grid",type=int,default=5);P.add_argument("--expected-input-sha",required=True);P.add_argument("--native-frame-calibration",type=Path,required=True)
A=P.parse_args();assert A.grid>0 and A.grid%2==1
calibration=json.loads(A.native_frame_calibration.read_text(encoding="utf-8-sig"))
assert calibration.get("status")=="PASS" and calibration.get("point_transform")=="MIRROR_X_THEN_CLOCKWISE_QUARTER_TURN" and calibration.get("partinst_display_prop_transform")=="ORIGIN_PLUS_LOCAL_NO_RM", "Native coordinate-frame calibration is required; do not infer from appearance"
assert calibration.get("input_xml_sha256", "").upper()==A.expected_input_sha.upper(), "Calibration must cover this input"
assert A.input.resolve()!=A.output.resolve() and not A.output.exists(),"Fresh separate output required"
input_sha=fs(A.input);assert input_sha==A.expected_input_sha.upper(),"Input lock mismatch"
br=E.parse(A.input).getroot()
nonzero=[D(i).get("dbId") for i in br.findall(".//Page/PartInst") if int(D(i).get("rotation","0")) or int(D(i).get("mirror","0"))]
assert not nonzero, "Legacy zero-pose rebase only: nonzero rotation/mirror requires native per-instance bbox-aware affine compensation, not O+RM(local). IDs="+str(nonzero[:20])
ar=copy.deepcopy(br);bv=view_index(br);av=view_index(ar)
assert set(bv)==set(av)
# Effective placed PortInst hotspots choose the local frame translation.
# All instances sharing the exact cached view must agree; no cache split is guessed.
active_residues=collections.defaultdict(set);active_instances=collections.Counter()
for inst in br.findall(".//Page/PartInst"):
 key=instance_key(inst);pins=[x for x in inst if x.tag in {"PortInstScalar","PortInstBus"}]
 rs={(int(D(x)["hotptX"])%A.grid,int(D(x)["hotptY"])%A.grid) for x in pins}
 assert len(rs)==1,("Effective placed pin residues conflict",D(inst),rs)
 active_residues[key].update(rs);active_instances[key]+=1
residues={};viewrows=[];missing_pin_rows=[]
for key,entry in bv.items():
 v=entry["view"];coordinates(v)
 pins=[x for x in v if x.tag in {"SymbolPinScalar","SymbolPinBus"}]
 if not pins:continue
 rs=active_residues.get(key,set())
 assert len(rs)<=1,("Shared cached view requires different rebase frames",key,rs)
 raw=next(iter(rs)) if rs else (0,0);r=tuple((x+A.grid//2)%A.grid-A.grid//2 for x in raw)
 residues[key]=r
 if r!=(0,0):
  shift_view(av[key]["view"],*r)
  cache_rs=sorted({(int(D(x)["hotptX"])%A.grid,int(D(x)["hotptY"])%A.grid) for x in pins})
  viewrows.append({"package":key[1],"graphic":key[2],"cell_index":entry["cell_index"],"view":entry["view_tag"],"pin_count":len(pins),"placed_instances":active_instances[key],"cache_pin_residues_before":j(cache_rs),"effective_pin_residue_before":j(raw),"local_residue_x":r[0],"local_residue_y":r[1]})
instrows=[];proof=[];beforeinst={D(x)["dbId"]:x for x in br.findall(".//Page/PartInst")};afterinst={D(x)["dbId"]:x for x in ar.findall(".//Page/PartInst")}
for page in ar.findall(".//Page"):
 for inst in page.findall("PartInst"):
  ident=D(inst)["dbId"];old=beforeinst[ident];key=instance_key(inst);assert key in av
  rx,ry=residues.get(key,(0,0))
  if (rx,ry)==(0,0):continue
  ia=D(inst);dx,dy=rm(rx,ry,ia);ox=int(ia["locX"]);oy=int(ia["locY"])
  ia["locX"]=str(ox+dx);ia["locY"]=str(oy+dy)
  pin_count=0;dp_count=0
  for pin in inst:
   if pin.tag not in {"PortInstScalar","PortInstBus"}:continue
   dd=pin.find("Defn")
   for x,y in [("startX","startY"),("hotptX","hotptY")]:
    if x in dd.attrib or y in dd.attrib:
     assert x in dd.attrib and y in dd.attrib
     dd.set(x,str(int(dd.get(x))-rx));dd.set(y,str(int(dd.get(y))-ry))
   # Refuse unvalidated nested instance-pin coordinate fields.
   for ch in pin:
    if ch.tag=="Defn":continue
    for z in ch.iter():
     assert not(set(z.attrib)&COORDNAMES),("Unreviewed nested instance pin coordinates",ident,ch.tag)
   pin_count+=1
  for dp in inst.findall("PartInstDisplayProp"):
   dd=dp.find("Defn");dd.set("locX",str(int(dd.get("locX","0"))-dx));dd.set("locY",str(int(dd.get("locY","0"))-dy));dp_count+=1
  instrows.append({"page":D(page).get("name",""),"instance_id":ident,"refdes":D(inst.find("Reference")).get("name",""),
   "package":key[1],"graphic":key[2],"local_shift_x":rx,"local_shift_y":ry,"world_origin_delta_x":dx,"world_origin_delta_y":dy,
   "old_origin_x":ox,"old_origin_y":oy,"new_origin_x":ox+dx,"new_origin_y":oy+dy,"pin_override_count":pin_count,"display_prop_count":dp_count,
   "rotation":ia.get("rotation","0"),"mirror":ia.get("mirror","0")})
# Record every cached pin missing from actual instance PortInsts without inferring
# an unexported instantiated/hidden flag from PinShared or absence alone.
for ident,old in beforeinst.items():
 new=afterinst[ident];key=instance_key(old);entry=bv[key];nv=av[key]["view"]
 cps={D(x)["position"]:x for x in entry["view"] if x.tag in {"SymbolPinScalar","SymbolPinBus"}}
 nps={D(x)["position"]:x for x in nv if x.tag in {"SymbolPinScalar","SymbolPinBus"}}
 placed={D(x)["position"] for x in old if x.tag in {"PortInstScalar","PortInstBus"}}
 for pos,pin in cps.items():
  if pos in placed:continue
  pd=D(pin);nd=D(nps[pos]);phys=[]
  for pi,p in enumerate(entry["libpart"].findall("PhysicalPart")):
   rows=[{"tag":x.tag,"defn":D(x)} for x in p if D(x).get("position")==pos]
   if rows:phys.append({"physical_part_index":pi,"records":rows})
  oldhot=absolute(int(pd["hotptX"]),int(pd["hotptY"]),D(old));newhot=absolute(int(nd["hotptX"]),int(nd["hotptY"]),D(new));assert oldhot==newhot
  flags={tag:D(pin.find(tag)).get("val","XML_ABSENT") if pin.find(tag) is not None else "XML_ABSENT" for tag in ["IsNoConnect","IsGlobal","IsNumberVisible"]}
  missing_pin_rows.append({"instance_id":ident,"package":key[1],"graphic":key[2],"position":pos,"name":pd.get("name",""),"visible_raw":pd.get("visible",""),"type_raw":pd.get("type",""),"flags_json":j(flags),"physical_mapping_json":j(phys),"present_in_actual_PortInst":False,"native_instantiated_flag":"NOT_EXPORTED_OR_QUERIED_DO_NOT_INFER","virtual_absolute_hot_before":j(oldhot),"virtual_absolute_hot_after":j(newhot),"virtual_absolute_grid_residue":j((oldhot[0]%A.grid,oldhot[1]%A.grid)),"policy":"Preserve all raw flags and virtual geometry; not claimed hidden/NC or aligned. Future display/instantiation needs separate review."})
# Independent forward actual-coordinate proof for every active instance, not pin ID.
for ident,old in beforeinst.items():
 new=afterinst[ident];key=instance_key(old)
 geometry=projection(bv[key]["view"],old)==projection(av[key]["view"],new)
 pin_equal=override_projection(old)==override_projection(new)
 text_equal=dp_projection(old)==dp_projection(new)
 assert geometry and pin_equal and text_equal,("Visible geometry changed",ident,geometry,pin_equal,text_equal)
 proof.append({"instance_id":ident,"all_ordered_cache_geometry_and_pins_absolute_equal":geometry,"all_pin_position_start_hot_and_attributes_absolute_equal":pin_equal,"all_display_props_actual_anchor_font_visibility_absolute_equal":text_equal})
# Inverse only the explicit representation changes and require whole XML equality.
inv=copy.deepcopy(ar);iv=view_index(inv)
for key,r in residues.items():
 if r!=(0,0):shift_view(iv[key]["view"],-r[0],-r[1])
for inst in inv.findall(".//Page/PartInst"):
 key=instance_key(inst);rx,ry=residues.get(key,(0,0))
 if (rx,ry)==(0,0):continue
 dd=inst.find("Defn");dx,dy=rm(rx,ry,dd.attrib);dd.set("locX",str(int(dd.get("locX"))-dx));dd.set("locY",str(int(dd.get("locY"))-dy))
 for pin in inst:
  if pin.tag not in {"PortInstScalar","PortInstBus"}:continue
  pd=pin.find("Defn")
  for x,y in [("startX","startY"),("hotptX","hotptY")]:
   if x in pd.attrib:pd.set(x,str(int(pd.get(x))+rx));pd.set(y,str(int(pd.get(y))+ry))
 for dp in inst.findall("PartInstDisplayProp"):
  pd=dp.find("Defn");pd.set("locX",str(int(pd.get("locX","0"))+dx));pd.set("locY",str(int(pd.get("locY","0"))+dy))
assert h(inv)==h(br),"Whole-tree inverse allowlist did not reproduce original"
off_origins=[];off_pins=[]
for page in ar.findall(".//Page"):
 for inst in page.findall("PartInst"):
  dd=D(inst)
  if int(dd["locX"])%A.grid or int(dd["locY"])%A.grid:off_origins.append((D(page).get("name"),dd["dbId"],dd["locX"],dd["locY"]))
  for pin in inst:
   if pin.tag not in {"PortInstScalar","PortInstBus"}:continue
   pd=D(pin);x,y=absolute(int(pd["hotptX"]),int(pd["hotptY"]),dd)
   if x%A.grid or y%A.grid:off_pins.append((D(page).get("name"),dd["dbId"],pd.get("position"),x,y))
assert not off_origins and not off_pins,("Grid gate failed",off_origins,off_pins)
def hashes(r,path):return [h(x) for x in r.findall(path)]
unchanged={path:hashes(br,path)==hashes(ar,path) for path in [".//Page/NetScalar",".//Page/NetBus",".//Page/Global",".//Page/OffPageConnector",".//Page/Port","Occurrences","./Cache/OffPageSymbol","./Cache/GlobalSymbol","./Cache/PortSymbol",".//PhysicalPart"]}
assert all(unchanged.values())
assert fs(A.input)==input_sha
A.output.parent.mkdir(parents=True,exist_ok=True);E.ElementTree(ar).write(A.output,encoding="utf-8",xml_declaration=True)
assert h(E.parse(A.output).getroot())==h(ar)
def csvw(name,rows):
 with (A.output.parent/name).open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]) if rows else ["none"]);w.writeheader();w.writerows(rows)
csvw("cache_pins_absent_from_current_instances_preserved.csv",missing_pin_rows);csvw("cache_view_origin_rebase_plan.csv",viewrows);csvw("instance_origin_rebase_plan.csv",instrows);csvw("actual_geometry_pin_text_preservation.csv",proof)
s={"status":"PASS_XML_ORIGIN_REBASE_ACTUAL_GEOMETRY_UNCHANGED_NATIVE_REQUIRED","input_xml_sha256":input_sha,"output_xml_sha256":fs(A.output),"grid":A.grid,"changed_cache_views":len(viewrows),"changed_instances":len(instrows),"all_instance_count":len(proof),"cached_pins_absent_from_current_PortInsts_preserved":len(missing_pin_rows),"unexported_instantiated_flags":"NOT_INFERRED; raw PinShared/NC/visible/numberVisible recorded per position","pin_overrides_rebased":sum(x["pin_override_count"] for x in instrows),"display_props_compensated":sum(x["display_prop_count"] for x in instrows),"part_origins_off_grid":off_origins,"actual_pin_hotspots_off_grid":off_pins,"whole_tree_inverse_allowlist_equal":True,"all_actual_geometry_pin_text_equal":True,"unchanged_electrical_wire_symbol_occurrence_physical_domains":unchanged,"native_transform_basis":"LEGACY ZERO ROTATION/MIRROR ONLY; nonzero poses rejected. Instance DP uses O+loc. Requires supplied input-bound calibration record.","native_gate":"REQUIRED: official XML import, independent reopen/cache-pin/actual text+glyph/geometry audit, PST255. Do not snap origins again."}
A.output.with_suffix(".validation.json").write_text(json.dumps(s,ensure_ascii=True,indent=2)+"\n",encoding="utf-8")
print(json.dumps(s,ensure_ascii=True,indent=2))
