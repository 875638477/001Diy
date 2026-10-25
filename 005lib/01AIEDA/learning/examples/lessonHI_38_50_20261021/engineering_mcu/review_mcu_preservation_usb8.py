import pathlib,json,hashlib,sys,re,csv,math,shutil,datetime
R=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu");H=R.parent
sys.path.insert(0,str(H/"tooling/packages"));sys.path.insert(0,str(R))
from shapely.geometry import Polygon,Point,LineString
from shapely.ops import unary_union
from native_polygon_geometry import poly_from_native
plan=R/"plans/mcu_critical_routes_v6.json";m=json.loads(plan.read_text(encoding="utf-8"));out={"status":"MCU6_GEOMETRY_AND_QUIET_ISLAND_PRESERVATION_AFTER_USB8_NOT_FINAL_HI_BOARD","date":datetime.datetime.now().astimezone().isoformat(),"planSHA256":hashlib.sha256(plan.read_bytes()).hexdigest(),"variants":{},"limitations":["HI wholeboard remains unfinished; USB8 included, GPIO6 and laterordinary routes notincluded","Hardwarestartup/ADC/EMI/impedance andGUI notestablished","Arcflatteningsagitta<=.00002mm; nativearea rounded/quantized difference<=.01mm2 accepted only forgeometryparsercheck"]}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for v in("4L","2L"):
 stage="usb_esd_4L_b008" if v=="4L" else "usb_esd_2L_b008_bulk"
 cp=H/"inventory/checkpoints"/stage;nf=cp/"normalized.json";n=json.loads(nf.read_text(encoding="utf-8"));logs=pathlib.Path(n["readbackDirectory"])
 archive=R/"review/inputs"/stage;archive.mkdir(parents=True,exist_ok=True)
 inputs=[]
 for p in[nf,cp/"networks.json",logs/"hi_hse_isolation_challenge.txt",logs/"native_summary.txt",logs/"hi_dynamic_boundaries.tsv",logs/"hi_rules_context.tsv",logs/"physical_pad_layers.tsv",logs/"hi_batch_execution.txt"]:
  if p.exists():q=archive/p.name;shutil.copy2(p,q);inputs.append({"source":str(p),"copy":str(q),"sha256":sha(q)})
 checks=[];add=lambda name,ok,detail=None:checks.append({"name":name,"pass":bool(ok),"detail":detail})
 native=logs.joinpath("native_summary.txt").read_text(encoding="utf-8");add("Nativecomplete80comp69netDRC0current","DE_BOARD_READ_COMPLETE" in native and"components=80" in native and"nets=69" in native and"drcs=0" in native and"drcState=t" in native,native)
 pp={p["ref"]:p for p in n["placements"]}
 for q in m["placementChanges"]:
  actual=pp[q["ref"]];add("Placement_"+q["ref"],math.dist(q["xy"],actual["xy"])<1e-6 and abs(q["rotation"]-actual["rotation"])<1e-6,{"expected":q,"actual":{k:actual[k] for k in("ref","xy","rotation")}})
 missing=[];wanted=0
 for o in m["operations"]:
  if o["type"]=="via":
   matches=[z for z in n["vias"] if z["net"]==o["net"] and math.dist(z["xy"],o["xy"])<1e-6];add("Via_"+o["id"],len(matches)==1,{"expected":o["xy"],"found":len(matches)})
  else:
   ws=o.get("widths") or[o["width"]]*(len(o["points"])-1)
   for j,(a,b,w) in enumerate(zip(o["points"],o["points"][1:],ws)):
    wanted+=1
    matches=[z for z in n["routes"] if z["net"]==o["net"] and z["layer"]=="ETCH/"+o["layer"] and abs(z["width"]-w)<1e-6 and(min(math.dist(a,z["startEnd"][0])+math.dist(b,z["startEnd"][1]),math.dist(a,z["startEnd"][1])+math.dist(b,z["startEnd"][0]))<1e-6)]
    if not matches:
     pieces=[LineString(z["startEnd"]) for z in n["routes"] if z["net"]==o["net"] and z["layer"]=="ETCH/"+o["layer"] and abs(z["width"]-w)<1e-6]
     covered=bool(pieces) and LineString([a,b]).difference(unary_union(pieces).buffer(.000001)).length<.000001
     if not covered:missing.append({"id":o["id"],"segment":j,"a":a,"b":b,"width":w})
 add("AllPlannedSegmentsReadExactly",not missing,{"segmentCount":wanted,"missing":missing})
 pols=[(p,poly_from_native(p)[0]) for p in n["planes"] if p["net"]=="GND"];island=Polygon(m["oscillatorReference"]["islandPolygon"]);void=Polygon(m["oscillatorReference"]["applicationGroundVoidPolygon"])
 quiet=[(p,s) for p,s in pols if s.symmetric_difference(island).area<1e-6];app=[(p,s) for p,s in pols if s.symmetric_difference(island).area>=1e-6]
 add("ExactlyOneTrueQuietShape",len(quiet)==1,[(p["layer"],p["area"]) for p,s in quiet])
 add("ActualQuietShapeOnCorrectLayer",len(quiet)==1 and quiet[0][0]["layer"]==("ETCH/L2" if v=="4L" else"ETCH/BOTTOM"))
 add("ActualQuietNoOtherLayerApplicationCopperOverlap",all(s.intersection(island).area<1e-7 for p,s in app),[(p["layer"],s.intersection(island).area) for p,s in app])
 add("AllGroundPolygonsValid",all(s.is_valid for p,s in pols))
 add("ArcParserAreaAgreementWithinPoint01",all(abs(s.area-p["area"])<=.01 for p,s in pols),[(p["layer"],p["area"],s.area) for p,s in pols])
 quietvias=[o for o in m["operations"] if o["id"] in("HSE_SINGLE_ANCHOR","HSE_LOCAL_C22","HSE_LOCAL_C23")]
 for o in quietvias:
  nv=next(z for z in n["vias"] if math.dist(o["xy"],z["xy"])<1e-6);layers=set()
  for row in csv.DictReader(logs.joinpath("physical_pad_layers.tsv").open(encoding="utf-8"),delimiter="\t"):
   xy=[float(x) for x in re.findall(r"[-+]?(?:\d*\.\d+|\d+)",row["xy"])]
   if row["kind"]=="VIA" and math.dist(xy,nv["xy"])<1e-6 and row["layer"].startswith("ETCH/") and row["figure"]!="NULL":layers.add(row["layer"])
  expected={"ETCH/TOP","ETCH/BOTTOM"}|({"ETCH/L2","ETCH/L3"} if v=="4L" else set())
  disk=Point(nv["xy"]).buffer(.3,quad_segs=128)
  add("ThroughViaAllRealPads_"+o["id"],layers==expected,sorted(layers))
  add("NoQuietViaUnexpectedAppPlaneTouch_"+o["id"],all(s.distance(disk)>.049 for p,s in app),[(p["layer"],s.distance(disk)) for p,s in app])
  add("QuietViaActualIslandOverlap_"+o["id"],len(quiet)==1 and quiet[0][1].intersects(disk))
 raw=logs.joinpath("hi_hse_isolation_challenge.txt").read_text(encoding="utf-8");neg=raw.split("HSE_NEGATIVE_DELETE_ONLY_ANCHOR=")[1].split("HSE_NEGATIVE_ACTUAL_GND_NET_UNCONNECTED")[0]
 proofs=re.findall(r'HI_ENDPOINT_PROOF from="([^"]+)" to="([^"]+)" expected=(t|nil) actual=(t|nil)',raw)
 add("ChallengeEveryExpectedEqualsActual",len(proofs)>=12 and all(a==b for _,_,a,b in proofs),{"proofCount":len(proofs)})
 add("ChallengeDeleteOnlyCorrectThroughVia",'xy (45.45 28.85)' in neg and 'objType "via"' in neg)
 for a,b,value in[("C22.2","C23.2","t"),("C22.2","U1.47","nil"),("C22.2","Y1.2","nil"),("C15.2","U1.47","t"),("Y1.2","Y1.4","t"),("Y1.2","U1.47","t")]:
  add("Negative_"+a+"_"+b,f'from="{a}" to="{b}" expected={value} actual={value}' in neg)
 add("NegativeAll3GuardEndsRemainLocal",neg.count("guardReached=t")==3 and neg.count("NEGATIVE_LOCAL_REFERENCE count=1")==3)
 restoredDirect = 'DRC_STATUS\tHSE_ANCHOR_RESTORED\t0\tt' in raw and "HSE_ISOLATION_NEGATIVE_TEST_COMPLETE_NO_SAVE" in raw
 endpointLog=logs.joinpath("hi_reopen_endpoint_proofs.txt").read_text(encoding="utf-8") if logs.joinpath("hi_reopen_endpoint_proofs.txt").exists() else ""
 restoredBulk = "HSE_ISOLATION_GRAPH_NEGATIVE_TEST_COMPLETE_FULL_DRC_REQUIRED" in raw and "HI_READBACK_UNWIND_DRC_RESTORED=t" in endpointLog and "drcs=0" in native and "drcState=t" in native
 add("RestoreDRC0CurrentComplete",restoredDirect or restoredBulk,{"directChallengeUpdate":restoredDirect,"bulkGraphThenExplicitFullUpdateAndCurrentSnapshot":restoredBulk})
 out["variants"][v]={"snapshot":str(nf),"sha256":sha(nf),"readbackDirectory":str(logs),"inputs":inputs,"checks":checks,"passed":sum(x["pass"] for x in checks),"total":len(checks),"allPassed":all(x["pass"] for x in checks),"quietArea":island.area,"minimumPhysicalMoat":island.boundary.distance(void.boundary)}
(R/"review/mcu_preservation_after_usb8_independent_review.json").write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps({v:{k:r[k] for k in("passed","total","allPassed")} |{"failures":[z for z in r["checks"] if not z["pass"]]} for v,r in out["variants"].items()},ensure_ascii=True))
