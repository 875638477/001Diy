import pathlib,json,sys,math,datetime
R=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu");H=R.parent
sys.path.insert(0,str(H/"tooling/packages"));sys.path.insert(0,str(R))
from shapely.geometry import LineString,Point
from review_usb_native_paths import copper_ground,sha
cases=[("4L",H/"inventory/checkpoints/usb_esd_4L_b008/normalized.json"),("2L",R/"review/inputs/usb_failed2L_normalized.json")]
out={"status":"ACTUAL_COPPER_AVAILABLE_RETURN_CORRIDORS_NOT_FIELD_CURRENT_PREDICTION","date":datetime.datetime.now().astimezone().isoformat(),"method":"Check complete buffered polylines inside actualgroundpolygon+GNDclines+qualifiednativepads. Stated lengths are available geometric upperbounds, not shortest electromagnetic paths; startpointsy4.9 intentionally.9mm southofsignalvias, not the signalcenters.","cases":{}}
for v,nf in cases:
 n=json.loads(nf.read_text(encoding="utf-8"));logs=pathlib.Path(n["readbackDirectory"]);ref="L3" if v=="4L" else"TOP";g,om=copper_ground(n,logs,ref)
 requests=[("MirrorLeftReturn",[[39.75,4.9],[38.9,4.9],[38.15,5.8]],.4),("MirrorRightReturn",[[40.75,4.9],[41.3,4.9],[41.7,5.8]],.4),("MirrorCommonReturnStrip",[[38.15,5.8],[38.9,4.9],[41.3,4.9],[41.7,5.8]],.4)]
 rows=[]
 for name,points,w in requests:
  line=LineString(points);strip=line.buffer(w/2,quad_segs=64);miss=strip.difference(g)
  rows.append({"id":name,"layer":ref,"points":points,"verifiedCopperCorridorWidth":w,"lengthUpperBound":line.length,"uncoveredStripArea":miss.area,"wholeStripInActualGND":miss.area<.000001})
 forVia=[]
 forxy=[(38.15,5.8),(41.7,5.8)]
 for xy in forxy:
  via=next(z for z in n["vias"] if z["net"]=="GND" and math.dist(z["xy"],xy)<1e-5)
  forVia.append({"xy":xy,"actualThroughVia":via["padstack"],"refLayerPointInsideGround":g.covers(Point(xy)),"signalViaCenterDistance":math.dist(xy,[39.75 if xy[0]<40 else 40.75,5.8])})
 entry=None
 if v=="2L":
  b,_=copper_ground(n,logs,"BOTTOM");points=[[40.7,8.4],[39.4,8.4],[39.4,10.1],[41.2,10.1]];line=LineString(points);strip=line.buffer(.15,quad_segs=64)
  entry={"id":"ESD_VBUS_BOTTOM_SLOT_LEFT_DETOUR","referenceLayer":"BOTTOM","points":points,"verifiedCopperCorridorWidth":.3,"lengthUpperBound":line.length,"uncoveredStripArea":strip.difference(b).area,"wholeStripInActualGND":strip.difference(b).area<.000001,"qualification":"Actual available aroundleftend ofVBUSbridge; directprojectiongap1.34262mm remains. NotsayingHFcurrentmustfollowthispolyline, notuniformreference orUSBcompliance."}
 out["cases"][v]={"normalized":str(nf),"sha256":sha(nf),"readback":str(logs),"sourceScope":"4LformalUSB8checkpoint" if v=="4L" else"2LfirstUSBcandidatephysicalgeometryvalidbutelectrical/classDRCfailed; final2Lmustrecheck","mirrorReturnCorridors":rows,"groundVias":forVia,"entryReferenceDetour":entry}
(R/"review/usb_actual_return_corridors_01.json").write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps({v:{"mirror":[(x["id"],x["wholeStripInActualGND"],x["uncoveredStripArea"],x["lengthUpperBound"]) for x in c["mirrorReturnCorridors"]],"entry":c["entryReferenceDetour"]} for v,c in out["cases"].items()},ensure_ascii=True))
