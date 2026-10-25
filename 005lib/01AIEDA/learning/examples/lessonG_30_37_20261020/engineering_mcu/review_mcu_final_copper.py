import pathlib,csv,re,json,hashlib,math,collections,datetime,os
R=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\examples\lessonG_30_37_20261020\engineering_mcu");G=R.parent
os.environ["TMP"]=os.environ["TEMP"]=str(R/"runtime")
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return p.read_text(encoding="utf-8-sig")
def rows(p):return list(csv.DictReader(p.open(encoding="utf-8-sig",newline=""),delimiter="\t"))
def points(s):
    n=[float(x) for x in re.findall(r"-?\d+(?:\.\d+)?",s)]
    return [n[i:i+2] for i in range(0,len(n),2)]
def values(s):return {m[0]:m[1] for m in re.findall(r'\(([A-Za-z_]\w*)\s+("[^"]*"|[^ ()]+)\)',s)}
def sets(p):return {(r["cset"],r["layer"]):values(r["values"]) for r in rows(p)}
def canon(net,a,b,w):return (net,tuple(sorted((tuple(round(x,5) for x in a),tuple(round(x,5) for x in b)))),round(float(w),6))
def differences(a,b):return {k:{"parent":a.get(k),"local":b.get(k)} for k in sorted(set(a)|set(b)) if a.get(k)!=b.get(k)}
pre=json.loads(read(R/"local_copper_independent_precheck.json"))
placementReview=json.loads(read(R/"native_mcu_placement_review.json"))
wanted={"U1","Y1","J7","J8","J10"}|{"C"+str(i) for i in range(13,25)}|{"R"+str(i) for i in range(26,33)}
expectedVia={(32.45,25.2748),(42.3252,19.35),(47.45,28.7252),(52.0,35.0)}
expectedRegion=[[[34.2,23.5],[36.5,25.5]],[[41.5,21.2],[43.5,23.5]],[[43.5,28.5],[45.8,30.5]]]
bulk=[
 {"net":"V3V3","points":[[46.5,30.3],[49.5,30.3]],"width":.60,"role":"C15.1 to C16.1 VDD3 bulk branch"},
 {"net":"GND","points":[[47.45,28.7252],[47.9428,28.7252],[48.4,28.268],[49.5,28.268]],"width":.60,"role":"existing C15 GND-via node to C16.2; C15.2 joins through retained TOP trace"}]
