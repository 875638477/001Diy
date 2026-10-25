import pathlib,csv,re,json,hashlib,math,collections,datetime,os
R=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\examples\lessonG_30_37_20261020\engineering_mcu");G=R.parent
os.environ["TMP"]=os.environ["TEMP"]=str(R/"runtime")
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):return list(csv.DictReader(p.open(encoding="utf-8-sig",newline=""),delimiter="\t"))
def points(s):
    nums=[float(x) for x in re.findall(r"-?\d+(?:\.\d+)?",s)]
    return [nums[i:i+2] for i in range(0,len(nums),2)]
def values(s):
    return {m[0]:m[1] for m in re.findall(r'\(([A-Za-z_]\w*)\s+("[^"]*"|[^ ()]+)\)',s)}
def sets(p):return {(r["cset"],r["layer"]):values(r["values"]) for r in rows(p)}
def canon(net,a,b,w):return (net,tuple(sorted((tuple(a),tuple(b)))),round(float(w),6))
def differences(a,b):
    return {k:{"parent":a.get(k),"local":b.get(k)} for k in sorted(set(a)|set(b)) if a.get(k)!=b.get(k)}
P=json.loads((G/"inventory/normalized_actual_4L.json").read_text(encoding="utf-8-sig"))
pin={(c["ref"],p["number"]):p for c in P["placements"] for p in c["pins"] if p["number"]}
result={"status":"INTERMEDIATE_LOOPS05_REVIEW_FRESH_REOPEN_AND_CHALLENGE_PENDING","date":datetime.datetime.now().astimezone().isoformat(),"nativeInputSnapshotSHA256":h(G/"inventory/normalized_actual_4L.json"),"scope":"Independent geometric/constraint-field comparison from saved native loops05 outputs; not a new Cadence execution","variants":{}}
for v in ("4L","2L"):
    d=G/f"logs/loops_{v}_05";f=d/"local_loops.txt";text=f.read_text(encoding="utf-8-sig")
    routes=[]
    for line in text.splitlines():
        if not line.startswith("LOCAL_ROUTE\t"):continue
        parts=line.split("\t");pts=points(parts[4]);widths=[float(x) for x in re.findall(r"\d+(?:\.\d+)?",parts[5])]
        lengths=[math.dist(a,b) for a,b in zip(pts,pts[1:])]
        neck=sum(l for l,w in zip(lengths,widths) if w<.60-1e-6)
        start=pts[0];p0=next(p for (r,n),p in pin.items() if r=="U1" and math.dist(p["xy"],start)<.0002)
        bb=p0["padBBox"];dx,dy=pts[1][0]-start[0],pts[1][1]-start[1]
        if abs(dx)>.01 and abs(dy)<.0001:inside=abs((bb[0 if dx<0 else 1][0])-start[0])
        elif abs(dy)>.01 and abs(dx)<.0001:inside=abs((bb[0 if dy<0 else 1][1])-start[1])
        else:raise AssertionError("Unexpected non-axial first neck")
        routes.append({"name":parts[1],"net":parts[2].strip('"'),"layer":parts[3].strip('"'),"points":pts,"widths":widths,"segmentLengths":lengths,"totalCenterLength":sum(lengths),"nativeWholeNeckLength":neck,"firstAxialPadOverlap":inside,"externalNeckLength":neck-inside,"withinLocal1_4":neck<=1.4+.0001,"satisfiesOriginalGlobal1_0":neck<=1.0+.0001})
    actual=[r for r in rows(d/"route_geometry.tsv") if r["layer"]=="ETCH/TOP" and r["net"] in ("V3V3","GND")]
    expected=collections.Counter(canon(r["net"],a,b,w) for r in routes for a,b,w in zip(r["points"],r["points"][1:],r["widths"]))
    observed=collections.Counter(canon(r["net"],*points(r["startEnd"]),r["width"]) for r in actual)
    ps=sets(d/"physical_csets.tsv");ss=sets(d/"spacing_csets.tsv")
    parents=[("G31_POWER_ESCAPE","P_POWER_060" if v=="4L" else "G2L_POWER_DEMO"),("G31_GND_ESCAPE","P_GND_PLANE" if v=="4L" else "G2L_GND_DEMO")]
    pdiffs=[]
    for local,parent in parents:
        for (name,layer),pval in ps.items():
            if name!=parent:continue
            diff=differences(pval,ps[(local,layer)])
            pdiffs.append({"local":local,"parent":parent,"layer":layer,"diff":diff,"onlyMaxNeck1to1_4":diff=={"necklength_max":{"parent":"1.0","local":"1.4"}}})
    sdiffs=[]
    if v=="4L":
        for (name,layer),sval in ss.items():
            if name!="S_POWER_030":continue
            diff=differences(sval,ss[("G31_PIN_ESCAPE",layer)])
            sdiffs.append({"layer":layer,"diff":diff,"onlyTwoFields":diff=={k:{"parent":"0.3","local":"0.2"} for k in ("line_line","smdpin_line")}})
    boxes=[]
    for line in text.splitlines():
        if line.startswith("ESCAPE_REGION_RECT="):
            m=re.search(r"bBox (\(\([^)]*\) \([^)]*\)\))",line)
            boxes.append(points(m.group(1)))
    powerPins=[]
    otherPins=[]
    for (ref,num),p in pin.items():
        if any(b[0][0]-.0001<=p["xy"][0]<=b[1][0]+.0001 and b[0][1]-.0001<=p["xy"][1]<=b[1][1]+.0001 for b in boxes):
            target={"ref":ref,"pin":num,"net":p["net"],"xy":p["xy"]}
            (powerPins if p["net"] in ("V3V3","GND","VDDA","V5") else otherPins).append(target)
    viaunique=sorted(set((r["name"],float(r["x"]),float(r["y"]),r["net"],float(r["drill"])) for r in rows(d/"vias.tsv")))
    shapes=rows(d/"g_copper_shapes.tsv")
    goals=collections.Counter(re.findall(r"targetReached=(\w+)",text))
    refreached=len(re.findall(r"NATIVE_REFERENCE_REACHED.*count=1",text))
    finalDRC="DRC_STATUS\tLOOPS_WITH_REFERENCE\t0\tt" in text and "DRC_STATUS\tG_SNAPSHOT\t0\tt" in (d/"g_drc_details.txt").read_text(encoding="utf-8-sig")
    checks={"sixRoutes":len(routes)==6,"exact23NativeSegmentsMatch":expected==observed and len(actual)==23,"allNecksLocalNotGlobal":all(r["withinLocal1_4"] and not r["satisfiesOriginalGlobal1_0"] for r in routes),"padOverlapExactly0_6":all(abs(r["firstAxialPadOverlap"]-.6)<.0001 for r in routes),"physicalCloneOnlyNeck":all(x["onlyMaxNeck1to1_4"] for x in pdiffs),"fourLayerSpacingOnlyTwoFields":all(x["onlyTwoFields"] for x in sdiffs),"oneGroupThreeTOPRectangles":len(boxes)==3 and 'name "G31_U1_ESCAPE"' in text and text.count('layer "CONSTRAINT REGION/TOP"')==3,"powerPinScopeExactlyU1Six":set((p["ref"],p["pin"]) for p in powerPins)=={("U1",str(x)) for x in (23,24,35,36,47,48)},"fourUniqueGNDVias":len(viaunique)==4 and all(x[3]=="GND" for x in viaunique),"oneActualFilledCurrentGNDShape":len(shapes)==1 and shapes[0]["layer"]==("ETCH/L2" if v=="4L" else "ETCH/BOTTOM") and shapes[0]["net"]=="GND" and shapes[0]["filled"]=="t" and shapes[0]["generated"]=="t" and shapes[0]["fillOOD"]=="nil","nativeSixTargetsAndThreeReference":goals=={"t":6} and refreached==3,"nativeCurrentDRC0":finalDRC,"nativeComplete": "G_LOCAL_LOOPS_COMPLETE" in text}
    result["variants"][v]={"status":"PASS_LOOPS05_SCOPE" if all(checks.values()) else "REQUIRES_CORRECTION","checks":checks,"routes":routes,"physicalCSetDiffs":pdiffs,"spacingCSetDiffs":sdiffs,"region":{"name":"G31_U1_ESCAPE","groups":1,"topRectangles":boxes,"powerPinAnchorsInside":powerPins,"otherPinAnchorsGeometricallyInside":otherPins,"restriction":"Other GPIO anchors can lie geometrically inside, but Region-Class binds only corresponding power/GND classes; class matching/spacing interaction must still be honored."},"uniqueVias":viaunique,"localGroundTopology":"U1.VSS -> TOP short trace -> corresponding cap.2 -> cap-side via -> real filled GND plane. HF cap loop has direct TOP return; graph reaches plane but does not prove mandatory current through plane.","referenceShape":{"layer":shapes[0]["layer"],"area":float(shapes[0]["area"]),"bbox":points(shapes[0]["bbox"])},"inputFilesSHA256":{p.name:h(p) for p in [f,d/"route_geometry.tsv",d/"physical_csets.tsv",d/"spacing_csets.tsv",d/"class_table.tsv",d/"group_members.tsv",d/"g_copper_shapes.tsv",d/"vias.tsv",d/"g_drc_details.txt"]}}
(R/"local_copper_independent_precheck.json").write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps({k:{"status":v["status"],"failed":[c for c,p in v["checks"].items() if not p],"segments":sum(len(r["widths"]) for r in v["routes"]),"neck":v["routes"][0]["nativeWholeNeckLength"],"external":v["routes"][0]["externalNeckLength"]} for k,v in result["variants"].items()},ensure_ascii=True))
