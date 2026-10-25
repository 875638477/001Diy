import pathlib,json,sys,math,hashlib,datetime
R=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu");H=R.parent
sys.path.insert(0,str(H/"tooling/packages"))
from shapely.geometry import LineString,Point,box,Polygon
from shapely import affinity
p=json.loads((R/"plans/combined_v6_screen_4L.json").read_text(encoding="utf-8"))
report={"status":"CANDIDATE_COPPER_SCREEN_ONLY_NATIVE_DRC_PENDING","date":datetime.datetime.now().astimezone().isoformat(),"versionsRejected":[{"version":"v1","reason":"via43,29.25 conflicts proposed V3V3starx43"},{"version":"v2","reason":"via45.45,30.1 overlaps actual retained VDD path near45.45,30.15; reviewer initially omitted real lines and only compared pads; caught before execution"}],"variants":{}}
for v in ("4L",):
 nfile=H/f"inventory/normalized_actual_{v}.json";n=json.loads(nfile.read_text(encoding="utf-8-sig"))
 obs=[];orig={c["ref"]:c for c in n["placements"]};changes={x["ref"]:x for x in p["placementChanges"]}
 for c in n["placements"]:
  for z in c["pins"]:
   if not z["number"] or not z["net"]:continue
   bb=z["padBBox"];shape=box(*bb[0],*bb[1])
   if c["ref"] in changes:
    q=changes[c["ref"]];shape=affinity.rotate(shape,q["rotation"]-c["rotation"],origin=c["xy"])
    shape=affinity.translate(shape,q["xy"][0]-c["xy"][0],q["xy"][1]-c["xy"][1])
   quiet=c["ref"] in ("C22","C23") and z["number"]=="2"
   obs.append({"id":c["ref"]+"."+z["number"],"net":z["net"],"shape":shape,"layer":"TOP","kind":"pad","groundRole":"quiet" if quiet else"app"})
 for i,z in enumerate(n["routes"]):
  if not z["layer"].startswith("ETCH/") or not z.get("net"):continue
  obs.append({"id":"existingRoute"+str(i),"net":z["net"],"shape":LineString(z["startEnd"]).buffer(z["width"]/2,quad_segs=32),"layer":z["layer"].split("/")[1],"kind":"route","groundRole":"app","points":z["startEnd"],"width":z["width"]})
 for i,z in enumerate(n["vias"]):
  obs.append({"id":"existingVia"+str(i),"net":z["net"],"shape":Point(z["xy"]).buffer(.3,quad_segs=64),"layer":"ALL","kind":"via","groundRole":"app"})
 new=[]
 for o in p["operations"]:
  if o["type"]=="via":
   new.append({"id":o["id"],"net":o["net"],"shape":Point(o["xy"]).buffer(.3,quad_segs=64),"layer":"ALL","kind":"via","groundRole":"bridge" if o["id"]=="HSE_SINGLE_ANCHOR" else"quiet" if o["id"] in ("HSE_LOCAL_C22","HSE_LOCAL_C23") else"app"})
  else:
   ws=o.get("widths") or [o["width"]]*(len(o["points"])-1)
   for j,(a,b,w) in enumerate(zip(o["points"],o["points"][1:],ws)):
    new.append({"id":o["id"]+"/"+str(j),"net":o["net"],"shape":LineString([a,b]).buffer(w/2,quad_segs=32),"layer":o["layer"],"kind":"route","groundRole":"quiet" if o["id"].startswith(("HSE_GUARD","HSE_C22_RETURN","HSE_C23_RETURN")) else"app"})
 anchor=next(x for x in new if x["id"]=="HSE_SINGLE_ANCHOR")
 anear=[]
 for z in obs:
  if z["net"]!="GND" and z["layer"] in ("TOP","ALL"):
   anear.append({"distance":anchor["shape"].distance(z["shape"]),"id":z["id"],"net":z["net"],"kind":z["kind"],"points":z.get("points")})
 anear.sort(key=lambda x:x["distance"])
 issues=[]
 for i,x in enumerate(new):
  for y in obs+new[:i]:
   if x["layer"]!="ALL" and y["layer"]!="ALL" and x["layer"]!=y["layer"]:continue
   isolate=x["net"]==y["net"]=="GND" and {x["groundRole"],y["groundRole"]}=={"quiet","app"}
   if x["net"]==y["net"] and not isolate:continue
   dist=x["shape"].distance(y["shape"])
   if dist<.29995:
    issues.append({"a":x["id"],"b":y["id"],"nets":[x["net"],y["net"]],"distance":dist,"overlap":x["shape"].intersects(y["shape"]),"quietAppIsolation":isolate})
 issues.sort(key=lambda x:x["distance"])
 poly=Polygon(p["oscillatorReference"]["islandPolygon"]);void=Polygon(p["oscillatorReference"]["applicationGroundVoidPolygon"])
 report["variants"][v]={"snapshot":str(nfile),"sha256":hashlib.sha256(nfile.read_bytes()).hexdigest(),"readback":n["readbackDirectory"],"nativeTOPCurrentSegments":sum(x["kind"]=="route" and x["layer"]=="TOP" for x in obs),"anchorMinimumOtherNetCopper":anear[:12],"anchorMinAtLeastPoint299":anear[0]["distance"]>=.2999,"candidateIssuesBelowPoint30":issues,"overlapCount":sum(x["overlap"] for x in issues),"issuesBelowPoint20":[x for x in issues if x["distance"]<.19995],"islandPolygonValid":poly.is_valid,"voidPolygonValid":void.is_valid,"islandFullyInsideVoid":void.contains(poly),"moatMinimum":poly.boundary.distance(void.boundary)}
(R/"review/combined_v6_copper_screen_4L.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps({v:{"anchorMin":r["anchorMinimumOtherNetCopper"][:3],"allIssues":len(r["candidateIssuesBelowPoint30"]),"overlaps":r["overlapCount"],"below20":len(r["issuesBelowPoint20"]),"firstIssues":r["issuesBelowPoint20"][:12],"moatMinimum":r["moatMinimum"]} for v,r in report["variants"].items()},ensure_ascii=True))