res={"status":"IN_PROGRESS","checkedAt":datetime.datetime.now().astimezone().isoformat(),"scope":"Independent read-only comparison of final native reopen evidence, exact local segments, rule-field copies, region/class scope and reversible challenges. No Cadence invocation by this reviewer.","inheritedLayoutReview":str(R/"native_mcu_placement_review.json"),"variants":{},"limitations":["Only three local VDD/VSS decoupling demonstrations and VDD3 C16 branch are physically routed; HSE/ADC/other board nets remain incomplete.","DRC 0/current and graph reachability do not certify PI/SI/EMI, mandatory current via reference plane, manufacturing release, GUI use, or effective C16 capacitance.","Local CSet values were copied from named source CSet at creation; the word parent denotes provenance, not a live inheritance link. Future source-rule edits require explicit comparison/resynchronization."]}
for v in ("4L","2L"):
    d=G/f"logs/final_reopen_{v}_01"; cd=G/f"logs/freeze_{v}_02"
    board=G/f"current/G_{v}_LAYOUT_v1.brd";snap=G/f"inventory/normalized_actual_{v}.json"
    n=json.loads(read(snap));old=json.loads(read(R/f"native_snapshot_{v}_reconcile02.json"))
    nowBy={x["ref"]:x for x in n["placements"]};oldBy={x["ref"]:x for x in old["placements"]}
    pose=[]
    for ref in sorted(wanted):
        a,b=oldBy[ref],nowBy[ref]
        def pindata(c):return sorted((p["number"],p["net"],p["xy"],p["padBBox"]) for p in c["pins"] if p["number"])
        pose.append({"ref":ref,"samePoseAndBody":all(a[k]==b[k] for k in ("xy","rotation","bodyExtent")),"sameLogicalPinNetXYCopperBBox":pindata(a)==pindata(b)})
    proof=read(d/"g_final_connectivity_constraints.txt");challenge=read(cd/"local_rule_challenges.txt");launch=json.loads(read(d/"launch.json"))
    routes=pre["variants"][v]["routes"]
    expected=collections.Counter(canon(r["net"],a,b,w) for r in routes for a,b,w in zip(r["points"],r["points"][1:],r["widths"]))
    for b in bulk:
        expected.update(canon(b["net"],a,z,b["width"]) for a,z in zip(b["points"],b["points"][1:]))
    actual=[r for r in rows(d/"route_geometry.tsv") if r["layer"].startswith("ETCH/")]
    top=[r for r in actual if r["layer"]=="ETCH/TOP"]
    observed=collections.Counter(canon(r["net"],*points(r["startEnd"]),r["width"]) for r in top)
    plane=[r for r in actual if r["layer"]!= "ETCH/TOP"]
    ps=sets(d/"physical_csets.tsv");ss=sets(d/"spacing_csets.tsv")
    pDiff=[]
    for local,parent in [("G31_POWER_ESCAPE","P_POWER_060" if v=="4L" else "G2L_POWER_DEMO"),("G31_GND_ESCAPE","P_GND_PLANE" if v=="4L" else "G2L_GND_DEMO")]:
        for (name,layer),pval in ps.items():
            if name==parent:
                diff=differences(pval,ps[(local,layer)])
                pDiff.append({"source":parent,"copy":local,"layer":layer,"diff":diff,"onlyMaxNeck1to1_4":diff=={"necklength_max":{"parent":"1.0","local":"1.4"}}})
    sDiff=[]
    if v=="4L":
        for (name,layer),sval in ss.items():
            if name=="S_POWER_030":
                diff=differences(sval,ss[("G31_PIN_ESCAPE",layer)])
                sDiff.append({"source":name,"copy":"G31_PIN_ESCAPE","layer":layer,"diff":diff,"onlyLineLineAndSMDPinLine03to02":diff=={k:{"parent":"0.3","local":"0.2"} for k in ("line_line","smdpin_line")}})
    regionlines=[x for x in proof.splitlines() if x.startswith("REGION_SHAPE ")]
    boxes=[points(re.search(r"bBox (\(\([^)]*\) \([^)]*\)\))",x).group(1)) for x in regionlines]
    powerInside=[];otherInside=[]
    for c in n["placements"]:
        for p in c["pins"]:
            if not p["number"]:continue
            if any(b[0][0]-.0001<=p["xy"][0]<=b[1][0]+.0001 and b[0][1]-.0001<=p["xy"][1]<=b[1][1]+.0001 for b in boxes):
                target={"ref":c["ref"],"pin":p["number"],"net":p["net"],"xy":p["xy"]}
                (powerInside if p["net"] in ("V3V3","VDDA","GND","V5") else otherInside).append(target)
    vias=sorted(set((r["name"],float(r["x"]),float(r["y"]),r["net"],float(r["drill"])) for r in rows(d/"vias.tsv")))
    shapes=rows(d/"g_copper_shapes.tsv");refLayer="ETCH/L2" if v=="4L" else "ETCH/BOTTOM"
    stages={m[0]:{"errors":int(m[1]),"current":m[2]=="t"} for m in re.findall(r"DRC_STATUS\t([A-Z0-9_]+)\t(\d+)\t(\w+)",challenge)}
    targetedOutside=[x for x in challenge.splitlines() if x.startswith("DRC_DETAIL\tOUTSIDE_REGION_GLOBAL_RULES")]
    outsideNeck=next((x for x in targetedOutside if 'name "Maximum Neck Length"' in x),None)
    outsideSpacing=next((x for x in targetedOutside if 'name "Line to Line Spacing"' in x),None)
    goals=collections.Counter(re.findall(r"targetReached=(\w+)",proof))
    reference=re.findall(r'NATIVE_REFERENCE_REACHED\t"([^"]+)"\t"([^"]+)"\t"([^"]+)"\tcount=(\d+)',proof)
    group=rows(d/"group_members.tsv")
    # Exact group member table remains recorded as original evidence; live resolution is explicit in final native TABLE lines.
    table=[x for x in proof.splitlines() if x.startswith("TABLE ")]
    physicalPowerClass="NC_POWER_LV_P" if v=="4L" else "G31_POWER_P"
    tableCheck=all(any(t in x for x in table) for t in [f'class1="{physicalPowerClass}" class2=nil region="G31_U1_ESCAPE" physical="G31_POWER_ESCAPE"', 'class1="G31_GND_P" class2=nil region="G31_U1_ESCAPE" physical="G31_GND_ESCAPE"'])
    if v=="4L":tableCheck=tableCheck and any('class1="NC_POWER_LV_S" class2=nil region="G31_U1_ESCAPE" physical=nil spacing="G31_PIN_ESCAPE"' in x for x in table)
    scriptProof={"currentHash":h(board).upper(),"readonlyBefore":launch["beforeSHA256"],"readonlyAfter":launch["afterSHA256"]}
    challengesExpected={"BASELINE":0,"LOCAL_NECK_STRICT_1MM":12,"OUTSIDE_REGION_GLOBAL_RULES":13 if v=="4L" else 9,"CHALLENGES_RESTORED":0}
    if v=="4L":challengesExpected["LOCAL_SPACING_STRICT_030"]=30
    checks={
      "finalNativeInputReadonlyHashUnchanged":scriptProof["currentHash"]==scriptProof["readonlyBefore"]==scriptProof["readonlyAfter"] and launch["readonly"] and launch["completed"] and "-readonly" in launch["args"],
      "freshReadbackAndInventoryComplete":n["readbackDirectory"]==str(d) and "G_INVENTORY_COMPLETE" in read(d/"g_inventory_summary.txt") and "G_FINAL_NATIVE_PROOF_COMPLETE" in proof,
      "twentyFourPosesAnd96PinsUnchangedSinceReviewedCheckpoint":len(pose)==24 and all(x["samePoseAndBody"] and x["sameLogicalPinNetXYCopperBBox"] for x in pose) and sum(len([p for p in nowBy[r]["pins"] if p["number"]]) for r in wanted)==96,
      "exact27TOPSegmentsIncludingBulkMatch":expected==observed and len(top)==27,
      "allNinetyOneEtchSegmentsAccounted":len(actual)==91 and len(plane)==64 and all(x["net"]=="GND" and x["layer"]==refLayer for x in plane),
      "sixRetainedWholeNecks13657LocalNotGlobal":all(abs(r["nativeWholeNeckLength"]-1.365685424949238)<.0001 and r["withinLocal1_4"] and not r["satisfiesOriginalGlobal1_0"] for r in routes),
      "originalPhysicalRulesPreservedExceptScopedCopyNeck":bool(pDiff) and all(x["onlyMaxNeck1to1_4"] for x in pDiff),
      "fourLayerSpacingOnlyTwoFieldsCopied":(v=="2L" or bool(sDiff)) and all(x["onlyLineLineAndSMDPinLine03to02"] for x in sDiff),
      "oneRegionGroupExactlyThreeTOPRectangles":len([x for x in proof.splitlines() if x.startswith("REGION (")])==1 and boxes==expectedRegion and all('layer "CONSTRAINT REGION/TOP"' in x for x in regionlines),
      "onlySixMCUPowerAnchorsInScope":set((p["ref"],p["pin"]) for p in powerInside)=={("U1",str(x)) for x in (23,24,35,36,47,48)},
      "regionClassBindingsExplicit":tableCheck,
      "fourUniqueGNDViasThreeNewOneInherited":len(vias)==4 and set((x[1],x[2]) for x in vias)==expectedVia and all(x[3]=="GND" for x in vias),
      "oneActualFilledCurrentGNDPlane":len(shapes)==1 and shapes[0]["layer"]==refLayer and shapes[0]["net"]=="GND" and shapes[0]["filled"]=="t" and shapes[0]["generated"]=="t" and shapes[0]["fillOOD"]=="nil",
      "eightNativeTargetsAndFourReferenceGraphs":goals=={"t":8} and len(reference)==4 and all(x[2]==refLayer and x[3]=="1" for x in reference),
      "finalDynamicOOD0AndDRC0Current":"DYNAMIC_OOD=0" in proof and "DRC_STATUS\tG_FINAL\t0\tt" in proof and "DRC_STATUS\tG_SNAPSHOT\t0\tt" in read(d/"g_drc_details.txt"),
      "allChallengeStagesExpectedAndRestored":all(k in stages and stages[k]["errors"]==c and stages[k]["current"] for k,c in challengesExpected.items()) and "G_RULE_CHALLENGES_COMPLETE_NO_SAVE" in challenge,
      "outsideGlobalNeckAndSpacingProven":outsideNeck is not None and outsideSpacing is not None and 'expected "1 MM" actual "1.2 MM"' in outsideNeck and ('source "P_POWER_060"' if v=="4L" else 'source "G2L_POWER_DEMO"') in outsideNeck and ('source "S_POWER_030"' if v=="4L" else 'source "G2L_POWER_GND_SPACING"') in outsideSpacing,
      "insideChallengeNamesActual13657":'actual "1.3657 MM" name "Maximum Neck Length"' in challenge and 'source "G31_POWER_ESCAPE"' in challenge and 'source "G31_GND_ESCAPE"' in challenge,
      "challengeTemporaryCouponAbsentFinal":not any(any(p[1]>=49 for p in points(x["startEnd"])) for x in top) and len(vias)==4
    }
    files=[board,snap,d/"launch.json",d/"g_final_connectivity_constraints.txt",d/"route_geometry.tsv",d/"physical_csets.tsv",d/"spacing_csets.tsv",d/"class_table.tsv",d/"group_members.tsv",d/"g_copper_shapes.tsv",d/"vias.tsv",d/"g_drc_details.txt",d/"g_inventory_summary.txt",cd/"local_rule_challenges.txt",cd/"freeze.txt",G/"scripts/local_loops05.il",G/"scripts/local_copperG_v2.il"]
    res["variants"][v]={"status":"PASS_MCU_LOCAL_COPPER_AND_SCOPED_RULES" if all(checks.values()) else "REQUIRES_CORRECTION","checks":checks,"board":str(board),"boardIdentity":scriptProof,"nativeReadback":str(d),"poseAndPins":pose,"etchSegmentCounts":{"TOPManualLocal":len(top),"TOPV3V3":sum(x["net"]=="V3V3" for x in top),"TOPGND":sum(x["net"]=="GND" for x in top),"referenceLayerThermalGenerated":len(plane),"total":len(actual)},"threeLocalLoops":routes,"bulkBranch":bulk,"physicalCSetCopiedFieldDiffs":pDiff,"spacingCSetCopiedFieldDiffs":sDiff,"region":{"groups":1,"name":"G31_U1_ESCAPE","layer":"CONSTRAINT REGION/TOP","rectangles":boxes,"powerPinAnchorsInside":powerInside,"otherSignalPinAnchorsInside":otherInside,"note":"Other signal anchors can be geometrically inside; Region-Class bindings and existing Class-Class interactions determine rules. This is not a universal spacing waiver."},"uniqueVias":vias,"referenceShape":{"layer":shapes[0]["layer"],"area":float(shapes[0]["area"]),"bbox":points(shapes[0]["bbox"])},"conductiveTopology":"Each VDD pin has a short TOP route to its own 100nF cap. Its paired VSS has a direct TOP return to cap GND; one cap-side via joins this GND subgraph to actual reference copper. High-frequency local loop can return directly in TOP; plane reachability does not establish mandatory plane current. C16 GND attaches by a 3-segment branch at existing C15 GND-via node.","challengeStages":stages,"outsideGlobalNeckDetail":outsideNeck,"outsideGlobalLineSpacingDetail":outsideSpacing,"finalConnectivityTargets":re.findall(r"NATIVE_CONNECTIVITY[^\r\n]+",proof),"nativeReferenceProof":reference,"inputFilesSHA256":{str(p):h(p) for p in files}}
res["status"]="PASS_FINAL_MCU_SCOPE" if all(v["status"].startswith("PASS") for v in res["variants"].values()) else "REQUIRES_CORRECTION"
(R/"local_copper_independent_final_review.json").write_text(json.dumps(res,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps({"status":res["status"],"variants":{k:{"failed":[c for c,p in v["checks"].items() if not p],"checks":len(v["checks"]),"counts":v["etchSegmentCounts"],"boardSHA256":v["boardIdentity"]["currentHash"]} for k,v in res["variants"].items()}},ensure_ascii=True))
assert res["status"]=="PASS_FINAL_MCU_SCOPE"
