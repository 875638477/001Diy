import pathlib,json,sys,math
R=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu");H=R.parent
sys.path.insert(0,str(H/"tooling/packages"))
from shapely.geometry import Point,LineString,box
from shapely import affinity
p=json.loads((R/"plans/combined_v11_screen_4L.json").read_text(encoding="utf-8"));n=json.loads((H/"inventory/normalized_actual_4L.json").read_text(encoding="utf-8"));changes={q["ref"]:q for q in p["placementChanges"]};obs=[]
for c in n["placements"]:
 for z in c["pins"]:
  if not z["net"] or z["net"]=="GND":continue
  shape=box(*z["padBBox"][0],*z["padBBox"][1])
  if c["ref"] in changes:
   q=changes[c["ref"]];shape=affinity.rotate(shape,q["rotation"]-c["rotation"],origin=c["xy"]);shape=affinity.translate(shape,q["xy"][0]-c["xy"][0],q["xy"][1]-c["xy"][1])
  obs.append((c["ref"]+"."+z["number"],shape))
for z in n["routes"]:
 if z["net"] and z["net"]!="GND":obs.append(("native_"+z["net"],LineString(z["startEnd"]).buffer(z["width"]/2,quad_segs=32)))
for o in p["operations"]:
 if o["net"]=="GND":continue
 if o["type"]=="via":obs.append((o["id"],Point(o["xy"]).buffer(.3,quad_segs=64)))
 else:
  ws=o.get("widths") or[o["width"]]*(len(o["points"])-1)
  obs.extend((o["id"],LineString([a,b]).buffer(w/2,quad_segs=32)) for a,b,w in zip(o["points"],o["points"][1:],ws))
rows=[]
for i in range(330,352):
 for j in range(277,321):
  xy=[i/10,j/10];disk=Point(xy).buffer(.3,quad_segs=64);ds=sorted((disk.distance(sh),name) for name,sh in obs)
  if ds[0][0]>=.29995:rows.append({"xy":xy,"distanceToSignalExit":math.dist(xy,[34.5,29.6]),"nearest":ds[:3]})
rows.sort(key=lambda x:x["distanceToSignalExit"]);(R/"review/gpio_west_return_candidates.json").write_text(json.dumps(rows[:30],indent=2),encoding="utf-8");print(json.dumps(rows[:10]))
